def classify_command(command: str):
    command = command.lower().strip()

    rules = [
        ("wget", "MALWARE_DOWNLOAD", "CRITICAL", "T1105"),
        ("curl", "MALWARE_DOWNLOAD", "CRITICAL", "T1105"),
        ("chmod +x", "EXECUTION_PREP", "HIGH", "T1222"),
        ("./", "EXECUTION", "HIGH", "T1059"),
        ("uname", "RECON", "LOW", "T1082"),
        ("whoami", "RECON", "LOW", "T1082"),
        ("id", "RECON", "LOW", "T1082"),
    ]

    for keyword, attack, severity, mitre in rules:
        if keyword in command:
            return {
                "attack_type": attack,
                "severity": severity,
                "mitre": mitre
            }

    return {
        "attack_type": "UNKNOWN",
        "severity": "INFO",
        "mitre": "N/A"
    }
