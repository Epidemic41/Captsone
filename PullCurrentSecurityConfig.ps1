#pull current security configuration and store for future comparision with target configuration to measure compliance

#output file
$currentStatePath = "C:\Users\bob\Desktop\currentState.json"

# Get Windows Firewall profile statuses
$firewallProfiles = Get-NetFirewallProfile

$firewallDomainStatus = $firewallProfiles | Where-Object { $_.Name -eq 'Domain' } | Select-Object -ExpandProperty Enabled
$firewallPrivateStatus = $firewallProfiles | Where-Object { $_.Name -eq 'Private' } | Select-Object -ExpandProperty Enabled
$firewallPublicStatus = $firewallProfiles | Where-Object { $_.Name -eq 'Public' } | Select-Object -ExpandProperty Enabled

# Get UAC status
$uacStatus = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLUA").EnableLUA

#Check if Windows Update service is running
    # Specify the name of the service (e.g., Windows Update service)
    $serviceName = "wuauserv"

    # Get the service information
    $service = Get-Service -Name wuauserv

    # Check the startup type
    if ($service.StartType -eq "Manual") {
        # Check if it's set to trigger start
        $triggerStartRegistryValue = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\$serviceName" -Name "TriggerStart"

        if ($triggerStartRegistryValue) {
            $windowsUpdateStatus = "Manual (Trigger Start)"
        } else {
            $windowsUpdateStatus = "Manual"
        }
    } elseif ($service.StartType -eq "Automatic") {
        $windowsUpdateStatus = "Automatic"
    }


# Get Windows Defender status 
$windowsDefenderStatus = Get-MpComputerStatus
# retreive desired configuration from cmdlet
$ComputerState = $windowsDefenderStatus.ComputerState
$AMServiceEnabled = $windowsDefenderStatus.AMServiceEnabled
$AntispywareEnabled = $windowsDefenderStatus.AntispywareEnabled
$AntivirusEnabled = $windowsDefenderStatus.AntivirusEnabled
$RealTimeProtectionEnabled = $windowsDefenderStatus.RealTimeProtectionEnabled
$BehaviorMonitorEnabled = $windowsDefenderStatus.BehaviorMonitorEnabled

# Create a custom PowerShell object to store the information
$systemInfo = [PSCustomObject]@{
    firewallDomainStatus = $firewallDomainStatus 
    firewallPrivateStatus = $firewallPrivateStatus 
    firewallPublicStatus = $firewallPublicStatus

    <# compliant = 1
    1=enabled 0=disabled #>
    
    UACStatus = $uacStatus
    <# compliant = 1 or 2 
    0 - UAC is turned off ("Never Notify")
    1 - Default UAC setting ("Notify me only when apps try to make changes")
    2 - UAC is turned on with the highest level of notification ("Always notify me")
    #>

    WindowsUpdateStatus = $windowsUpdateStatus
    # compliant = "Manual (Trigger Start)" or "Automatic"

    AMServiceEnabled = $windowsDefenderStatus.AMServiceEnabled
        # compliant = true

    AntispywareEnabled = $windowsDefenderStatus.AntispywareEnabled
        # compliant = true

    AntivirusEnabled = $windowsDefenderStatus.AntivirusEnabled
        # compliant = true

    RealTimeProtectionEnabled = $windowsDefenderStatus.RealTimeProtectionEnabled
        # compliant = true
        
    BehaviorMonitorEnabled = $windowsDefenderStatus.BehaviorMonitorEnabled
        # compliant = true

    ComputerState = $windowsDefenderStatus.ComputerState

   <#
        compliant = 0, 2, or 5. others are eithers transional phases or IOCs

    0 - "NoStatus`:
        This state indicates that no specific status information is available for Windows Defender at the moment.

    1 - "Disabled`:
        Indicates that Windows Defender is currently disabled. This means it is not actively providing real-time protection or performing scans.

    2 - "Enabled`:
        This state indicates that Windows Defender is enabled and actively protecting the system against threats.

    3 - "NotMonitored`:
        Indicates that Windows Defender is not actively being monitored. This can occur if there are issues with the monitoring service.

    4 - "OutOfDate`:
        This state signifies that the antivirus definitions are out of date. It's important to regularly update definitions to ensure effective protection.

    5 - "UpToDate`:
        Indicates that the antivirus definitions are current and up to date.

    6 - "NoResponse`:
        This state suggests that Windows Defender is not responding. This might indicate a problem with the service.

    7 - "ServiceStarting`:
        Indicates that the Windows Defender service is in the process of starting up.

    8 - "ServiceStopping`:
        This state indicates that the Windows Defender service is in the process of shutting down.

    9 - "NeedsFullScan`:
        Indicates that a full system scan is recommended or needed.

    10 - "ThreatDetected`:
        This state means that Windows Defender has detected one or more threats on the system.
    #>

    
}

# Convert the object to JSON and save it to a file
$systemInfo | ConvertTo-Json | Set-Content -Path $currentStatePath
