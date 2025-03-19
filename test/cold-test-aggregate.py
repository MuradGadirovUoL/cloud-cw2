import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def visualize_jmeter_aggregate(
    azure_csv="azure_aggregate.csv",
    knative_csv="knative_aggregate.csv"
):
    """
    Reads two JMeter Aggregate Report CSV files (one for Azure, one for Knative),
    and visualizes key metrics. If there's only 1 sample per platform (typical for
    a single cold start test), it displays a simple single-bar comparison.
    Otherwise, it shows a grouped bar chart with Min, Average, Median, 90% Line,
    95% Line, and Max.
    """

    # Columns in JMeter Aggregate CSV (typical):
    # Label,# Samples,Average,Median,90% Line,95% Line,99% Line,Min,Max,Error %,Throughput,Received KB/sec,Sent KB/sec

    # Read the CSV files
    df_azure = pd.read_csv(azure_csv)
    df_knative = pd.read_csv(knative_csv)

    # Filter out the "TOTAL" row if present
    df_azure = df_azure[df_azure["Label"] != "TOTAL"]
    df_knative = df_knative[df_knative["Label"] != "TOTAL"]

    # Extract the single row for each platform
    azure_row = df_azure.iloc[0]
    knative_row = df_knative.iloc[0]

    # Identify labels
    azure_label = azure_row["Label"]
    knative_label = knative_row["Label"]

    # Get the number of samples for each
    azure_samples = float(azure_row["# Samples"])
    knative_samples = float(knative_row["# Samples"])

    # Convert key columns to float
    azure_min = float(azure_row["Min"])
    azure_avg = float(azure_row["Average"])
    azure_median = float(azure_row["Median"])
    azure_p90 = float(azure_row["90% Line"])
    azure_p95 = float(azure_row["95% Line"])
    azure_max = float(azure_row["Max"])

    knative_min = float(knative_row["Min"])
    knative_avg = float(knative_row["Average"])
    knative_median = float(knative_row["Median"])
    knative_p90 = float(knative_row["90% Line"])
    knative_p95 = float(knative_row["95% Line"])
    knative_max = float(knative_row["Max"])

    # Check if each platform has exactly 1 sample (typical for a single cold start test)
    if azure_samples == 1 and knative_samples == 1:
        # For single-sample cold start: min=avg=median=90%=95%=max.
        # We'll just plot one bar per platform with that single time.
        azure_cold_time = azure_avg  # could be min or max, they're the same
        knative_cold_time = knative_avg

        platforms = [azure_label, knative_label]
        values = [azure_cold_time, knative_cold_time]

        plt.figure(figsize=(6, 5))
        bars = plt.bar(platforms, values, color=["cornflowerblue", "lightgreen"])
        plt.ylabel("Cold Start Duration (ms)")
        plt.title("Azure vs Knative (Cold Start) - Single Request")

        # Attach numeric labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height:.0f}',
                         xy=(bar.get_x() + bar.get_width()/2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom')
        plt.tight_layout()
        plt.show()

    else:
        # If there's more than 1 sample, produce the grouped bar chart
        metrics_labels = ["Min", "Average", "Median", "90% Line", "95% Line", "Max"]
        azure_values = [azure_min, azure_avg, azure_median, azure_p90, azure_p95, azure_max]
        knative_values = [knative_min, knative_avg, knative_median, knative_p90, knative_p95, knative_max]

        x = np.arange(len(metrics_labels))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))
        bars_azure = ax.bar(x - width/2, azure_values, width, label=azure_label, color="cornflowerblue")
        bars_knative = ax.bar(x + width/2, knative_values, width, label=knative_label, color="lightgreen")

        ax.set_ylabel("Response Time (ms)")
        ax.set_title("Azure vs Knative - Single Request")
        ax.set_xticks(x)
        ax.set_xticklabels(metrics_labels)
        ax.legend()

        # Function to label bars with numeric values
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{height:.0f}',
                            xy=(rect.get_x() + rect.get_width()/2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(bars_azure)
        autolabel(bars_knative)

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    visualize_jmeter_aggregate(
        azure_csv="azure-cold-start-aggregate.csv",
        knative_csv="knative-cold-start-aggregate.csv"
    )
