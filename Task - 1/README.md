# Task 1: Network Packet Analyzer

A Python-based network packet sniffer built for the CodSoft Cyber Security internship. Using the `scapy` library, this tool monitors network interfaces and extracts key packet details including Source IP, Destination IP, Protocol (TCP/UDP/ICMP), and payload data.

## Prerequisites

- **Python 3.x**
- **Npcap**: Required for Windows users to capture raw packets (included with Wireshark, or download from [npcap.com](https://npcap.com/)). Linux users require `libpcap`.
- **Elevated Privileges**: The script must be run as an Administrator (Windows) or root (Linux/macOS).

## Installation & Setup

1. Clone the main repository:
   ```bash
   git clone https://github.com/JYOT001/Codsoft_Cyber
   ```
2. Navigate to the Task 1 directory:
   ```bash
   cd Codsoft_Cyber/"Task - 1"
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Open your terminal as an Administrator inside the `Task - 1` folder and run:

**Windows:**
```powershell
python "NETWORK PACKET ANALYZER.py"
```

**Linux / macOS:**
```bash
sudo python3 "NETWORK PACKET ANALYZER.py"
```

To stop capturing packets, press `Ctrl + C`.

## Disclaimer
This tool is built for educational purposes and network troubleshooting. Do not use this application to monitor traffic on networks you do not own or do not have explicit authorization to inspect.