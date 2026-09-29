param(
    [string]$EnvName = "test",
    [string]$Marker = ""
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$Python = if (Test-Path ".venv\Scripts\python.exe") {
    ".venv\Scripts\python.exe"
} else {
    "python"
}

$Arguments = @("run.py", "--env", $EnvName)
if ($Marker) {
    $Arguments += @("-m", $Marker)
}

& $Python @Arguments
exit $LASTEXITCODE
