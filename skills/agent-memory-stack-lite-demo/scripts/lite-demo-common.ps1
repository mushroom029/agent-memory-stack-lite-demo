#requires -Version 7.0

function ConvertTo-LiteDemoVersion {
    param([Parameter(Mandatory=$true)][string]$Version)

    $trimmed = $Version.Trim()
    if ($trimmed -notmatch '(?i)^v?(?<base>\d+\.\d+\.\d+)(?<suffix>[a-z]?)$') {
        throw "Unsupported Lite Demo version: $Version"
    }

    $suffixRank = 0
    if ($Matches.suffix) {
        $suffixRank = ([int][char]$Matches.suffix.ToLowerInvariant()) - ([int][char]'a') + 1
    }

    [pscustomobject]@{
        Base = [version]$Matches.base
        Suffix = $Matches.suffix.ToLowerInvariant()
        SuffixRank = $suffixRank
        Normalized = "v$($Matches.base)$($Matches.suffix.ToLowerInvariant())"
    }
}

function Compare-LiteDemoVersion {
    param(
        [Parameter(Mandatory=$true)][string]$Left,
        [Parameter(Mandatory=$true)][string]$Right
    )

    $leftVersion = ConvertTo-LiteDemoVersion -Version $Left
    $rightVersion = ConvertTo-LiteDemoVersion -Version $Right
    $baseComparison = $leftVersion.Base.CompareTo($rightVersion.Base)
    if ($baseComparison -ne 0) {
        return [Math]::Sign($baseComparison)
    }
    return [Math]::Sign($leftVersion.SuffixRank.CompareTo($rightVersion.SuffixRank))
}

function Get-LiteDemoDirectoryFingerprint {
    param([Parameter(Mandatory=$true)][string]$Root)

    if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
        throw "Directory not found for fingerprint: $Root"
    }

    $records = @(
        Get-ChildItem -LiteralPath $Root -Recurse -File -Force | ForEach-Object {
            $relative = [System.IO.Path]::GetRelativePath($Root, $_.FullName).Replace("\", "/")
            $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToUpperInvariant()
            "$relative|$hash"
        } | Sort-Object
    )
    $payload = $records -join "`n"
    return [Convert]::ToHexString(
        [System.Security.Cryptography.SHA256]::HashData(
            [System.Text.Encoding]::UTF8.GetBytes($payload)
        )
    )
}

function Invoke-LiteDemoCheckedPwsh {
    param(
        [Parameter(Mandatory=$true)][string[]]$Arguments,
        [Parameter(Mandatory=$true)][string]$Label,
        [switch]$PassThru
    )

    $output = @(& pwsh @Arguments 2>&1)
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) {
        $detail = ($output | ForEach-Object { $_.ToString() }) -join "`n"
        throw "$Label failed with exit code $exitCode`n$detail"
    }
    if ($PassThru) {
        return $output
    }
}
