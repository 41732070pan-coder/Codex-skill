#!/usr/bin/env python3
"""Validate tutorial-learning structure, requests, and example design bundles."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from minimal_schema import validate_json_schema
ROOT=Path(__file__).resolve().parents[1]
REFS={'learning_contract.md','source_adapter_contract.md','source_profiles.md','source_fidelity.md','triage_protocol.md','lecture_template.md','review_protocol.md','learning_route_contract.md','evaluator_rubric.md'}
REMOVED_REFS={'design_style_interface.md','interactive_webpage_contract.md','learner_state_contract.md','progressive_generation_contract.md'}

def main():
    errors=[]
    actual={p.name for p in (ROOT/'references').glob('*.md')}
    missing=REFS-actual
    if missing: errors.append(f"missing references: {sorted(missing)}")
    stale=REMOVED_REFS & actual
    if stale: errors.append(f"presentation/runtime references must be removed: {sorted(stale)}")
    schema=json.loads((ROOT/'schemas'/'tutorial_request.schema.json').read_text())
    for example in sorted((ROOT/'examples').iterdir()):
        if not example.is_dir(): continue
        request=json.loads((example/'request.json').read_text())
        errors.extend(f"{example/'request.json'}: {message}" for message in validate_json_schema(request, schema))
        result=subprocess.run([sys.executable, str(ROOT/'scripts'/'validate_artifact.py'), str(example/'expected')], text=True, capture_output=True)
        if result.returncode: errors.append(result.stdout.strip() or result.stderr.strip())
    if errors: print('\n'.join(f"ERROR: {e}" for e in errors)); return 1
    print('OK: tutorial-learning structure, requests, and examples'); return 0
if __name__=='__main__': sys.exit(main())
