#!/usr/bin/env python3
"""Validate tutorial-learning artifact sidecars with no third-party dependencies."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

REQUIRED = ("triage.json", "lecture.md", "review_plan.json", "evaluator_report.json")
DEPTH_RANK = {"skip": 0, "skim": 1, "standard": 2, "deep": 3}

def load_json(path: Path, errors: list[str]):
    try: return json.loads(path.read_text())
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}

def require(value, message, errors):
    if not value: errors.append(message)

def validate(root: Path) -> list[str]:
    errors=[]
    for name in REQUIRED:
        require((root/name).is_file(), f"{root}: missing {name}", errors)
    if errors: return errors
    triage=load_json(root/'triage.json', errors); review=load_json(root/'review_plan.json', errors); report=load_json(root/'evaluator_report.json', errors)
    lecture=(root/'lecture.md').read_text()
    outline=load_json(root/'source_outline.json', errors) if (root/'source_outline.json').is_file() else None
    blocks=triage.get('blocks', []); objectives=triage.get('learning_objectives', [])
    require(blocks, f"{root}: triage.blocks must not be empty", errors)
    require(2 <= len(objectives) <= 4, f"{root}: learning_objectives must contain 2-4 entries", errors)
    objective_ids=set(); trace_ids=set()
    if outline:
        trace_ids={t.get('id') for t in outline.get('sourceTraces', [])}
        require(outline.get('blocks'), f"{root}: source_outline.blocks must not be empty", errors)
    for obj in objectives:
        objective_ids.add(obj.get('id'))
        require(obj.get('sourceTraceIds'), f"{root}: objective {obj.get('id')} needs sourceTraceIds", errors)
    for block in blocks:
        bid=block.get('id'); role=block.get('content_role'); route=block.get('route'); depth=block.get('depth', {}); trace=block.get('sourceTrace', {})
        require(trace.get('id'), f"{root}: block {bid} needs sourceTrace.id", errors)
        require(role in {'core','supporting','reference_only','filler','deferred_ops'}, f"{root}: block {bid} has invalid content_role", errors)
        require(route in {'in_lecture','appendix','skip_with_deep_dive'}, f"{root}: block {bid} has invalid route", errors)
        if role == 'filler': require(route != 'in_lecture', f"{root}: filler block {bid} cannot route in_lecture", errors)
        if role == 'reference_only': require(route == 'appendix', f"{root}: reference_only block {bid} must route appendix", errors)
        if route == 'skip_with_deep_dive' and depth.get('importance',0) >= 3:
            dd=block.get('deep_dive', {})
            require(dd.get('url') or dd.get('note'), f"{root}: important skipped block {bid} needs deep_dive url or note", errors)
        rank=DEPTH_RANK.get(depth.get('study_depth'), -1)
        if depth.get('prerequisite_value',0)>=4 and depth.get('importance',0)>=3:
            require(rank>=2, f"{root}: block {bid} violates prerequisite-floor guardrail", errors)
        if depth.get('risk_flags'):
            require(rank>=2, f"{root}: block {bid} violates risk-floor guardrail", errors)
    require('## 微测' in lecture, f"{root}: lecture needs ## 微测", errors)
    require('预测' in lecture, f"{root}: lecture micro-test needs 预测", errors)
    require('用自己的话' in lecture, f"{root}: lecture micro-test needs 用自己的话", errors)
    if any(o.get('mastery')=='application' for o in objectives): require('应用' in lecture, f"{root}: application objective needs 应用 micro-test", errors)
    cards=review.get('cards', []); schedule=review.get('schedule', [])
    require(3 <= len(cards) <= 5, f"{root}: review cards must contain 3-5 entries", errors)
    scheduled={s.get('card_id') for s in schedule}
    covered=set()
    for card in cards:
        cid=card.get('id'); ids=card.get('objective_ids', []); traces=card.get('source_trace_ids', [])
        require(ids, f"{root}: card {cid} needs objective_ids", errors); require(traces, f"{root}: card {cid} needs source_trace_ids", errors)
        require(set(ids)<=objective_ids, f"{root}: card {cid} references unknown objective", errors)
        require(cid in scheduled, f"{root}: card {cid} needs schedule entry", errors); covered.update(ids)
    require(len(covered) >= max(1, (len(objective_ids)*4+4)//5), f"{root}: cards must cover at least 80% of objectives", errors)
    required_scores={'source_fidelity','triage_depth_routing','chinese_lecture_quality','assessment_review'}
    require(set(report.get('scores', {})) == required_scores, f"{root}: evaluator scores must contain exactly {sorted(required_scores)}", errors)
    failures=report.get('blocking_failures', [])
    require(isinstance(report.get('delivery_allowed'), bool), f"{root}: evaluator delivery_allowed must be boolean", errors)
    if failures: require(report.get('delivery_allowed') is False, f"{root}: blocking failures require delivery_allowed=false", errors)
    for name, score in report.get('scores', {}).items(): require(isinstance(score,int) and 0<=score<=5, f"{root}: evaluator score {name} must be integer 0-5", errors)
    return errors

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('artifact_dir', type=Path); args=parser.parse_args()
    errors=validate(args.artifact_dir)
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors)); return 1
    print(f'OK: {args.artifact_dir}')
    return 0
if __name__=='__main__': sys.exit(main())
