$DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

python -m pip install --user cryptography

$LauncherPath = Join-Path $DIR "206s.ps1"
@"
`$env:PYTHONPATH = "$DIR"
python -m tool.cli @args
"@ | Set-Content -Path $LauncherPath

if (!(Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
}

$FunctionLine = "function 206s { & `"$LauncherPath`" @args }"
$ProfileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
if ($ProfileContent -notlike "*$FunctionLine*") {
    Add-Content -Path $PROFILE -Value $FunctionLine
    Write-Host "[+] Alias added to $PROFILE"
}

Write-Host "[+] Restart PowerShell, then run: 206s"