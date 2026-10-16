# Creates Desktop and Start menu shortcuts:
#   verse-ai         - today's study in its own window
#   verse-ai poster  - today's verse as an animated poster in your browser
#
# Run once from the project folder:
#   powershell -ExecutionPolicy Bypass -File make_shortcut.ps1

$project = $PSScriptRoot
$venvPython = Join-Path $project ".venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    $python = $venvPython
} else {
    $found = Get-Command python -ErrorAction SilentlyContinue
    if ($null -eq $found -or $found.Source -like "*WindowsApps*") {
        Write-Error "Python not found. Install Python 3.10+ from python.org, then run this again."
        exit 1
    }
    $python = $found.Source
}
# pythonw runs without a console window, which the poster doesn't need.
$pythonw = Join-Path (Split-Path $python) "pythonw.exe"
if (-not (Test-Path $pythonw)) { $pythonw = $python }

$shortcuts = @(
    @{ Name = "verse-ai";        Exe = $python;  Script = "main.py";   Description = "verse-ai: daily Bible study" },
    @{ Name = "verse-ai poster"; Exe = $pythonw; Script = "visual.py"; Description = "verse-ai: today's verse as an animated poster" }
)
$folders = @(
    [Environment]::GetFolderPath("Desktop"),
    (Join-Path ([Environment]::GetFolderPath("StartMenu")) "Programs")
)

$shell = New-Object -ComObject WScript.Shell
foreach ($folder in $folders) {
    foreach ($s in $shortcuts) {
        $path = Join-Path $folder "$($s.Name).lnk"
        $shortcut = $shell.CreateShortcut($path)
        $shortcut.TargetPath = $s.Exe
        $shortcut.Arguments = "`"$(Join-Path $project $s.Script)`""
        $shortcut.WorkingDirectory = $project
        $shortcut.Description = $s.Description
        $shortcut.Save()
        Write-Output "Created $path"
    }
}
