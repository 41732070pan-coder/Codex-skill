#!/usr/bin/env python3
"""Validate medium-neutral tutorial-learning design bundles with no third-party dependencies."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from minimal_schema import validate_json_schema

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "source_outline.json", "triage.json", "review_plan.json", "evaluator_report.json",
    "learning_plan.md", "lecture.md", "tutorial_structure.md", "triage.md",
    "assessment_plan.md", "practice_plan.md", "review_plan.md", "source_fidelity.md",
)
SCHEMA_FILES = {
    "source_outline.json": "source_outline.schema.json",
    "triage.json": "triage.schema.json",
    "review_plan.json": "review_plan.schema.json",
    "evaluator_report.json": "evaluator_report.schema.json",
}
DEPTH_RANK = {"skip": 0, "skim": 1, "standard": 2, "deep": 3}
TRACE_FIELDS = ("source_format", "locator", "pageRange", "headingPath", "anchor", "url", "blockId", "extractionSlice", "boundaryConfidence", "evidenceType")
DOC_HEADINGS = {
    "learning_plan.md": ("# 学习计划", "## 学习范围与目标", "## 内容规模判断", "## 学习阶段安排", "## 本轮设计范围", "## 后续设计规则", "## 复习节奏"),
    "tutorial_structure.md": ("# 教程结构", "## 教学单元", "## 下游渲染交接"),
    "triage.md": ("# 内容取舍", "## 路由决策", "## 跳过内容"),
    "assessment_plan.md": ("# 测验计划", "## 尝试优先规则", "## 微测"),
    "practice_plan.md": ("# 练习计划", "## 练习任务", "## 验收标准"),
    "review_plan.md": ("# 复习计划", "## 复习卡", "## 复习节奏"),
    "source_fidelity.md": ("# 来源忠实度", "## 来源边界", "## 证据与推断", "## 省略项"),
}
LECTURE_HEADINGS = ("## 本节目标", "## 来源与边界", "## 学习路线", "## 核心讲解", "## 微测", "## 练习任务", "## 复习卡", "## 阅读材料（附录）", "## 复盘")
FORBIDDEN_PRESENTATION = ("interactive_tutorial.html", "my-design-style", "chinese-traditional-color-style", "data-design-skill", "<html", "localStorage", "CSS", "JavaScript")

def load_json(path: Path, errors: list[str]):
    try: return json.loads(path.read_text())
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}

def require(value, message, errors):
    if not value: errors.append(message)

def section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", text)
    return match.group(1).strip() if match else ""

def frontmatter(text: str) -> str:
    match = re.match(r"(?s)^---\s*\n(.*?)\n---\s*(?:\n|$)", text)
    return match.group(1) if match else ""

def require_unique(items, label: str, root: Path, errors: list[str]):
    values=[item.get("id") for item in items]
    require(all(values), f"{root}: {label} ids must be non-empty", errors)
    require(len(values) == len(set(values)), f"{root}: {label} ids must be unique", errors)

def require_canonical_trace(trace: dict, canonical: dict, label: str, root: Path, errors: list[str]):
    tid=trace.get("id")
    require(tid in canonical, f"{root}: {label} references unknown trace {tid}", errors)
    if tid not in canonical: return
    for field in TRACE_FIELDS:
        require(trace.get(field) == canonical[tid].get(field), f"{root}: {label} sourceTrace {tid} field {field} conflicts with canonical trace", errors)

def validate(root: Path) -> list[str]:
    errors=[]
    for name in REQUIRED: require((root/name).is_file(), f"{root}: missing {name}", errors)
    for removed in ("interactive_tutorial.html", "state/learner_state.json", "state/next_lesson_context.json"):
        require(not (root/removed).exists(), f"{root}: presentation/runtime artifact must be removed: {removed}", errors)
    if errors: return errors
    docs={name: load_json(root/name, errors) for name in SCHEMA_FILES}
    for name, schema_name in SCHEMA_FILES.items():
        schema=load_json(ROOT/'schemas'/schema_name, errors)
        errors.extend(f"{root/name}: {message}" for message in validate_json_schema(docs[name], schema))
    outline, triage, review, report=(docs[x] for x in ("source_outline.json", "triage.json", "review_plan.json", "evaluator_report.json"))
    markdown={name:(root/name).read_text() for name in REQUIRED if name.endswith('.md')}
    for name, headings in DOC_HEADINGS.items():
        for heading in headings: require(heading in markdown[name], f"{root}: {name} needs {heading}", errors)
    for name, text in markdown.items():
        for token in FORBIDDEN_PRESENTATION: require(token not in text, f"{root}: {name} must remain medium-neutral; found {token!r}", errors)
    blocks, objectives=triage.get('blocks', []), triage.get('learning_objectives', [])
    outline_blocks, source_traces=outline.get('blocks', []), outline.get('sourceTraces', [])
    require_unique(source_traces, 'source trace', root, errors); require_unique(outline_blocks, 'outline block', root, errors)
    require_unique(blocks, 'triage block', root, errors); require_unique(objectives, 'objective', root, errors)
    require(outline_blocks, f"{root}: source_outline.blocks must not be empty", errors); require(blocks, f"{root}: triage.blocks must not be empty", errors)
    require(2 <= len(objectives) <= 4, f"{root}: learning_objectives must contain 2-4 entries", errors)
    canonical={t.get('id'):t for t in source_traces if t.get('id')}; trace_ids=set(canonical); outline_ids={b.get('id') for b in outline_blocks}; objective_ids={o.get('id') for o in objectives}
    for block in outline_blocks: require_canonical_trace(block.get('sourceTrace', {}), canonical, f"outline block {block.get('id')}", root, errors)
    for obj in objectives:
        traces=obj.get('sourceTraceIds', []); require(traces, f"{root}: objective {obj.get('id')} needs sourceTraceIds", errors); require(set(traces)<=trace_ids, f"{root}: objective {obj.get('id')} references unknown source trace", errors)
    in_lecture_traces=set(); filler_titles=[]
    for block in blocks:
        bid=block.get('id'); role=block.get('content_role'); route=block.get('route'); depth=block.get('depth', {}); trace=block.get('sourceTrace', {})
        require(bid in outline_ids, f"{root}: triage block {bid} is missing from source outline", errors); require_canonical_trace(trace, canonical, f"triage block {bid}", root, errors)
        require(trace.get('blockId') == bid, f"{root}: triage block {bid} sourceTrace blockId must match block id", errors)
        if route == 'in_lecture': in_lecture_traces.add(trace.get('id'))
        if role == 'filler': filler_titles.append(block.get('title','')); require(route != 'in_lecture', f"{root}: filler block {bid} cannot route in_lecture", errors)
        if role == 'reference_only': require(route == 'appendix', f"{root}: reference_only block {bid} must route appendix", errors)
        rank=DEPTH_RANK.get(depth.get('study_depth'), -1)
        if depth.get('prerequisite_value', 0)>=4 and depth.get('importance', 0)>=3: require(rank>=2, f"{root}: block {bid} violates prerequisite-floor guardrail", errors)
        if depth.get('risk_flags'): require(rank>=2, f"{root}: block {bid} violates risk-floor guardrail", errors)
    lecture=markdown['lecture.md']; fm=frontmatter(lecture)
    for heading in LECTURE_HEADINGS: require(heading in lecture, f"{root}: lecture needs {heading}", errors)
    require(re.search(r"(?m)^skill:\s*tutorial-learning\s*$", fm), f"{root}: lecture front matter skill must be tutorial-learning", errors)
    core=section(lecture, '## 核心讲解')
    for trace in in_lecture_traces: require(trace in lecture and trace in markdown['source_fidelity.md'], f"{root}: routed trace {trace} must appear in lecture and source_fidelity.md", errors)
    for title in filler_titles:
        if title: require(title not in core, f"{root}: filler title {title!r} leaked into lecture core", errors)
    cards=review.get('cards', []); schedule=review.get('schedule', []); require(3<=len(cards)<=5, f"{root}: review cards must contain 3-5 entries", errors)
    scheduled={s.get('card_id') for s in schedule}; covered=set()
    for card in cards:
        cid=card.get('id'); ids=card.get('objective_ids', []); traces=card.get('source_trace_ids', [])
        require(set(ids)<=objective_ids and ids, f"{root}: card {cid} references unknown or empty objectives", errors); require(set(traces)<=trace_ids and traces, f"{root}: card {cid} references unknown or empty traces", errors); require(cid in scheduled, f"{root}: card {cid} needs schedule entry", errors); require(cid in markdown['review_plan.md'], f"{root}: review_plan.md needs card {cid}", errors); covered.update(ids)
    require(len(covered) >= max(1, (len(objective_ids)*4+4)//5), f"{root}: cards must cover at least 80% of objectives", errors)
    required_scores={'source_fidelity','triage_depth_routing','chinese_lecture_quality','assessment_review','tutorial_design_completeness'}
    require(set(report.get('scores', {})) == required_scores, f"{root}: evaluator scores must contain exactly {sorted(required_scores)}", errors)
    require(isinstance(report.get('delivery_allowed'), bool), f"{root}: evaluator delivery_allowed must be boolean", errors)
    if report.get('blocking_failures'): require(report.get('delivery_allowed') is False, f"{root}: blocking failures require delivery_allowed=false", errors)
    return errors

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('artifact_dir', type=Path); args=parser.parse_args(); errors=validate(args.artifact_dir)
    if errors: print('\n'.join(f'ERROR: {e}' for e in errors)); return 1
    print(f'OK: {args.artifact_dir}'); return 0
if __name__=='__main__': sys.exit(main())
