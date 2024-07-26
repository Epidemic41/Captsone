function Get-IPAddress {
    param (
        [string]$InterfaceAlias = 'Ethernet0'
    )

    try {
        $ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias $InterfaceAlias | Where-Object { $_.IPAddress -ne '127.0.0.1' }).IPAddress
        if ($null -eq $ip) { throw "No IP Address found for InterfaceAlias: $InterfaceAlias" }
        return $ip
    } catch {
        Write-Error "Error getting IP Address: $_"
        return $null
    }
}

function Generate-Report {
    param (
        [string]$CurrentStatePath,
        [string]$TargetStatePath,
        [string]$NonCompliantPropertiesPath,
        [string]$CompliantPropertiesPath,
        [string]$ReportOutputPath
    )

    try {
        $epochDate = [Math]::Round((Get-Date -UFormat %s))
        $hostname = $env:COMPUTERNAME
        $ipAddress = Get-IPAddress -InterfaceAlias 'Ethernet0'

        $currentState = Get-Content -Path $CurrentStatePath | ConvertFrom-Json
        $targetState = Get-Content -Path $TargetStatePath | ConvertFrom-Json
        $nonCompliantProperties = Get-Content -Path $NonCompliantPropertiesPath | ConvertFrom-Json
        $compliantProperties = Get-Content -Path $CompliantPropertiesPath | ConvertFrom-Json
        
        $compliantTF = $null -eq $nonCompliantProperties # You might need to adjust this depending on how you define compliance

        $report = @{
            DateEpoch             = $epochDate
            Hostname              = $hostname
            IPAddress             = $ipAddress
            CompliantTF           = $compliantTF
            CurrentState          = $currentState
            TargetState           = $targetState
            ComparisonResults     = @{
                compliantProperties    = $compliantProperties
                nonCompliantProperties = $nonCompliantProperties
            }
        }

        $report | ConvertTo-Json | Set-Content -Path $ReportOutputPath
        Write-Host "Report generated and saved to $ReportOutputPath."

    } catch {
        Write-Error "Error generating report: $_"
    }
}

# Parameterize Paths
param (
    [string]$CurrentStatePath = "C:\Users\bob\Desktop\currentState.json",
    [string]$TargetStatePath = "C:\Users\bob\Desktop\targetState.json",
    [string]$NonCompliantPropertiesPath = "C:\Users\bob\Desktop\nonCompliantOutput.json",
    [string]$CompliantPropertiesPath = "C:\Users\bob\Desktop\compliantOutput.json",
    [string]$ReportOutputPath = "C:\Users\bob\Desktop\report.json"
)

# Generate the report
Generate-Report -CurrentStatePath $CurrentStatePath -TargetStatePath $TargetStatePath -NonCompliantPropertiesPath $NonCompliantPropertiesPath -CompliantPropertiesPath $CompliantPropertiesPath -ReportOutputPath $ReportOutputPath
