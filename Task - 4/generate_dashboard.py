import csv
import collections

def generate_dashboard():
    alerts = []
    
    # Read the simulated Snort alert log
    with open('snort_alerts.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            alerts.append(row)
            
    # Count the occurrences of each alert type for the chart
    alert_counts = collections.Counter(alert['Alert_Message'] for alert in alerts)
    labels = list(alert_counts.keys())
    data = list(alert_counts.values())

    # Generate HTML content with embedded Chart.js and CSS
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NIDS Alert Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 20px; }}
            .container {{ max-width: 1000px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .chart-container {{ width: 70%; margin: 20px auto; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #3498db; color: white; }}
            tr:hover {{ background-color: #f5f5f5; }}
            .badge {{ padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 0.9em; }}
            .tcp {{ background-color: #ffeaa7; color: #d35400; }}
            .icmp {{ background-color: #fab1a0; color: #c0392b; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ Network Intrusion Detection Dashboard</h1>
            
            <div class="chart-container">
                <canvas id="alertChart"></canvas>
            </div>

            <h2>Recent Alerts Log</h2>
            <table>
                <tr><th>Timestamp</th><th>Alert Signature</th><th>Source IP</th><th>Destination IP</th><th>Protocol</th></tr>
                {"".join(f"<tr><td>{a['Timestamp']}</td><td>{a['Alert_Message']}</td><td>{a['Source_IP']}</td><td>{a['Destination_IP']}</td><td><span class='badge {a['Protocol'].lower()}'>{a['Protocol']}</span></td></tr>" for a in alerts)}
            </table>
        </div>

        <script>
            const ctx = document.getElementById('alertChart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: {labels},
                    datasets: [{{
                        label: 'Number of Alerts Detected',
                        data: {data},
                        backgroundColor: ['#e74c3c', '#f1c40f', '#e67e22', '#3498db'],
                        borderWidth: 1
                    }}]
                }},
                options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true, ticks: {{ stepSize: 1 }} }} }} }}
            }});
        </script>
    </body>
    </html>
    """

    # Save the generated dashboard
    with open('dashboard.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
    print("[+] Dashboard successfully generated: dashboard.html")

if __name__ == "__main__":
    generate_dashboard()