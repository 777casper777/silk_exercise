import matplotlib.pyplot as plt
from pymongo import MongoClient
from collections import Counter
import os
import textwrap

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
client = MongoClient(MONGO_URL)
collection = client["host_db"]["hosts"]

def shorten_os_name(os_name: str) -> str:
    """Trims or simplifies long OS names"""
    if not os_name:
        return "Unknown"
    if "Windows" in os_name:
        return "Windows Server"
    if "Amazon" in os_name:
        return "Amazon Linux 2"
    return os_name.strip()

def main():
    hosts = list(collection.find())
    if not hosts:
        print("⚠ No data found in the 'hosts' collection.")
        return

    os_counter = Counter(shorten_os_name(h.get("os")) for h in hosts)
    if not os_counter:
        print("⚠ No valid 'os' data to display.")
        return

    # Wrap long OS names
    labels = [textwrap.fill(label, width=20) for label in os_counter.keys()]
    values = list(os_counter.values())

    # Plot the chart
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color="skyblue")
    plt.title("OS Distribution of Hosts")
    plt.xlabel("Operating System")
    plt.ylabel("Number of Hosts")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    output_path = "visualisations/screenshots/os_distribution.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    print(f"✅ Chart saved to: {output_path}")

if __name__ == "__main__":
    main()
