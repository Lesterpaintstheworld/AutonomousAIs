# Function to create and activate a virtual environment
function Create-And-Activate-Venv($path) {
    if (Test-Path $path) {
        Write-Host "Virtual environment already exists at $path. Skipping creation."
    } else {
        Write-Host "Creating virtual environment at $path..."
        python -m venv $path
        if (-not $?) {
            throw "Failed to create virtual environment at $path"
        }
    }
    Write-Host "Activating virtual environment..."
    & "$path\Scripts\Activate.ps1"
    if (-not $?) {
        throw "Failed to activate virtual environment at $path"
    }
}

# Function to create an Aider function and alias
function Create-Aider-Function($name, $path) {
    $functionName = "Run-$($name.Replace('-', ''))"
    $functionContent = @"
function global:$functionName {
    param(`$arguments)
    Write-Host "Activating $name environment..."
    `$env:VIRTUAL_ENV = "$path"
    `$env:PATH = "`$path\Scripts;" + `$env:PATH
    `$pythonPath = "$path\Scripts\python.exe"
    Write-Host "Using Python executable: `$pythonPath"
    Write-Host "Running $name with arguments: `$arguments"
    & `$pythonPath -m aider `$arguments
    Write-Host "$name execution completed."
}
"@
    Invoke-Expression $functionContent
    Set-Alias -Name $name -Value $functionName -Scope Global -Force
    Write-Host "Function and alias for $name created/updated."
}

# Function to invoke Aider
function Invoke-Aider {
    param (
        [Parameter(Mandatory=$true)]
        [ValidateSet("lyra", "pixel", "rhythm", "vox")]
        [string]$Instance,
        
        [Parameter(ValueFromRemainingArguments=$true)]
        [string[]]$Arguments
    )
    
    $functionName = "Run-aider$Instance"
    if (Get-Command $functionName -ErrorAction SilentlyContinue) {
        & $functionName $Arguments
    } else {
        Write-Error "Function $functionName not found. Make sure it's properly defined."
    }
}

# Check for required tools
$requiredTools = @("git", "python", "pip")
foreach ($tool in $requiredTools) {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        throw "$tool is not installed or not in PATH. Please install it and try again."
    }
}

# Main script
$aiderInstances = @("aider-lyra", "aider-pixel", "aider-rhythm", "aider-vox")
foreach ($instance in $aiderInstances) {
    Write-Host "Setting up $instance..."
    
    $venvPath = "C:\Users\conta\Synthetic Souls\$instance\venv"
    $repoPath = "C:\Users\conta\Synthetic Souls\$instance"

    # Create and activate virtual environment
    try {
        Create-And-Activate-Venv $venvPath
    } catch {
        Write-Host "Error setting up virtual environment for $instance"
        Write-Host $_.Exception.Message
        continue
    }

    # Check if Aider is already installed
    if ((Test-Path "$repoPath\setup.py") -or (Test-Path "$repoPath\pyproject.toml")) {
        Write-Host "Aider already exists at $repoPath. Updating..."
        Push-Location $repoPath
        git pull
        Pop-Location
    } else {
        Write-Host "Aider not found in $repoPath. Please ensure Aider is installed in this directory."
        continue
    }

    # Install or update Aider
    Write-Host "Installing/Updating Aider..."
    pip install -e $repoPath
    if (-not $?) {
        Write-Host "Failed to install/update Aider for $instance"
        continue
    }

    # Verify Python version in this venv
    Write-Host "Verifying Python version for $instance:"
    & "$venvPath\Scripts\python.exe" --version

    # Create function and alias
    Create-Aider-Function $instance $venvPath

    # Deactivate virtual environment
    deactivate
    Write-Host "Setup for $instance completed successfully."
    Write-Host "--------------------------------------------------"
}

Write-Host "Setup complete. You can now use Invoke-Aider or the individual aliases."

# Add this to your PowerShell profile
$profileContent = @"
# Aider functions and aliases
$(Get-Content $MyInvocation.MyCommand.Path)

# Invoke-Aider function
function Invoke-Aider {
    param (
        [Parameter(Mandatory=`$true)]
        [ValidateSet("lyra", "pixel", "rhythm", "vox")]
        [string]`$Instance,
        
        [Parameter(ValueFromRemainingArguments=`$true)]
        [string[]]`$Arguments
    )
    
    `$functionName = "Run-aider`$Instance"
    if (Get-Command `$functionName -ErrorAction SilentlyContinue) {
        & `$functionName `$Arguments
    } else {
        Write-Error "Function `$functionName not found. Make sure it's properly defined."
    }
}
"@

Add-Content -Path $PROFILE -Value $profileContent

Write-Host "Setup script has been added to your PowerShell profile. Please restart your PowerShell session or run 'Import-Module `$PROFILE' to use the new functions and aliases."