{% autoescape off %}# Installation de FinCompta (Windows 10/11 64 bits).
# Dans PowerShell :  irm {{ script_url }} | iex
# Télécharge la dernière version publiée sur infos.fincompta.net, vérifie son
# empreinte SHA-256 puis l'installe (une confirmation administrateur est demandée).
& {
    $ErrorActionPreference = 'Stop'
    $ProgressPreference = 'SilentlyContinue'
    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

    $manifeste = @{}
    foreach ($ligne in (Invoke-WebRequest -UseBasicParsing '{{ manifeste_url }}').Content -split "`r?`n") {
        if ($ligne -match '^\s*([a-z0-9]+)\s*=\s*(.*?)\s*$') { $manifeste[$Matches[1]] = $Matches[2] }
    }
    if (-not $manifeste.url -or -not $manifeste.sha256) { throw "Aucune version de FinCompta n'est disponible pour le moment." }

    $setup = Join-Path $env:TEMP "FinCompta-Setup-$($manifeste.version).exe"
    Write-Host "Téléchargement de FinCompta $($manifeste.version)..." -ForegroundColor Cyan
    Invoke-WebRequest -UseBasicParsing $manifeste.url -OutFile $setup
    if ((Get-FileHash $setup -Algorithm SHA256).Hash -ne $manifeste.sha256) {
        Remove-Item $setup -ErrorAction SilentlyContinue
        throw "Le fichier téléchargé est incomplet ou altéré : relancez l'installation."
    }

    Write-Host "Installation de FinCompta $($manifeste.version)..." -ForegroundColor Cyan
    $p = Start-Process $setup -ArgumentList '/SILENT', '/SP-', '/NORESTART', '/CLOSEAPPLICATIONS' -Verb RunAs -Wait -PassThru
    Remove-Item $setup -ErrorAction SilentlyContinue
    if ($p.ExitCode -ne 0) { throw "L'installation a échoué ou a été annulée (code $($p.ExitCode))." }
    Write-Host "FinCompta $($manifeste.version) est installé : icône « FinCompta » du Bureau ou du menu Démarrer." -ForegroundColor Green
}
{% endautoescape %}