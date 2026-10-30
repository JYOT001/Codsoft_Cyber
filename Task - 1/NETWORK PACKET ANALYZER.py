from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw

def packet_callback(packet):
    """
    Callback function executed for each captured packet.
    Extracts and formats IP, Protocol, and Payload data.
    """
    # Verify the packet has an IP layer before processing
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto_num = packet[IP].proto
        
        # Identify Protocol Type
        if proto_num == 6:
            protocol = "TCP"
        elif proto_num == 17:
            protocol = "UDP"
        elif proto_num == 1:
            protocol = "ICMP"
        else:
            protocol = f"OTHER ({proto_num})"

        # Extract Packet Data (Payload) if present
        payload_data = "No payload"
        if Raw in packet:
            raw_bytes = packet[Raw].load
            # Attempt to decode as readable text, ignore unreadable binary
            try:
                payload_data = raw_bytes.decode('utf-8', errors='ignore').strip()
                # Truncate long payloads for cleaner terminal output
                if len(payload_data) > 80:
                    payload_data = payload_data[:80] + "..."
            except Exception:
                payload_data = f"<Binary Data: {len(raw_bytes)} bytes>"

        # Print the extracted details in a clear, organized format
        print("-" * 50)
        print(f"Source IP      : {src_ip}")
        print(f"Destination IP : {dst_ip}")
        print(f"Protocol       : {protocol}")
        print(f"Packet Data    : {payload_data}")

def main():
    print("[*] Starting Network Packet Sniffer...")
    print("[*] Listening for traffic... (Press Ctrl+C to stop)")
    
    # Start sniffing. 
    # store=False prevents the application from keeping all packets in memory.
    try:
        sniff(prn=packet_callback, store=False)
    except KeyboardInterrupt:
        print("\n[*] Sniffing stopped by user.")
    except PermissionError:
        print("\n[!] Error: You must run this script as Administrator or root.")

if __name__ == "__main__":
    main()