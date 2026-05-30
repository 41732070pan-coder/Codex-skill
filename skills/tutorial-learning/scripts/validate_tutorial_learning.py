#!/usr/bin/env python3
"""Validate tutorial-learning structure, requests, examples, and validator regressions."""
from __future__ import annotations
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
from minimal_schema import validate_json_schema
ROOT=Path(__file__).resolve().parents[1]
REFS={'learning_contract.md','source_adapter_contract.md','source_profiles.md','source_fidelity.md','triage_protocol.md','lecture_template.md','review_protocol.md','tutorial_modes.md','personalization_contract.md','learning_route_contract.md','lesson_design_contract.md','evaluator_rubric.md'}
REMOVED_REFS={'design_style_interface.md','interactive_webpage_contract.md','learner_state_contract.md','progressive_generation_contract.md'}
EXAMPLE_AUDIT_SIDECARS={'source_outline.json','triage.json','learning_route.json','review_plan.json','evaluator_report.json'}
VALIDATOR=ROOT/'scripts'/'validate_artifact.py'

def run_validator(path: Path):
    return subprocess.run([sys.executable, str(VALIDATOR), str(path)], text=True, capture_output=True)

def validate_regressions(example_dir: Path, errors: list[str]):
    with tempfile.TemporaryDirectory() as tmp:
        markdown_only=Path(tmp)/'markdown-only'
        shutil.copytree(example_dir, markdown_only)
        for name in EXAMPLE_AUDIT_SIDECARS: (markdown_only/name).unlink()
        lecture=markdown_only/'lecture.md'
        lecture.write_text(lecture.read_text()+'\nCSS、JavaScript 和 localStorage 可以作为教程源术语保留。\n')
        result=run_validator(markdown_only)
        if result.returncode: errors.append(f"markdown-only bundle with source terms should validate: {result.stdout.strip() or result.stderr.strip()}")
        (markdown_only/'learning_route.json').write_text((example_dir/'learning_route.json').read_text())
        result=run_validator(markdown_only)
        if result.returncode: errors.append(f"valid standalone optional learning_route.json should validate when present: {result.stdout.strip() or result.stderr.strip()}")
        (markdown_only/'learning_route.json').write_text('{"stages": []}')
        result=run_validator(markdown_only)
        if result.returncode == 0: errors.append('invalid optional learning_route.json should fail schema validation when present')
        (markdown_only/'learning_route.json').unlink()
        lecture.write_text(lecture.read_text()+'\nrender as final HTML\n')
        result=run_validator(markdown_only)
        if result.returncode == 0: errors.append('final HTML rendering instruction should fail medium-neutral validation')
        lecture.write_text(lecture.read_text().replace('render as final HTML\n', '').replace('evidence_granularity: paragraph', 'evidence_granularity: outline'))
        result=run_validator(markdown_only)
        if result.returncode == 0: errors.append('chapter_tutorial with outline-only evidence should fail depth-gate validation')
        lecture.write_text(lecture.read_text().replace('design_mode: chapter_tutorial', 'design_mode: route_overview').replace('lesson_count: 1', 'lesson_count: 0').replace('### Lesson ', '### Orientation '))
        result=run_validator(markdown_only)
        if result.returncode: errors.append(f"route_overview should allow outline evidence without deep lessons: {result.stdout.strip() or result.stderr.strip()}")

def main():
    errors=[]
    actual={p.name for p in (ROOT/'references').glob('*.md')}
    missing=REFS-actual
    if missing: errors.append(f"missing references: {sorted(missing)}")
    stale=REMOVED_REFS & actual
    if stale: errors.append(f"presentation/runtime references must be removed: {sorted(stale)}")
    schema=json.loads((ROOT/'schemas'/'tutorial_request.schema.json').read_text())
    examples=[]
    for example in sorted((ROOT/'examples').iterdir()):
        if not example.is_dir(): continue
        expected=example/'expected'; examples.append(expected)
        request=json.loads((example/'request.json').read_text())
        errors.extend(f"{example/'request.json'}: {message}" for message in validate_json_schema(request, schema))
        missing_sidecars={name for name in EXAMPLE_AUDIT_SIDECARS if not (expected/name).is_file()}
        if missing_sidecars: errors.append(f"{expected}: maintained example needs complete JSON audit bundle; missing={sorted(missing_sidecars)}")
        result=run_validator(expected)
        if result.returncode: errors.append(result.stdout.strip() or result.stderr.strip())
    if examples: validate_regressions(examples[0], errors)
    if errors: print('\n'.join(f"ERROR: {e}" for e in errors)); return 1
    print('OK: tutorial-learning structure, requests, examples, and validator regressions'); return 0
if __name__=='__main__': sys.exit(main())
