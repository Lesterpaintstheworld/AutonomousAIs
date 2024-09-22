# Définir l'encodage d'entrée et de sortie en UTF-8
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Write-ColoredOutput {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [Parameter(Mandatory=$false)]
        [ConsoleColor]$ForegroundColor = [ConsoleColor]::White
    )
    
    Write-Host $Message -ForegroundColor $ForegroundColor
}

function Invoke-StreamingRequest {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Url,

        [Parameter(Mandatory=$true)]
        [string]$Role,

        [Parameter(Mandatory=$false)]
        [string]$Folder,

        [Parameter(Mandatory=$false)]
        [string]$Request
    )

    Write-ColoredOutput "Démarrage de la requête streaming vers $Url" -ForegroundColor Cyan

    try {
        $body = @{
            role = $Role
            folder = $Folder
            request = $Request
        } | ConvertTo-Json

        $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)

        $webRequest = [System.Net.WebRequest]::Create($Url)
        $webRequest.Method = "POST"
        $webRequest.ContentType = "application/json"
        $webRequest.ContentLength = $bodyBytes.Length
        $webRequest.Timeout = 3600000  # 1 hour in milliseconds

        $requestStream = $webRequest.GetRequestStream()
        $requestStream.Write($bodyBytes, 0, $bodyBytes.Length)
        $requestStream.Close()

        $response = $webRequest.GetResponse()
        $responseStream = $response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($responseStream)

        Write-ColoredOutput "Connexion établie. Début du streaming..." -ForegroundColor Green

        $lineCount = 0
        while (-not $reader.EndOfStream) {
            if ([Console]::KeyAvailable -and [Console]::ReadKey($true).Key -eq [ConsoleKey]::C -and [Console]::KeyAvailable -and [Console]::ReadKey($true).Modifiers -eq [ConsoleModifiers]::Control) {
                Write-ColoredOutput "`nInterruption demandée. Arrêt du streaming..." -ForegroundColor Yellow
                break
            }

            $line = $reader.ReadLine()
            if ($line) {
                $lineCount++
                try {
                    $jsonObject = $line | ConvertFrom-Json
                    if ($jsonObject.output) {
                        Write-ColoredOutput "$lineCount : $($jsonObject.output)" -ForegroundColor Yellow
                    } elseif ($jsonObject.error) {
                        Write-ColoredOutput "$lineCount : $($jsonObject.error)" -ForegroundColor Red
                    } elseif ($jsonObject.debug) {
                        Write-ColoredOutput "$lineCount : $($jsonObject.debug)" -ForegroundColor Cyan
                    } else {
                        Write-ColoredOutput "$lineCount : $line" -ForegroundColor Magenta
                    }
                } catch {
                    Write-ColoredOutput "$lineCount : $line" -ForegroundColor Magenta
                }
            }
        }
    }
    catch {
        Write-ColoredOutput "Erreur lors de la requête : $_" -ForegroundColor Red
        Write-ColoredOutput "StackTrace : $($_.Exception.StackTrace)" -ForegroundColor Red
    }
    finally {
        if ($reader) { $reader.Close() }
        if ($responseStream) { $responseStream.Close() }
        if ($response) { $response.Close() }
        Write-ColoredOutput "Streaming terminé. Lecture de $lineCount lignes." -ForegroundColor Green
    }
}

# Traitement des arguments en ligne de commande
$Url = "https://autonomous.digitalkin.ai/kinos"
$Role = ""
$Folder = ""
$Request = ""

for ($i = 0; $i -lt $args.Count; $i++) {
    switch ($args[$i]) {
        "-Agent" { $Role = $args[$i+1]; $i++ }
        "-Mission" { $Folder = $args[$i+1]; $i++ }
        "-Url" { $Url = $args[$i+1]; $i++ }
        "-Message" { $Request = $args[$i+1]; $i++ }
    }
}

# Vérification des paramètres obligatoires
if ([string]::IsNullOrEmpty($Role)) {
    Write-ColoredOutput "Le paramètre -Agent est obligatoire." -ForegroundColor Red
    exit
}

# Utilisation de la fonction avec les paramètres
Invoke-StreamingRequest -Url $Url -Role $Role -Folder $Folder -Request $Request