# Define the paths to the JSON files
$currentStatePath = "C:\Users\David\Documents\ASU\currentState.json"
$targetStatePath = "C:\Users\David\Documents\ASU\Capstone\targetState.json"

# Read the content of the JSON files
$currentState = Get-Content -Path $currentStatePath | ConvertFrom-Json
$targetState = Get-Content -Path $targetStatePath | ConvertFrom-Json

# Define a flag to track compliance
$compliant = $true

# Loop through keys in target state
foreach ($key in $targetState.PSObject.Properties.Name) {
    if ($key -eq "DateEpoch" -or $key -eq "Hostname" -or $key -eq "IPAddress"){
        continue
    }

    #stores value assoicated with key
    $targetValue = $targetState.$key
    $currentValue = $currentState.$key

    # check if array -isarray, -contains
    # recurision function
    if ($targetValue -is [array]) {
         if ($currentValue -contains $targetValue) {
            Write-Host "!Property $key is not compliant. Target: $targetValue, Current: $currentValue"
            $compliant = $false
    }
        if ($currentValue -contains $targetValue) {
            Write-Host "*Property $key is compliant. Target: $targetValue, Current: $currentValue"
    }
    }

    # if not array do bellow
    # Check if current value matches target value
    if (-not ($targetValue -is [array])) {
        if ($currentValue -ne $targetValue) {
            Write-Host "!Property $key is not compliant. Target: $targetValue, Current: $currentValue"
            $compliant = $false
    }
        if ($currentValue -eq $targetValue) {
            Write-Host "*Property $key is compliant. Target: $targetValue, Current: $currentValue"
    }
     }

}

# Check compliance status
if ($compliant) {
    Write-Host "The current state is compliant with the target state."
} else {
    Write-Host "The current state is not compliant with the target state."
}
