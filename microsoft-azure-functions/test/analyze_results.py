import json
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import matplotlib.dates as mdates

def analyze_results(json_file="results.json"):
    timestamps = []
    latencies = []

    with open(json_file, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if "metric" in entry and entry["metric"] == "http_req_duration":
                    data_point = entry.get("data", {})
                    timestamp = data_point.get("time")
                    latency = data_point.get("value")

                    if timestamp and latency is not None:
                        timestamps.append(timestamp)
                        latencies.append(float(latency))
            except json.JSONDecodeError:
                print("Skipping invalid JSON line.")

    # Convert to DataFrame
    df = pd.DataFrame({"Timestamp": timestamps, "Response Time (ms)": latencies})

    if df.empty:
        print("No valid HTTP request data found. Check your JSON file.")
        return

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    cold_start_latency = df.iloc[0]["Response Time (ms)"]
    warm_start_latency = df["Response Time (ms)"].mean()

    print(f"Cold Start Response Time: {cold_start_latency:.2f} ms")
    print(f"Average Warm Start Response Time: {warm_start_latency:.2f} ms")

    plt.figure(figsize=(10, 5))
    plt.plot(df["Timestamp"], df["Response Time (ms)"], label="Response Time (ms)", marker="o")

    plt.axhline(y=cold_start_latency, color='r', linestyle='--', label="Cold Start")
    plt.axhline(y=warm_start_latency, color='g', linestyle='--', label="Warm Start Avg")

    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()  # Auto-rotate date labels

    plt.xlabel("Time")
    plt.ylabel("Response Time (ms)")
    plt.title("Cold vs Warm Start Response Time (Microsoft Azure Functions)")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze K6 Load Test Results")
    parser.add_argument("json_file", type=str, nargs="?", default="results.json",
                        help="Path to K6 JSON result file")
    args = parser.parse_args()
    analyze_results(args.json_file)
