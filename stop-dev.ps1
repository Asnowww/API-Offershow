param(
  [int[]]$Ports = @(5173, 8000)
)

$ErrorActionPreference = "SilentlyContinue"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$RuntimeDir = Join-Path $Root ".runtime"

function Write-Step($Message) {
  Write-Host "[OfferShow] $Message"
}

function Stop-ProcessTree($ProcessId) {
  if (!$ProcessId) { return }
  $children = Get-CimInstance Win32_Process | Where-Object { $_.ParentProcessId -eq $ProcessId }
  foreach ($child in $children) {
    Stop-ProcessTree $child.ProcessId
  }
  $proc = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
  if ($proc) {
    Write-Step "Stopping pid=$ProcessId ($($proc.ProcessName))"
    Stop-Process -Id $ProcessId -Force
  }
}

foreach ($name in @("frontend", "backend")) {
  $pidFile = Join-Path $RuntimeDir "$name.pid"
  if (Test-Path $pidFile) {
    $pidValue = Get-Content $pidFile | Select-Object -First 1
    Stop-ProcessTree ([int]$pidValue)
    Remove-Item $pidFile -Force
  }
}

foreach ($port in $Ports) {
  $listeners = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
  foreach ($listener in $listeners) {
    Stop-ProcessTree ([int]$listener.OwningProcess)
  }
}

Write-Step "Stopped development services"

