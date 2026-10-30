# Task 4: Network Intrusion Detection System (NIDS)

This project demonstrates the configuration and deployment of a Network Intrusion Detection System using **Snort**. It includes custom detection rules, simulated alert logs, and an automated Python script that builds an interactive graphical dashboard for threat monitoring.

## 🎯 Objective
To configure a NIDS, create custom rules to detect malicious network activity, and generate a graphical dashboard to visualize network events and alerts.

## 🛠️ Configuration & Custom Rules
The `local.rules` file in this repository contains custom Snort signatures designed to detect:
1. **ICMP Ping Floods:** Potential Denial of Service (DoS) attacks.
2. **FTP Anonymous Logins:** Suspicious unauthorized access attempts.
3. **SSH Brute Force Attacks:** Repeated connection attempts targeting port 22.
4. **Nmap TCP SYN Scans:** Reconnaissance and network mapping behavior.

## 🚨 Alert Monitoring & Response Actions
When Snort is deployed in IPS (Intrusion Prevention System) mode or integrated with a firewall (like `iptables` or `ufw`), the following basic response actions are triggered based on the alerts:
* **Drop:** Automatically drop the offending packets (e.g., dropping ICMP packets during a Ping Flood).
* **Block IP:** Temporarily ban the Source IP using `fail2ban` (e.g., after 5 failed SSH brute force attempts).
* **Log & Alert:** Forward the alert to a SIEM or dashboard for security analyst review.

## 📊 Bonus: Interactive Dashboard Generator
To fulfill the visualization requirement, this repository includes a Python script that parses Snort alert logs and dynamically generates a graphical HTML dashboard.

### How to use the Dashboard:
1. Ensure you have Python installed.
2. Run the generator script:
   ```bash
   python generate_dashboard.py
   ```
3. A file named `dashboard.html` will be generated in the directory.
4. Open `dashboard.html` in any web browser to view the interactive threat charts and log tables.