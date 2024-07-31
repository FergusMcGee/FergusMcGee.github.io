import json
import boto3
import time
import schedule
import datetime
from plyer import notification 
from pathlib import Path

# --- Get Working Directory Using pathlib ---
script_dir = Path(__file__).parent.resolve()
config_path = script_dir / "config.json"


# --- Load Configuration from JSON ---
with open(config_path, "r") as f:
    config = json.load(f)
notifications = config.get("notifications", [])  # Load list of notifications

# --- Notification Function ---

def show_notification(message):
    # toaster = ToastNotifier()
    # toaster.show_toast("Scheduled Notification", message, duration=10)
    notification.notify(
    title="Scheduled Notification",
    message=message,
    app_name="Notify",
    timeout=10
    )

def is_business_hours():
    now = datetime.datetime.now()
    start_time = datetime.datetime.strptime(hours_start, "%H:%M").time()
    end_time = datetime.datetime.strptime(hours_end, "%H:%M").time()
    return now.weekday() < 5 and start_time <= now.time() <= end_time  # Mon-Fri, within start/end times


# --- Schedule Setup ---

for my_notification in notifications:
    message_text = my_notification["message_text"]
    notification_time = my_notification["notification_time"]
    repeat_interval = my_notification.get("repeat_interval", "daily")
    intervals = notification_time.split(':')
    hours_start = config.get("business_hours_start", "09:00")  # Default to 9:00 AM
    hours_end = config.get("business_hours_end", "17:00")      # Default to 5:00 PM
    minutes = int(intervals[0])

    if repeat_interval == "hourly":
        schedule.every().hour.at(f":{minutes:02d}").do(show_notification, message_text)
    elif repeat_interval == "daily":
        schedule.every().day.at(notification_time).do(show_notification, message_text)
    else:
        print(f"Invalid repeat interval '{repeat_interval}' for message '{message_text}'. Please use 'hourly' or 'daily'.")

# --- Main Loop ---

while True:
    if schedule.jobs and is_business_hours():  # Check business hours only if jobs exist
        schedule.run_pending()
    time.sleep(1)
