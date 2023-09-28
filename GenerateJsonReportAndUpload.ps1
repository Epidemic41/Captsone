

#input files
$currentStateJsonPath = "C:\Users\bob\Desktop\currentState.json"
$targetStateJsonPath = "C:\Users\bob\Desktop\targetState.json"

#output files
$nonCompliantJsonPath = "C:\Users\bob\Desktop\nonCompliantOutput.json"
$compliantJsonPath = "C:\Users\bob\Desktop\compliantOutput.json"
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
$nonCompliant = Get-Content -Path $nonCompliantJsonPath | ConvertFrom-Json

# Read the contents of the compliant JSON file
$compliant = Get-Content -Path $compliantJsonPath | ConvertFrom-Json

# Define the report template
$reportTemplate = @{
    "DateEpoch" = $epochDate
    "Hostname" = $hostname
    "IPAddress" = $ipAddress
    "Compliant" = $compliant
    "currentState" = $currentState
    "targetState" = $targetState
    "comparisonResults" = @{
    ##############################################################two $compliant variables. one is array, other is boolean, need to have the boolean be acessable globally. just rename boolean to $COMPLIANCEBOOLEAN
        "compliantProperties" = $compliant
        "nonCompliantProperties" = $nonCompliant
    }
}

# Convert the report template to JSON format
$jsonOutput = $reportTemplate | ConvertTo-Json

# Write the JSON report to the specified output file
Set-Content -Path $reportOutputPath -Value $jsonOutput

Write-Host "Report generated and saved to $reportOutputPath."
