import requests
import random
import time
from datetime import datetime

BACKEND_URL = "https://organ-c-codefest-hackathon.onrender.com/api/v1/iot/"

def generate_random_record():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "store": random.randint(1, 45),
        "dept": random.randint(1, 98),
        "Weekly_Sales": round(random.uniform(2000, 60000), 2),
        "Temperature": round(random.uniform(10, 38), 2),
        "Fuel_Price": round(random.uniform(2.0, 4.5), 2),
        "CPI": round(random.uniform(150, 260), 2),
        "Unemployment": round(random.uniform(3.0, 11.0), 2),
        "IsHoliday": random.choice([0, 1])
    }

def send_record():
    data = generate_random_record()
    print("Sending data:", data)

    try:
        r = requests.post(BACKEND_URL, json=data)
        print("Response:", r.status_code, r.text)
    except Exception as e:
        print("Failed:", e)

if __name__ == "__main__":
    print("IoT Simulator running... (Every 10 minutes)")
    while True:
        send_record()
        time.sleep(600)
