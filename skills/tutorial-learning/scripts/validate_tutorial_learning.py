#!/usr/bin/env python3
"""Validate tutorial-learning structure, requests, and example artifacts."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from minimal_schema import validate_json_schema
ROOT=Path(__file__).resolve().parents[1]
REFS={'learning_contract.md','source_adapter_contract.md','source_profiles.md','source_fidelity.md','triage_protocol.md','lecture_template.md','review_protocol.md','interactive_webpage_contract.md','progressive_generation_contract.md','design_style_interface.md','learner_state_contract.md','evaluator_rubric.md'}
SCHEMAS={'tutorial_request.schema.json','source_outline.schema.json','triage.schema.json','review_plan.schema.json','evaluator_report.schema.json','learner_state.schema.json','next_lesson_context.schema.json'}
EXAMPLES={'markdown_basic','html_with_noise','pdf_excerpt_noisy','plain_text_headings'}
def load_json(path: Path, errors: list[str]):
    try: return json.loads(path.read_text())
    except Exception as exc:
        errors.append(f'invalid JSON {path}: {exc}'); return {}
def main():
    errors=[]
    for folder, required in [(ROOT/'references',REFS),(ROOT/'schemas',SCHEMAS)]:
        for name in sorted(required):
            if not (folder/name).is_file(): errors.append(f'missing {folder/name}')
    schemas={schema.name: load_json(schema, errors) for schema in sorted((ROOT/'schemas').glob('*.json'))}
    request_schema=schemas.get('tutorial_request.schema.json', {})
    for name in sorted(EXAMPLES):
        example=ROOT/'examples'/name; expected=example/'expected'; request_path=example/'request.json'
        if not expected.is_dir(): errors.append(f'missing {expected}'); continue
        request=load_json(request_path, errors)
        errors.extend(f'{request_path}: {message}' for message in validate_json_schema(request, request_schema))
        locator=request.get('source', {}).get('locator')
        if locator and not (example/locator).is_file(): errors.append(f'{request_path}: locator {locator!r} does not exist in fixture')
        outline=load_json(expected/'source_outline.json', errors)
        for trace in outline.get('sourceTraces', []):
            if locator and trace.get('locator') != locator:
                errors.append(f"{expected/'source_outline.json'}: trace {trace.get('id')} locator {trace.get('locator')!r} does not match request locator {locator!r}")
        result=subprocess.run([sys.executable, str(ROOT/'scripts'/'validate_artifact.py'), str(expected)], text=True, capture_output=True)
        if result.returncode: errors.append(result.stdout.strip() or result.stderr.strip())
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors)); return 1
    print('OK: tutorial-learning structure, requests, and examples')
    return 0
if __name__=='__main__': sys.exit(main())
