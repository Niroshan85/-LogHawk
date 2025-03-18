# LogHawk - Log Monitoring Tool LogHawk 

## Overview
LogHawk is a robust log monitoring tool tailored for security teams to efficiently scan and analyze log files for any suspicious activities. It focuses on identifying issues like failed login attempts, unauthorized access, and critical errors. By utilizing advanced pattern matching and alerting mechanisms, LogHawk not only enhances security visibility but also supports proactive incident response, ensuring that potential threats are detected and addressed swiftly. Its comprehensive features make it an essential asset for maintaining a secure environment.

## Features 🚀
✓ failed login attempts and brute-force attacks.

✓ Monitors for unauthorized access (HTTP 401 errors).

✓ Identifies suspicious script executions.

✓ Recognizes critical errors and unusual traffic spikes.

✓ Sends real-time SMS alerts via Twilio when threats are detected.

✓ Supports automated monitoring via cron jobs.

## Installation💻
### Prerequisites
Ensure you have Python 3 installed. You can install it using:
```bash
sudo apt-get install python3
```
You also need to install required Python dependencies:
twilio for SMS Alerts 🚨
```bash
pip install twilio
```
## Usage 🛠️
Run LogHawk with the following command:
```bash
python3 loghawk.py /path/to/logfile.log
```
If no log file is specified, LogHawk defaults to scanning:
```
/home/student/Desktop/logs/logs.txt
```

### Example Output
```
Suspicious Activity Detected:
[Unauthorized Access (401)] 203.0.113.50 - - [17/Feb/2025:10:15:33 +0000] "GET /admin HTTP/1.1" 401 123
[Critical Error] Feb 17 10:17:20 server1 app[6789]: CRITICAL: Unauthorized API access attempt from 192.168.1.50
[Failed Login] Feb 17 10:15:14 server1 sshd[2143]: Failed password for invalid user admin from 192.168.1.15 port 54321 ssh2
[Failed Login] Feb 17 10:30:47 server1 sshd[2143]: Failed password for root from 203.0.113.42 port 3390 ssh2
[ALERT] IP 203.0.113.50 made multiple failed attempts (401) within 2.0 seconds.
[ALERT] IP 203.0.113.50 made multiple failed attempts (401) within 2.0 seconds.
```
### **SMS Alert **
![image](https://github.com/user-attachments/assets/331bdee4-3134-4337-918c-8bddcacd6cb3)


## Automating LogHawk with Cron
In the cron table, you'll define when to run the LogHawk script. For example, to run the script every hour, add the following line:
Use the crontab command to open the cron table for editing.
```bash
crontab -e
```
```bash
0 * * * * /path/to/python /path/to/loghawk.py >> /path/to/loghawk.log 2>&1
```
To verify that the cron job was added successfully, you can list your cron jobs:
```bash
crontab -l
```

## Twilio SMS Alerts ‼️
To receive real-time alerts via SMS, configure your Twilio credentials in `loghawk.py`:
```python
ACCOUNT_SID = 'your_account_sid'
AUTH_TOKEN = 'your_auth_token'
FROM_PHONE = 'your_twilio_phone_number'
TO_PHONE = 'recipient_phone_number'
```
**Disclaimer⚠️**  
This project is developed for **educational purposes only**. It is intended to demonstrate concepts and tools related to cybersecurity and log monitoring.
