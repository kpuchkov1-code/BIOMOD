# Restores Claude Code's project memory from this repo into the local
# Claude config so Claude on this laptop has full context for the BIOMOD project.
#
# Run from PowerShell while sitting in the cloned repo folder:
#   ./claude-memory/restore-memory.ps1
#
# Then launch `claude` from your home directory (e.g. C:\Users\<you>) so it
# picks up the memory under that working directory.

$ErrorActionPreference = "Stop"

# Claude encodes the working directory by replacing ':' and '\' with '-'.
# Memory lives under <home>\.claude\projects\<encoded-home>\memory.
# We target the HOME directory, which is where `claude` is launched from.
$home_dir = $env:USERPROFILE
$encoded  = ($home_dir -replace ':', '-') -replace '\\', '-'
$target   = Join-Path $home_dir ".claude\projects\$encoded\memory"

New-Item -ItemType Directory -Force -Path $target | Out-Null

$src = Join-Path $PSScriptRoot "*.md"
Copy-Item $src -Destination $target -Force

Write-Output "Restored Claude memory to:"
Write-Output "  $target"
Write-Output ""
Write-Output "Files:"
Get-ChildItem $target -Filter *.md | Select-Object -ExpandProperty Name | ForEach-Object { Write-Output "  $_" }
Write-Output ""
Write-Output "Now run 'claude' from $home_dir and it will have the project context."
