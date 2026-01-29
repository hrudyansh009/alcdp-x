# detections/rules.py

def classify_command(command: str) -> dict:
    """
    Classify a command into attack type, severity, and MITRE ATT&CK ID.
    """
    cmd = command.strip().lower()

    # Reconnaissance commands
    recon_cmds = ["uname", "whoami", "id", "hostname", "cat /etc/passwd", "ls", "pwd"]
    for rc in recon_cmds:
        if cmd.startswith(rc):
            return {"attack_type": "RECON", "severity": "LOW", "mitre": "T1082"}

    # Credential brute-force or login attempts
    brute_cmds = ["ssh", "telnet", "ftp", "curl", "nc"]
    for bc in brute_cmds:
        if cmd.startswith(bc):
            return {"attack_type": "BRUTE_FORCE", "severity": "HIGH", "mitre": "T1110"}

    # Malware download / suspicious network activity
    download_cmds = ["wget", "curl", "powershell", "fetch"]
    for dc in download_cmds:
        if cmd.startswith(dc):
            return {"attack_type": "MALWARE_DOWNLOAD", "severity": "CRITICAL", "mitre": "T1105"}

    # File manipulation / system modification
    sys_cmds = ["rm", "mv", "cp", "chmod", "chown", "mkdir", "touch"]
    for sc in sys_cmds:
        if cmd.startswith(sc):
            return {"attack_type": "SYSTEM_MANIPULATION", "severity": "MEDIUM", "mitre": "T1059"}

    # Default fallback
    return {"attack_type": "UNKNOWN", "severity": "INFO", "mitre": "N/A"}
