import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def visualize_jmeter_aggregate(
    azure_csv="azure_aggregate.csv",
    knative_csv="knative_aggregate.csv"
):
    """
    Reads two JMeter Aggregate Report CSV files (one for Azure, one for Knative),
    and visualizes the key metrics: Min, Average, Median, 90% Line, 95% Line, and Max
    in a grouped bar chart.
    """

    # Columns in JMeter Aggregate CSV (typical):
    # Label,# Samples,Average,Median,90% Line,95% Line,99% Line,Min,Max,Error %,Throughput,Received KB/sec,Sent KB/sec

    # Read the CSV files
    df_azure = pd.read_csv(azure_csv)
    df_knative = pd.read_csv(knative_csv)

    # Filter out the "TOTAL" row if present
    df_azure = df_azure[df_azure["Label"] != "TOTAL"]
    df_knative = df_knative[df_knative["Label"] != "TOTAL"]

    # Extract the single row for each
    azure_row = df_azure.iloc[0]
    knative_row = df_knative.iloc[0]

    # Identify labels
    azure_label = azure_row["Label"]
    knative_label = knative_row["Label"]

    # Extract the key metrics
    # Convert them to float if needed (JMeter outputs can be strings)
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

    # Define metrics in order
    metrics_labels = ["Min", "Average", "Median", "90% Line", "95% Line", "Max"]
    azure_values = [azure_min, azure_avg, azure_median, azure_p90, azure_p95, azure_max]
    knative_values = [knative_min, knative_avg, knative_median, knative_p90, knative_p95, knative_max]

    # Create a grouped bar chart
    x = np.arange(len(metrics_labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars_azure = ax.bar(x - width/2, azure_values, width, label=azure_label, color="cornflowerblue")
    bars_knative = ax.bar(x + width/2, knative_values, width, label=knative_label, color="lightgreen")

    ax.set_ylabel("Response Time (ms)")
    ax.set_title("Azure vs Knative (Warm Tests) - Multiple Request")
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
    # Example usage (adjust filenames as needed)
    visualize_jmeter_aggregate(
        azure_csv="azure-warm-start-load-aggregate.csv",
        knative_csv="knative-warm-start-load-aggregate.csv"
    )
