#!/usr/bin/env python3
"""Validate tutorial-learning artifact sidecars with no third-party dependencies."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from minimal_schema import validate_json_schema

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("source_outline.json", "triage.json", "lecture.md", "review_plan.json", "evaluator_report.json")
SCHEMA_FILES = {
    "source_outline.json": "source_outline.schema.json",
    "triage.json": "triage.schema.json",
    "review_plan.json": "review_plan.schema.json",
    "evaluator_report.json": "evaluator_report.schema.json",
}
DEPTH_RANK = {"skip": 0, "skim": 1, "standard": 2, "deep": 3}
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
    blocks=triage.get('blocks', []); objectives=triage.get('learning_objectives', [])
    outline_blocks=outline.get('blocks', []); trace_ids={t.get('id') for t in outline.get('sourceTraces', [])}
    outline_block_ids={b.get('id') for b in outline_blocks}; objective_ids=set()
    require(outline_blocks, f"{root}: source_outline.blocks must not be empty", errors)
    require(blocks, f"{root}: triage.blocks must not be empty", errors)
    require(2 <= len(objectives) <= 4, f"{root}: learning_objectives must contain 2-4 entries", errors)
    for block in outline_blocks:
        bid=block.get('id'); trace=block.get('sourceTrace', {})
        require(trace.get('id') in trace_ids, f"{root}: outline block {bid} references unknown trace {trace.get('id')}", errors)
    for obj in objectives:
        oid=obj.get('id'); objective_ids.add(oid)
        traces=obj.get('sourceTraceIds', [])
        require(traces, f"{root}: objective {oid} needs sourceTraceIds", errors)
        require(set(traces) <= trace_ids, f"{root}: objective {oid} references unknown source trace", errors)
    in_lecture_traces=set(); filler_titles=[]
    for block in blocks:
        bid=block.get('id'); role=block.get('content_role'); route=block.get('route'); depth=block.get('depth', {}); trace=block.get('sourceTrace', {})
        require(bid in outline_block_ids, f"{root}: triage block {bid} is missing from source outline", errors)
        require(trace.get('id') in trace_ids, f"{root}: block {bid} references unknown source trace {trace.get('id')}", errors)
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
    required_scores={'source_fidelity','triage_depth_routing','chinese_lecture_quality','assessment_review'}
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
