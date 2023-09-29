# Function to get the status of each firewall profile
function Get-FirewallProfileStatus {
    $firewallProfiles = Get-NetFirewallProfile
    $status = @{}
    $firewallProfiles | ForEach-Object {
        # Store the status of each profile in the status hashtable
        $status[$_.Name] = $_.Enabled
    }
    return $status
}

# Function to get the status of User Account Control (UAC)
function Get-UACStatus {
    try {
        # Retrieve the UAC status from the registry
        $uac = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLUA").EnableLUA
        return $uac
    } catch {
        Write-Error "Error getting UAC status: $_"
        return $null
    }
}

# Function to get the status of the Windows Update service
function Get-WindowsUpdateStatus {
    param (
        [string]$ServiceName = "wuauserv"
    )

    try {
        $service = Get-Service -Name $ServiceName
        # Determine the status based on the StartType of the service
        switch ($service.StartType) {
            "Manual" { 
                $triggerStartRegistryValue = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\$ServiceName" -Name "TriggerStart"
                if ($triggerStartRegistryValue) { return "Manual (Trigger Start)" } else { return "Manual" }
            }
            "Automatic" { return "Automatic" }
            Default { throw "Unexpected Service StartType: $($service.StartType)" }
        }
    } catch {
        Write-Error "Error getting Windows Update status: $_"
        return $null
    }
}

# Function to get the status of Windows Defender
function Get-WindowsDefenderStatus {
    try {
        # Retrieve the status of Windows Defender
        return Get-MpComputerStatus
    } catch {
        Write-Error "Error getting Windows Defender status: $_"
        return $null
    }
}

# Define the output file path
$currentStatePath = "C:\Users\bob\Desktop\currentState.json"

try {
    # Get the status of firewall profiles
    $firewallStatus = Get-FirewallProfileStatus
    
    # Get the status of UAC
    $uacStatus = Get-UACStatus
    
    # Get the status of the Windows Update service
    $windowsUpdateStatus = Get-WindowsUpdateStatus
    
    # Get the status of Windows Defender
    $windowsDefenderStatus = Get-WindowsDefenderStatus
    
    if ($null -eq $windowsDefenderStatus) { throw "Unable to get Windows Defender status" }
    
    # Store the retrieved information in a custom object
    $systemInfo = [PSCustomObject]@{
        FirewallDomainStatus     = $firewallStatus['Domain']
        FirewallPrivateStatus    = $firewallStatus['Private']
        FirewallPublicStatus     = $firewallStatus['Public']
        UACStatus                = $uacStatus   # 0: Disabled, 1: Default, 2: Always Notify
        WindowsUpdateStatus      = $windowsUpdateStatus # compliant = "Manual (Trigger Start)" or "Automatic"
        AMServiceEnabled         = $windowsDefenderStatus.AMServiceEnabled # compliant = true
        AntispywareEnabled       = $windowsDefenderStatus.AntispywareEnabled # compliant = true
        AntivirusEnabled         = $windowsDefenderStatus.AntivirusEnabled # compliant = true
        RealTimeProtectionEnabled= $windowsDefenderStatus.RealTimeProtectionEnabled # compliant = true
        BehaviorMonitorEnabled   = $windowsDefenderStatus.BehaviorMonitorEnabled # compliant = true
        ComputerState            = $windowsDefenderStatus.ComputerState # compliant = 0, 2, or 5
    }

    # Convert the object to JSON and save it to the defined path
    $systemInfo | ConvertTo-Json | Set-Content -Path $currentStatePath

} catch {
    # Output any errors that occur during execution
    Write-Error "Error occurred: $_"
}
