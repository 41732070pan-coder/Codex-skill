#!/usr/bin/env python3
"""Validate tutorial-learning structure and examples."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REFS={'learning_contract.md','source_adapter_contract.md','source_profiles.md','source_fidelity.md','triage_protocol.md','lecture_template.md','review_protocol.md','evaluator_rubric.md'}
SCHEMAS={'tutorial_request.schema.json','source_outline.schema.json','triage.schema.json','review_plan.schema.json','evaluator_report.schema.json'}
EXAMPLES={'markdown_basic','html_with_noise','pdf_excerpt_noisy'}
def main():
    errors=[]
    for folder, required in [(ROOT/'references',REFS),(ROOT/'schemas',SCHEMAS)]:
        for name in sorted(required):
            if not (folder/name).is_file(): errors.append(f'missing {folder/name}')
    for schema in sorted((ROOT/'schemas').glob('*.json')):
        try: json.loads(schema.read_text())
        except Exception as exc: errors.append(f'invalid JSON {schema}: {exc}')
    for name in sorted(EXAMPLES):
        expected=ROOT/'examples'/name/'expected'
        if not expected.is_dir(): errors.append(f'missing {expected}'); continue
        result=subprocess.run([sys.executable, str(ROOT/'scripts'/'validate_artifact.py'), str(expected)], text=True, capture_output=True)
        if result.returncode: errors.append(result.stdout.strip() or result.stderr.strip())
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors)); return 1
    print('OK: tutorial-learning structure and examples')
    return 0
if __name__=='__main__': sys.exit(main())
