Param(
    [string]$AliasName = "bluxq",
    [string]$Target = "bluxq"
)

Write-Host "Registering PowerShell alias '$AliasName' for '$Target'"
New-Alias -Name $AliasName -Value $Target -Force
Write-Host "Alias registered. Add to your profile for persistence."
