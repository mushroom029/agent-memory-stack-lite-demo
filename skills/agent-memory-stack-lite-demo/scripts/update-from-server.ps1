#requires -Version 7.0
[CmdletBinding()]
param(
    [string]$ManifestUrl = "https://159.75.127.201/agent-memory-stack/lite-demo/latest.json",
    [string]$CodexHome,
    [string]$ProjectRoot,
    [string]$GlobalAgentsPath,
    [switch]$WriteProjectAgents,
    [switch]$PreauthorizeMemoryLanding,
    [switch]$CheckOnly,
    [switch]$KeepDownload
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$OfficialPackage = "agent-memory-stack-lite-demo"
$OfficialChannel = "stable"

function Resolve-CodexHome {
    param([string]$Value)

    if ($Value) {
        return $Value
    }
    if ($env:CODEX_HOME) {
        return $env:CODEX_HOME
    }
    return (Join-Path $HOME ".codex")
}

function Read-JsonDocument {
    param([string]$Source)

    if (Test-Path -LiteralPath $Source) {
        return (Get-Content -LiteralPath $Source -Raw -Encoding UTF8 | ConvertFrom-Json)
    }

    $response = Invoke-WebRequest -Uri $Source -UseBasicParsing
    return ($response.Content | ConvertFrom-Json)
}

function Copy-Or-Download {
    param(
        [string]$Source,
        [string]$Destination
    )

    if (Test-Path -LiteralPath $Source) {
        Copy-Item -LiteralPath $Source -Destination $Destination -Force
        return
    }

    Invoke-WebRequest -Uri $Source -OutFile $Destination -UseBasicParsing
}

$CodexHome = Resolve-CodexHome -Value $CodexHome
$manifest = Read-JsonDocument -Source $ManifestUrl

if ($manifest.package -ne $OfficialPackage) {
    throw "Unexpected package in manifest: $($manifest.package)"
}
if ($manifest.channel -ne $OfficialChannel) {
    throw "Unexpected channel in manifest: $($manifest.channel)"
}
if (-not $manifest.version) {
    throw "Manifest missing version"
}
if (-not $manifest.zipUrl) {
    throw "Manifest missing zipUrl"
}
if (-not $manifest.sha256) {
    throw "Manifest missing sha256"
}

$installedVersionPath = Join-Path $CodexHome "skills/agent-memory-stack-lite-demo/VERSION.txt"
$installedVersion = if (Test-Path -LiteralPath $installedVersionPath) {
    (Get-Content -LiteralPath $installedVersionPath -Raw -Encoding UTF8).Trim()
} else {
    "unknown"
}

if ($CheckOnly) {
    [pscustomobject]@{
        Package = $manifest.package
        Channel = $manifest.channel
        InstalledVersion = $installedVersion
        LatestVersion = $manifest.version
        ManifestUrl = $ManifestUrl
        ZipUrl = $manifest.zipUrl
        SHA256 = $manifest.sha256
        NextPrompt = "启用外挂记忆"
        NaturalPrompt = "启动外挂记忆"
        LegacyPrompt = "启动lite demo"
    } | ConvertTo-Json -Depth 5
    exit 0
}

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("agent-memory-stack-lite-demo-update-" + [System.Guid]::NewGuid().ToString("N"))
$extractRoot = Join-Path $tempRoot "extract"
New-Item -ItemType Directory -Path $extractRoot -Force | Out-Null

try {
    $zipName = "agent-memory-stack-lite-demo-$($manifest.version).zip"
    $zipPath = Join-Path $tempRoot $zipName
    Copy-Or-Download -Source $manifest.zipUrl -Destination $zipPath

    $actualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToUpperInvariant()
    $expectedHash = ([string]$manifest.sha256).ToUpperInvariant()
    if ($actualHash -ne $expectedHash) {
        throw "SHA256 mismatch. Expected $expectedHash but got $actualHash"
    }

    Expand-Archive -LiteralPath $zipPath -DestinationPath $extractRoot -Force
    $packageRoot = Get-ChildItem -LiteralPath $extractRoot -Directory -Recurse |
        Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "scripts/install.ps1") } |
        Select-Object -First 1

    if (-not $packageRoot) {
        throw "Downloaded package does not contain scripts/install.ps1"
    }

    $checkScript = Join-Path $packageRoot.FullName "scripts/check-package.ps1"
    $installScript = Join-Path $packageRoot.FullName "scripts/install.ps1"

    & pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File $checkScript

    $installArgs = @(
        "-NoLogo",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        $installScript,
        "-CodexHome",
        $CodexHome,
        "-WriteGlobalAgents",
        "-UpdateExistingAgentsBlock",
        "-Force"
    )

    if ($ProjectRoot) {
        $installArgs += @("-ProjectRoot", $ProjectRoot)
    }
    if ($GlobalAgentsPath) {
        $installArgs += @("-GlobalAgentsPath", $GlobalAgentsPath)
    }
    if ($WriteProjectAgents) {
        $installArgs += "-WriteProjectAgents"
    }
    if ($PreauthorizeMemoryLanding) {
        $installArgs += "-PreauthorizeMemoryLanding"
    }

    & pwsh @installArgs

    [pscustomobject]@{
        Package = $manifest.package
        Channel = $manifest.channel
        PreviousInstalledVersion = $installedVersion
        InstalledVersion = $manifest.version
        CodexHome = $CodexHome
        ManifestUrl = $ManifestUrl
        ZipUrl = $manifest.zipUrl
        SHA256 = $actualHash
        Author = $manifest.author.name
        DouyinName = $manifest.author.douyinName
        DouyinId = $manifest.author.douyinId
        QQ = $manifest.author.qq
        NextPrompt = "启用外挂记忆"
        NaturalPrompt = "启动外挂记忆"
        LegacyPrompt = "启动lite demo"
    } | ConvertTo-Json -Depth 5
} finally {
    if (-not $KeepDownload -and (Test-Path -LiteralPath $tempRoot)) {
        Remove-Item -LiteralPath $tempRoot -Recurse -Force
    }
}
