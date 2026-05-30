#!/usr/bin/env python3
"""Run tutorial-learning example regressions."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    for example in sorted((ROOT/'examples').iterdir()):
        if not example.is_dir(): continue
        result=subprocess.run([sys.executable, str(ROOT/'scripts'/'validate_artifact.py'), str(example/'expected')])
        if result.returncode: return result.returncode
    print('OK: tutorial-learning examples')
    return 0
if __name__=='__main__': sys.exit(main())
