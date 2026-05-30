#!/usr/bin/env python3
"""Validate tutorial-learning artifact sidecars with no third-party dependencies."""
from __future__ import annotations
import argparse, html, json, re, sys
from pathlib import Path
from minimal_schema import validate_json_schema

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("source_outline.json", "triage.json", "lecture.md", "learning_plan.md", "interactive_tutorial.html", "review_plan.json", "evaluator_report.json", "state/learner_state.json", "state/next_lesson_context.json")
SCHEMA_FILES = {
    "source_outline.json": "source_outline.schema.json",
    "triage.json": "triage.schema.json",
    "review_plan.json": "review_plan.schema.json",
    "evaluator_report.json": "evaluator_report.schema.json",
    "state/learner_state.json": "learner_state.schema.json",
    "state/next_lesson_context.json": "next_lesson_context.schema.json",
}
DEPTH_RANK = {"skip": 0, "skim": 1, "standard": 2, "deep": 3}
TRACE_FIELDS = ("source_format", "locator", "pageRange", "headingPath", "anchor", "url", "blockId", "extractionSlice", "boundaryConfidence", "evidenceType")
LEARNING_PLAN_HEADINGS = (
    "# 学习计划", "## 学习范围与目标", "## 内容规模判断", "## 学习阶段安排",
    "## 本轮生成范围", "## 后续生成规则", "## 复习节奏",
)
LECTURE_HEADINGS = (
    "## 本节目标", "## 来源与边界", "## 学习路线", "## 核心讲解", "## 微测",
    "## 练习任务", "## 复习卡", "## 阅读材料（附录）", "## 复盘",
)

def load_json(path: Path, errors: list[str]):
    try: return json.loads(path.read_text())
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}

def require(value, message, errors):
    if not value: errors.append(message)

def section(lecture: str, heading: str) -> str:
    match = re.search(rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", lecture)
    return match.group(1).strip() if match else ""

def frontmatter(lecture: str) -> str:
    match = re.match(r"(?s)^---\s*\n(.*?)\n---\s*(?:\n|$)", lecture)
    return match.group(1) if match else ""

def markdown_table(section_text: str) -> tuple[list[str], list[list[str]]]:
    rows=[]
    for line in section_text.splitlines():
        if line.strip().startswith('|') and line.strip().endswith('|'):
            rows.append([cell.strip() for cell in line.strip().strip('|').split('|')])
    if len(rows) < 2: return [], []
    return rows[0], rows[2:]

def require_unique(items, label: str, root: Path, errors: list[str]):
    values=[item.get("id") for item in items]
    require(all(values), f"{root}: {label} ids must be non-empty", errors)
    require(len(values) == len(set(values)), f"{root}: {label} ids must be unique", errors)

def require_canonical_trace(trace: dict, canonical_traces: dict, label: str, root: Path, errors: list[str]):
    tid=trace.get("id")
    require(tid in canonical_traces, f"{root}: {label} references unknown trace {tid}", errors)
    if tid not in canonical_traces:
        return
    canonical=canonical_traces[tid]
    for field in TRACE_FIELDS:
        require(trace.get(field) == canonical.get(field), f"{root}: {label} sourceTrace {tid} field {field} conflicts with canonical trace: expected {canonical.get(field)!r}, got {trace.get(field)!r}", errors)

def validate(root: Path) -> list[str]:
    errors=[]
    for name in REQUIRED:
        require((root/name).is_file(), f"{root}: missing {name}", errors)
    if errors: return errors
    docs = {name: load_json(root/name, errors) for name in SCHEMA_FILES}
    if errors: return errors
    for name, schema_name in SCHEMA_FILES.items():
        schema = load_json(ROOT/'schemas'/schema_name, errors)
        errors.extend(f"{root/name}: {message}" for message in validate_json_schema(docs[name], schema))
    outline=docs['source_outline.json']; triage=docs['triage.json']; review=docs['review_plan.json']; report=docs['evaluator_report.json']
    lecture=(root/'lecture.md').read_text()
    learning_plan=(root/'learning_plan.md').read_text()
    interactive_html=(root/'interactive_tutorial.html').read_text()
    blocks=triage.get('blocks', []); objectives=triage.get('learning_objectives', [])
    outline_blocks=outline.get('blocks', []); source_traces=outline.get('sourceTraces', [])
    require_unique(source_traces, 'source trace', root, errors)
    require_unique(outline_blocks, 'outline block', root, errors)
    require_unique(blocks, 'triage block', root, errors)
    require_unique(objectives, 'objective', root, errors)
    canonical_traces={t.get('id'): t for t in source_traces if t.get('id')}
    trace_ids=set(canonical_traces)
    outline_block_ids={b.get('id') for b in outline_blocks}; objective_ids=set()
    require(outline_blocks, f"{root}: source_outline.blocks must not be empty", errors)
    require(blocks, f"{root}: triage.blocks must not be empty", errors)
    require(2 <= len(objectives) <= 4, f"{root}: learning_objectives must contain 2-4 entries", errors)
    for block in outline_blocks:
        bid=block.get('id'); trace=block.get('sourceTrace', {})
        require_canonical_trace(trace, canonical_traces, f'outline block {bid}', root, errors)
    for obj in objectives:
        oid=obj.get('id'); objective_ids.add(oid)
        traces=obj.get('sourceTraceIds', [])
        require(traces, f"{root}: objective {oid} needs sourceTraceIds", errors)
        require(set(traces) <= trace_ids, f"{root}: objective {oid} references unknown source trace", errors)
    in_lecture_traces=set(); filler_titles=[]
    for block in blocks:
        bid=block.get('id'); role=block.get('content_role'); route=block.get('route'); depth=block.get('depth', {}); trace=block.get('sourceTrace', {})
        require(bid in outline_block_ids, f"{root}: triage block {bid} is missing from source outline", errors)
        require_canonical_trace(trace, canonical_traces, f'triage block {bid}', root, errors)
        require(trace.get('blockId') == bid, f"{root}: triage block {bid} sourceTrace blockId must match block id", errors)
        require(role in {'core','supporting','reference_only','filler','deferred_ops'}, f"{root}: block {bid} has invalid content_role", errors)
        require(route in {'in_lecture','appendix','skip_with_deep_dive'}, f"{root}: block {bid} has invalid route", errors)
        if route == 'in_lecture': in_lecture_traces.add(trace.get('id'))
        if role == 'filler':
            filler_titles.append(block.get('title', ''))
            require(route != 'in_lecture', f"{root}: filler block {bid} cannot route in_lecture", errors)
        if role == 'reference_only': require(route == 'appendix', f"{root}: reference_only block {bid} must route appendix", errors)
        if route == 'skip_with_deep_dive' and depth.get('importance',0) >= 3:
            dd=block.get('deep_dive', {})
            require(dd.get('url') or dd.get('note'), f"{root}: important skipped block {bid} needs deep_dive url or note", errors)
        rank=DEPTH_RANK.get(depth.get('study_depth'), -1)
        if depth.get('prerequisite_value',0)>=4 and depth.get('importance',0)>=3:
            require(rank>=2, f"{root}: block {bid} violates prerequisite-floor guardrail", errors)
        if depth.get('risk_flags'):
            require(rank>=2, f"{root}: block {bid} violates risk-floor guardrail", errors)
    for heading in LEARNING_PLAN_HEADINGS:
        require(heading in learning_plan, f"{root}: learning plan needs {heading}", errors)
    require(re.search(r"交付模式[：:]\s*(complete_course|progressive_chapter)", learning_plan), f"{root}: learning plan needs an explicit delivery mode", errors)
    require('| 阶段 |' in learning_plan and '| 状态 |' in learning_plan, f"{root}: learning plan needs a staged schedule table with status", errors)
    mode_match=re.search(r"交付模式[：:]\s*(complete_course|progressive_chapter)", learning_plan)
    require('<!doctype html' in interactive_html.lower(), f"{root}: interactive tutorial needs an HTML doctype", errors)
    require('id="home-nav"' in interactive_html and 'aria-label="学习导航"' in interactive_html, f"{root}: interactive tutorial needs accessible homepage navigation", errors)
    require('data-design-skill="my-design-style"' in interactive_html and 'data-theme="chinese-traditional-color-style"' in interactive_html, f"{root}: interactive tutorial must expose the default pluggable Chinese traditional design theme", errors)
    for hook in ('id="learning-plan"', 'lesson-page', 'id="lesson-content"', 'id="micro-test"', 'id="practice-task"', 'id="lesson-complete"', 'id="review-center"'):
        require(hook in interactive_html, f"{root}: interactive tutorial needs {hook}", errors)
    for label in ('学习计划', '复习中心', '预测', '用自己的话', '练习任务'):
        require(label in interactive_html, f"{root}: interactive tutorial needs learner-facing {label}", errors)
    if mode_match:
        mode=mode_match.group(1)
        require(f'data-delivery-mode="{mode}"' in interactive_html, f"{root}: interactive tutorial body must use delivery mode {mode}", errors)
        if mode == 'progressive_chapter':
            require('data-page-state="ready-to-generate"' in interactive_html, f"{root}: progressive interactive tutorial needs a ready-to-generate navigation entry", errors)
            require('data-page-state="locked"' in interactive_html, f"{root}: progressive interactive tutorial needs inspectable locked navigation entries", errors)
            for progressive_hook in ('生成并开始下一课', 'generateNextLesson', 'explanationPreference'):
                require(progressive_hook in interactive_html, f"{root}: progressive interactive tutorial needs {progressive_hook}", errors)
    lesson_content_match=re.search(r'(?s)<section id="lesson-content"[^>]*>(.*?)</section>', interactive_html)
    lesson_content=re.sub(r'<[^>]+>', ' ', lesson_content_match.group(1)) if lesson_content_match else ''
    require(len(re.sub(r'\s+', '', lesson_content)) >= 40, f"{root}: interactive tutorial lesson content is too thin", errors)
    require(re.search(r'[\u4e00-\u9fff]', lesson_content), f"{root}: interactive tutorial lesson content needs Chinese explanation", errors)
    normalized_core=re.sub(r'\s+', ' ', section(lecture, '## 核心讲解')).strip()
    normalized_html=re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', interactive_html))).strip()
    require(normalized_core and normalized_core in normalized_html, f"{root}: interactive tutorial must render the lecture core explanation", errors)
    for trace in in_lecture_traces: require(trace in interactive_html, f"{root}: interactive tutorial does not expose routed source trace {trace}", errors)
    for js_hook in ('localStorage', 'addEventListener', 'showView', 'revealAnswer', 'completeLesson', 'exportLearnerState', 'buildNextLessonContext'):
        require(js_hook in interactive_html, f"{root}: interactive tutorial JavaScript needs {js_hook}", errors)
    require('下载学习记录' in interactive_html and '导出下一课上下文' in interactive_html, f"{root}: portable tutorial needs visible learner-state and next-context export actions", errors)
    fm=frontmatter(lecture)
    require(fm, f"{root}: lecture needs YAML front matter", errors)
    for key in ('skill', 'source_format', 'section_id'):
        require(re.search(rf"(?m)^{key}:\s*\S+", fm), f"{root}: lecture front matter needs {key}", errors)
    require(re.search(r"(?m)^learning_objectives:\s*(?:\S+|$)", fm), f"{root}: lecture front matter needs learning_objectives", errors)
    require(re.search(r"(?m)^skill:\s*tutorial-learning\s*$", fm), f"{root}: lecture front matter skill must be tutorial-learning", errors)
    require(re.search(r"(?m)^source_format:\s*(pdf|html|markdown|plain_text_with_headings)\s*$", fm), f"{root}: lecture front matter source_format is invalid", errors)
    for heading in LECTURE_HEADINGS:
        require(heading in lecture, f"{root}: lecture needs {heading}", errors)
    boundary=section(lecture, '## 来源与边界'); route_table=section(lecture, '## 学习路线'); core=section(lecture, '## 核心讲解'); cards_section=section(lecture, '## 复习卡')
    require('|' in boundary and any(trace in boundary for trace in in_lecture_traces), f"{root}: source boundary table needs an in-lecture trace id", errors)
    route_header, route_rows=markdown_table(route_table)
    require(route_header and '深度' in route_header, f"{root}: learning route needs a depth table", errors)
    if '深度' in route_header:
        depth_index=route_header.index('深度')
        for row in route_rows:
            require(len(row) > depth_index and row[depth_index] in DEPTH_RANK, f"{root}: learning route depth must be one of {sorted(DEPTH_RANK)}", errors)
    require('|' in cards_section, f"{root}: review cards section needs a table", errors)
    require('预测' in section(lecture, '## 微测'), f"{root}: lecture micro-test needs 预测", errors)
    require('用自己的话' in section(lecture, '## 微测'), f"{root}: lecture micro-test needs 用自己的话", errors)
    if any(o.get('mastery')=='application' for o in objectives): require('应用' in section(lecture, '## 微测'), f"{root}: application objective needs 应用 micro-test", errors)
    for trace in in_lecture_traces: require(trace in boundary or trace in core, f"{root}: lecture does not expose core trace {trace}", errors)
    for title in filler_titles:
        if title: require(title not in core, f"{root}: filler title {title!r} leaked into lecture core", errors)
    cards=review.get('cards', []); schedule=review.get('schedule', [])
    require(3 <= len(cards) <= 5, f"{root}: review cards must contain 3-5 entries", errors)
    scheduled={s.get('card_id') for s in schedule}; covered=set()
    for card in cards:
        cid=card.get('id'); ids=card.get('objective_ids', []); traces=card.get('source_trace_ids', [])
        require(ids, f"{root}: card {cid} needs objective_ids", errors); require(traces, f"{root}: card {cid} needs source_trace_ids", errors)
        require(set(ids)<=objective_ids, f"{root}: card {cid} references unknown objective", errors)
        require(set(traces)<=trace_ids, f"{root}: card {cid} references unknown source trace", errors)
        require(cid in scheduled, f"{root}: card {cid} needs schedule entry", errors)
        require(cid in cards_section, f"{root}: lecture review table needs card {cid}", errors); covered.update(ids)
    require(len(covered) >= max(1, (len(objective_ids)*4+4)//5), f"{root}: cards must cover at least 80% of objectives", errors)
    required_scores={'source_fidelity','triage_depth_routing','chinese_lecture_quality','assessment_review','interactive_web_learning'}
    require(set(report.get('scores', {})) == required_scores, f"{root}: evaluator scores must contain exactly {sorted(required_scores)}", errors)
    failures=report.get('blocking_failures', [])
    require(isinstance(report.get('delivery_allowed'), bool), f"{root}: evaluator delivery_allowed must be boolean", errors)
    if failures: require(report.get('delivery_allowed') is False, f"{root}: blocking failures require delivery_allowed=false", errors)
    return errors

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('artifact_dir', type=Path); args=parser.parse_args()
    errors=validate(args.artifact_dir)
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors)); return 1
    print(f'OK: {args.artifact_dir}')
    return 0
if __name__=='__main__': sys.exit(main())
