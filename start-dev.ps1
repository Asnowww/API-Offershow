param(
  [int]$BackendPort = 8000,
  [int]$FrontendPort = 5173,
  [string]$HostName = "127.0.0.1",
  [switch]$ResetMockData
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $Root "backend"
$FrontendDir = Join-Path $Root "frontend"
$RuntimeDir = Join-Path $Root ".runtime"
New-Item -ItemType Directory -Force $RuntimeDir | Out-Null

function Write-Step($Message) {
  Write-Host "[OfferShow] $Message"
}

function Test-Port($Port) {
  $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
  return $conn
}

function Wait-Http($Url, $Name) {
  for ($i = 1; $i -le 30; $i++) {
    try {
      Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2 | Out-Null
      Write-Step "$Name is ready: $Url"
      return
    } catch {
      Start-Sleep -Seconds 1
    }
  }
  throw "$Name did not become ready: $Url"
}

function Ensure-BackendEnv {
  $Python = Join-Path $BackendDir ".venv\Scripts\python.exe"
  if (!(Test-Path $Python)) {
    Write-Step "Creating backend virtual environment"
    python -m venv (Join-Path $BackendDir ".venv")
  }

  $Stamp = Join-Path $BackendDir ".venv\.deps-installed"
  $Req = Join-Path $BackendDir "requirements.txt"
  if (!(Test-Path $Stamp) -or ((Get-Item $Req).LastWriteTime -gt (Get-Item $Stamp).LastWriteTime)) {
    Write-Step "Installing backend dependencies"
    & $Python -m pip install -r $Req | Out-Host
    Set-Content -Path $Stamp -Value (Get-Date).ToString("o")
  }

  if ($ResetMockData) {
    Write-Step "Resetting PostgreSQL data from frontend mockData.js"
    & $Python -m app.scripts.import_frontend_mock | Out-Host
  }

  return $Python
}

function Ensure-FrontendEnv {
  if (!(Test-Path (Join-Path $FrontendDir "node_modules"))) {
    Write-Step "Installing frontend dependencies"
    Push-Location $FrontendDir
    try {
      npm install
    } finally {
      Pop-Location
    }
  }
}

$Python = [string](Ensure-BackendEnv | Select-Object -Last 1)
Ensure-FrontendEnv

$BackendPidFile = Join-Path $RuntimeDir "backend.pid"
$FrontendPidFile = Join-Path $RuntimeDir "frontend.pid"

$BackendConn = Test-Port $BackendPort
if ($BackendConn) {
  Write-Step "Backend port $BackendPort is already listening, pid=$($BackendConn.OwningProcess)"
  Set-Content -Path $BackendPidFile -Value $BackendConn.OwningProcess
} else {
  Write-Step "Starting backend on http://$HostName`:$BackendPort"
  $BackendOut = Join-Path $RuntimeDir "backend.out.log"
  $BackendErr = Join-Path $RuntimeDir "backend.err.log"
  $BackendProcess = Start-Process `
    -FilePath $Python `
    -ArgumentList @("-m", "uvicorn", "app.main:app", "--host", $HostName, "--port", "$BackendPort") `
    -WorkingDirectory $BackendDir `
    -WindowStyle Hidden `
    -PassThru `
    -RedirectStandardOutput $BackendOut `
    -RedirectStandardError $BackendErr
  Set-Content -Path $BackendPidFile -Value $BackendProcess.Id
}

Wait-Http "http://$HostName`:$BackendPort/api/v1/health" "Backend"

$FrontendConn = Test-Port $FrontendPort
if ($FrontendConn) {
  Write-Step "Frontend port $FrontendPort is already listening, pid=$($FrontendConn.OwningProcess)"
  Set-Content -Path $FrontendPidFile -Value $FrontendConn.OwningProcess
} else {
  Write-Step "Starting frontend on http://$HostName`:$FrontendPort"
  $FrontendOut = Join-Path $RuntimeDir "frontend.out.log"
  $FrontendErr = Join-Path $RuntimeDir "frontend.err.log"
  $FrontendCommand = "`$env:VITE_USE_MOCK='false'; npx vite --host $HostName --port $FrontendPort"
  $FrontendProcess = Start-Process `
    -FilePath "powershell.exe" `
    -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", $FrontendCommand) `
    -WorkingDirectory $FrontendDir `
    -WindowStyle Hidden `
    -PassThru `
    -RedirectStandardOutput $FrontendOut `
    -RedirectStandardError $FrontendErr
  Set-Content -Path $FrontendPidFile -Value $FrontendProcess.Id
}

Wait-Http "http://$HostName`:$FrontendPort" "Frontend"

Write-Host ""
Write-Step "Both services are running"
Write-Host "  Frontend: http://$HostName`:$FrontendPort"
Write-Host "  Backend:  http://$HostName`:$BackendPort"
Write-Host "  API docs: http://$HostName`:$BackendPort/docs"
Write-Host "  Logs:     $RuntimeDir"
Write-Host ""
Write-Host "Stop both services with:"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\stop-dev.ps1"
