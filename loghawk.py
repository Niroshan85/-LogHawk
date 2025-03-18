import re
import argparse
import os
from collections import defaultdict
from datetime import datetime
from twilio.rest import Client

# Default log file path
DEFAULT_LOG_FILE = "/home/student/Desktop/logs/logs.txt"

# Twilio credentials (replace with your own)
ACCOUNT_SID = 'SID'
AUTH_TOKEN = 'TOKEN'
FROM_PHONE = ' Phone number Twilio'  # Twilio phone number
TO_PHONE = 'Recipient number'  # The phone number to receive the alert

def send_sms_alert(message):
    """Send an SMS alert using Twilio."""
    try:
        # Initialize the Twilio client
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        
        # Send the SMS
        message = client.messages.create(
            body=message,  # The message content
            from_=FROM_PHONE,  # Your Twilio number
            to=TO_PHONE  # Recipient's phone number
        )
        
        print(f"Message sent: {message.sid}")
    
    except Exception as e:
        print(f"Error sending SMS: {e}")

def parse_log_file(log_file):
    """Scan log file for suspicious activity."""
    if not os.path.exists(log_file):
        print(f"Error: {log_file} not found.")
        return
    
    with open(log_file, 'r') as file:
        logs = file.readlines()
    
    alerts = []
    
    # Define suspicious patterns
    patterns = {
        "Failed Login": r"Failed password for .* from (\d+\.\d+\.\d+\.\d+) port",
        "Traffic Spike": r"Too many connections from (\d+\.\d+\.\d+\.\d+)",
        "Critical Error": r"CRITICAL: .*",
        "Suspicious Script": r"/tmp/.*\.sh",
        "Unauthorized Access (401)": r"(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] \"GET (.*?) HTTP/1.1\" 401"
    }
    
    # Track repeated 401 attempts by IP with timestamps
    ip_attempts = defaultdict(list)  # stores IP and corresponding timestamps
    
    for line in logs:
        for alert_type, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                if alert_type == "Unauthorized Access (401)":
                    ip_address = match.group(1)
                    timestamp_str = match.group(2).strip()
                    timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")  # Adjusted format to include timezone
                    
                    ip_attempts[ip_address].append(timestamp)
                
                alerts.append(f"[{alert_type}] {line.strip()}")
    
    # Check for multiple 401 attempts within 5 seconds
    for ip, timestamps in ip_attempts.items():
        timestamps.sort()  # Ensure timestamps are sorted
        for i in range(len(timestamps) - 1):
            time_diff = (timestamps[i + 1] - timestamps[i]).total_seconds()
            if time_diff <= 5:  # 5 seconds threshold
                alert_message = f"[ALERT] IP {ip} made multiple failed attempts (401) within {time_diff} seconds."
                alerts.append(alert_message)
                
                # Send an SMS alert for this suspicious activity
                send_sms_alert(alert_message)
    
    if alerts:
        print("\nSuspicious Activity Detected:")
        for alert in alerts:
            print(alert)
    else:
        print("No suspicious activity found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LogHawk: A Log Monitoring Tool")
    parser.add_argument("log_file", nargs="?", default=DEFAULT_LOG_FILE, help="Path to the log file to scan")
    args = parser.parse_args()
    
    parse_log_file(args.log_file)
