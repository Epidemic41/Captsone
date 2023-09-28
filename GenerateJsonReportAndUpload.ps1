

#input files
$currentStateJsonPath = "C:\Users\bob\Desktop\currentState.json"
$targetStateJsonPath = "C:\Users\bob\Desktop\targetState.json"
$nonCompliantPropertiesJsonPath = "C:\Users\bob\Desktop\nonCompliantOutput.json"
$compliantPropertiesJsonPath = "C:\Users\bob\Desktop\compliantOutput.json"

#output files
$reportOutputPath = "C:\Users\bob\Desktop\report.json"

# Get the current date in epoch (Unix timestamp)
$epochDate = [System.Math]::Round((Get-Date -UFormat %s))

# Get the hostname
$hostname = $env:COMPUTERNAME

# Get the IP address
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Ethernet0' | Where-Object { $_.IPAddress -ne '127.0.0.1' }).IPAddress

# Read the contents of the current state JSON file
$currentState = Get-Content -Path $currentStateJsonPath | ConvertFrom-Json

# Read the contents of the target state JSON file
$targetState = Get-Content -Path $targetStateJsonPath | ConvertFrom-Json

# Read the contents of the nonCompliant state JSON file
$nonCompliantProperties = Get-Content -Path $nonCompliantPropertiesJsonPath | ConvertFrom-Json

# Read the contents of the compliant JSON file
$compliantProperties = Get-Content -Path $compliantPropertiesJsonPath | ConvertFrom-Json

# Define the report template
$reportTemplate = @{
    "DateEpoch" = $epochDate
    "Hostname" = $hostname
    "IPAddress" = $ipAddress
    "CompliantTF" = $compliantTF
    "CurrentState" = $currentState
    "TargetState" = $targetState
    "ComparisonResults" = @{
        "compliantProperties" = $compliantProperties
        "nonCompliantProperties" = $nonCompliantProperties
    }
}

# Convert the report template to JSON format
$jsonOutput = $reportTemplate | ConvertTo-Json

# Write the JSON report to the specified output file
Set-Content -Path $reportOutputPath -Value $jsonOutput

Write-Host "Report generated and saved to $reportOutputPath."
