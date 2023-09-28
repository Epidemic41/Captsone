# Define the paths to the JSON files

#input files
$currentStatePath = "C:\Users\bob\Desktop\currentState.json"
$targetStatePath = "C:\Users\bob\Desktop\targetState.json"

#output files
$nonCompliantOutputPath = "C:\Users\bob\Desktop\nonCompliantOutput.json"
$compliantOutputPath = "C:\Users\bob\Desktop\CompliantOutput.json"

# Read the content of the JSON files
$currentState = Get-Content -Path $currentStatePath | ConvertFrom-Json
$targetState = Get-Content -Path $targetStatePath | ConvertFrom-Json

# Define a flag to track compliance
$global:compliant = $true

# Arrays to store compliant and non-compliant properties
$nonCompliantProperties = @()
$compliantProperties = @()

# Loop through keys in target state
foreach ($key in $targetState.PSObject.Properties.Name) {

    #stores value associated with key
    $targetValue = $targetState.$key
    $currentValue = $currentState.$key

    # check if array -isarray, -contains
    # recursion function
    if ($targetValue -is [array]) {
        if ($currentValue -contains $targetValue) {
            Write-Host "!Property $key is not compliant. Target: $targetValue, Current: $currentValue"
            $compliant = $false
            $nonCompliantProperties += @{
                Property = $key
                TargetValue = $targetValue
                CurrentValue = $currentValue
            }
        }
        else {
            $compliantProperties += @{
                Property = $key
                TargetValue = $targetValue
                CurrentValue = $currentValue
            }
        }
    }

    # if not array do below
    # Check if current value matches target value
    elseif ($currentValue -ne $targetValue) {
        Write-Host "!Property $key is not compliant. Target: $targetValue, Current: $currentValue"
        $compliant = $false
        $nonCompliantProperties += @{
            Property = $key
            TargetValue = $targetValue
            CurrentValue = $currentValue
        }
    }
    else {
        $compliantProperties += @{
            Property = $key
            TargetValue = $targetValue
            CurrentValue = $currentValue
        }
    }

}

# Save non-compliant properties to a JSON file
$nonCompliantProperties | ConvertTo-Json | Set-Content -Path $nonCompliantOutputPath

# Save compliant properties to a JSON file
$compliantProperties | ConvertTo-Json | Set-Content -Path $compliantOutputPath

# Check compliance status
if ($compliant) {
    Write-Host "The current state is compliant with the target state."
} else {
    Write-Host "The current state is not compliant with the target state."
}
