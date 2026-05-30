# skill-tune CLI wrapper: picks a working Python, then runs tune_session.py
$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot
$TuneSession = Join-Path $ScriptDir "tune_session.py"
$CheckRuntime = Join-Path $ScriptDir "check_runtime.py"

function Get-SkillTunePython {
    if ($env:SKILL_TUNE_PYTHON -and (Test-Path $env:SKILL_TUNE_PYTHON)) {
        return $env:SKILL_TUNE_PYTHON
    }
    foreach ($candidate in @("python", "python3")) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) {
            & $candidate -c "import sys" 2>$null
            if ($LASTEXITCODE -eq 0) { return (Get-Command $candidate).Source }
        }
    }
    if (Get-Command py -ErrorAction SilentlyContinue) {
        $exe = & py -3 -c "import sys; print(sys.executable)" 2>$null
        if ($LASTEXITCODE -eq 0 -and $exe) { return $exe.Trim() }
    }
    if (Test-Path $CheckRuntime) {
        $exe = & python $CheckRuntime 2>$null | Select-Object -First 1
        if (-not $exe) {
            $exe = & py -3 $CheckRuntime 2>$null | Select-Object -First 1
        }
        if ($exe) { return $exe.Trim() }
    }
    throw "No Python found. Run: py -3 scripts/check_runtime.py"
}

$Py = Get-SkillTunePython
& $Py $TuneSession @args
exit $LASTEXITCODE
