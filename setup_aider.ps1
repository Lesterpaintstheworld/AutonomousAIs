# Function to create and activate a virtual environment
function Create-AndActivateVenv {
    param([string]$path)
    if (Test-Path $path) {
        Write-Host "Virtual environment already exists at $path. Skipping creation."
    } else {
        Write-Host "Creating virtual environment at $path..."
        python -m venv $path
        if ($LASTEXITCODE -ne 0) { 
            Write-Host "Failed to create virtual environment at $path"
            exit 1 
        }
    }
    Write-Host "Activating virtual environment..."
    & "$path\Scripts\Activate.ps1"
    if ($LASTEXITCODE -ne 0) { 
        Write-Host "Failed to activate virtual environment at $path"
        exit 1 
    }
}

# Function to create an Aider function
function Create-AiderFunction {
    param([string]$name, [string]$path)
    $functionName = "Run-$($name -replace '-', '_')"
    $functionContent = @"
function global:$functionName {
    Write-Host "Activating $name environment..."
    `$env:VIRTUAL_ENV = "$path"
    `$env:PATH = "`$path\Scripts;`$env:PATH"
    `$pythonPath = "`$path\Scripts\python.exe"
    Write-Host "Using Python executable: `$pythonPath"
    Write-Host "Running $name with arguments: `$args"
    & `$pythonPath -m aider_nova `$args
    Write-Host "$name execution completed."
}
"@
    Invoke-Expression $functionContent
    Set-Alias -Name $name -Value $functionName -Scope Global
    Write-Host "Function and alias for $name created/updated."
}

# Main script
$instance = "aider_nova"
Write-Host "Setting up $instance..."

$venvPath = "$env:USERPROFILE\synthetic-souls\venv"
$repoPath = "C:\Users\reyno\synthetic-souls"

# Create and activate virtual environment
Create-AndActivateVenv $venvPath

# Update pip and setuptools
python -m pip install --upgrade pip setuptools wheel

# Update the existing repository
Write-Host "Updating Aider repository..."
Set-Location $repoPath
git pull

# Install or update Aider and its dependencies
Write-Host "Installing/Updating Aider and dependencies..."

if (Test-Path "requirements.txt") {
    Write-Host "Installing from requirements.txt..."
    pip install -r requirements.txt
} else {
    Write-Host "No requirements.txt found. Installing aider-chat manually."
    pip install aider-chat
}

# Install additional dependencies
pip install GitPython python-dotenv prompt_toolkit PyYAML

# Verify Python version in this venv
Write-Host "Verifying Python version for ${instance}:"
& "$venvPath\Scripts\python.exe" --version

# Create function and alias
Create-AiderFunction $instance $venvPath

# Deactivate virtual environment
deactivate
Write-Host "Setup for $instance completed successfully."
Write-Host "--------------------------------------------------"

Write-Host "Setup complete. You can now use the $instance alias."

# Add this to your PowerShell profile
$profileContent = @"
# Aider function and alias
$((Get-Command Create-AiderFunction).Definition)
$((Get-Command "Run-$($instance -replace '-', '_')").Definition)
New-Alias -Name $instance -Value Run-$($instance -replace '-', '_') -Scope Global
"@

Add-Content $PROFILE $profileContent

Write-Host "Setup script has been added to your PowerShell profile. Please restart your PowerShell or run '. `$PROFILE' to use the new function and alias."