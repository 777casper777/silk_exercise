import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime, timedelta
import os

# Используем переменную окружения или дефолтный адрес (для Docker)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
client = MongoClient(MONGO_URL)
collection = client["host_db"]["hosts"]

def main():
    now = datetime.utcnow()
    threshold = now - timedelta(days=30)

    old, recent, total = 0, 0, 0

    for h in collection.find():
        last_seen = h.get("last_seen")
        if last_seen:
            try:
                if isinstance(last_seen, str):
                    dt = datetime.fromisoformat(last_seen.replace("Z", "+00:00"))
                else:
                    dt = last_seen  # уже datetime

                if dt < threshold:
                    old += 1
                else:
                    recent += 1
                total += 1
            except Exception:
                pass

    print(f"🧾 Total valid hosts with 'last_seen': {total}")
    print(f"Old hosts: {old}, Recent hosts: {recent}")

    if total == 0:
        print("⚠ No data to display: all hosts are missing or have invalid 'last_seen'.")
        return

    labels = ["Old Hosts (>30d)", "Recent Hosts"]
    values = [old, recent]

    plt.figure(figsize=(6, 5))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Host Age Distribution")

    output_path = "visualisations/screenshots/host_age_chart.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    print(f"✅ Chart saved to: {output_path}")

if __name__ == "__main__":
    main()
