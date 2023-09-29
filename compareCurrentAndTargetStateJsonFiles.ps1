# Define a function to check compliance
function Check-Compliance {
    param (
        [Parameter(Mandatory=$true)]
        [PSCustomObject]$CurrentState,
        
        [Parameter(Mandatory=$true)]
        [PSCustomObject]$TargetState
    )

    $nonCompliantProperties = @()
    $compliantProperties = @()
    $compliantTF = $true

    foreach ($key in $TargetState.PSObject.Properties.Name) {
        $targetValue = $TargetState.$key
        $currentValue = $CurrentState.$key

        if ($targetValue -is [array]) {
            if (-not (Compare-Object $currentValue $targetValue -SyncWindow 0)) {
                $compliantProperties += Create-PropertyObject $key $targetValue $currentValue
            } else {
                Write-Host "!Property $key is not compliant. Target: $($targetValue -join ', '), Current: $($currentValue -join ', ')"
                $compliantTF = $false
                $nonCompliantProperties += Create-PropertyObject $key $targetValue $currentValue
            }
        } elseif ($currentValue -ne $targetValue) {
            Write-Host "!Property $key is not compliant. Target: $targetValue, Current: $currentValue"
            $compliantTF = $false
            $nonCompliantProperties += Create-PropertyObject $key $targetValue $currentValue
        } else {
            $compliantProperties += Create-PropertyObject $key $targetValue $currentValue
        }
    }

    return @{
        Compliant = $compliantTF
        NonCompliantProperties = $nonCompliantProperties
        CompliantProperties = $compliantProperties
    }
}

# Define a function to create a property object
function Create-PropertyObject {
    param (
        [string]$Property,
        $TargetValue,
        $CurrentValue
    )

    return @{
        Property = $Property
        TargetValue = $TargetValue
        CurrentValue = $CurrentValue
    }
}

# Parameterize Paths
param (
    [string]$CurrentStatePath = "C:\Users\bob\Desktop\currentState.json",
    [string]$TargetStatePath = "C:\Users\bob\Desktop\targetState.json",
    [string]$NonCompliantOutputPath = "C:\Users\bob\Desktop\nonCompliantOutput.json",
    [string]$CompliantOutputPath = "C:\Users\bob\Desktop\CompliantOutput.json"
)

# Read JSON files and convert to PSCustomObject
$currentState = Get-Content -Path $CurrentStatePath | ConvertFrom-Json
$targetState = Get-Content -Path $TargetStatePath | ConvertFrom-Json

# Check compliance and get results
$results = Check-Compliance -CurrentState $currentState -TargetState $targetState

# Save properties to JSON files
$results.NonCompliantProperties | ConvertTo-Json | Set-Content -Path $NonCompliantOutputPath
$results.CompliantProperties | ConvertTo-Json | Set-Content -Path $CompliantOutputPath

# Output compliance status
if ($results.Compliant) {
    Write-Host "The current state is compliant with the target state."
} else {
    Write-Host "The current state is not compliant with the target state."
}
