import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
import contextily as ctx


output_dir = Path(__file__).parent / "plots"
output_dir.mkdir(exist_ok=True)

data_dir = Path(__file__).parent.parent / 'coordgen' / 'data'
df = pd.read_csv(data_dir / 'synthetic_earthquakes.csv')



def save_plot(fig, filename, subfolder=""):
    folder = output_dir / subfolder
    folder.mkdir(parents=True, exist_ok=True)
    fig.savefig(folder / filename, bbox_inches='tight')
    plt.close(fig)  # Close figure to free memory

def plot_magnitude_distribution(df):
    fig, ax = plt.subplots(figsize=(8,5))
    sns.histplot(df['mag'], bins=30, kde=True, color='blue', ax=ax)
    ax.set_title("Earthquake Magnitude Distribution")
    ax.set_xlabel("Magnitude")
    ax.set_ylabel("Frequency")
    ax.grid(True)
    save_plot(fig, "magnitude_distribution.png", subfolder="distributions")

def plot_depth_distribution(df):
    fig, ax = plt.subplots(figsize=(8,5))
    sns.histplot(df['depth'], bins=30, kde=True, color='green', ax=ax)
    ax.set_title("Earthquake Depth Distribution")
    ax.set_xlabel("Depth (km)")
    ax.set_ylabel("Frequency")
    ax.grid(True)
    save_plot(fig, "depth_distribution.png", subfolder="distributions")

def plot_geographic_distribution(df):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(data=df, x='longitude', y='latitude', hue='tectonic_plate', palette='Set2', s=20, ax=ax)
    ax.set_title("Geographic Distribution of Events by Tectonic Plate")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend(title="Tectonic Plate")
    ax.grid(True)
    save_plot(fig, "geographic_distribution.png", subfolder="maps")

def plot_mag_vs_intensity(df):
    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(x='mag', y='intensity_level', data=df, alpha=0.6, ax=ax)
    ax.set_title("Magnitude vs Intensity Level")
    ax.set_xlabel("Magnitude")
    ax.set_ylabel("Intensity Level")
    ax.grid(True)
    save_plot(fig, "mag_vs_intensity.png", subfolder="scatterplots")

def plot_mag_vs_cost(df):
    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(x='mag', y='estimated_cost', data=df, alpha=0.6, ax=ax)
    ax.set_yscale('log')
    ax.set_title("Magnitude vs Estimated Cost (log scale)")
    ax.set_xlabel("Magnitude")
    ax.set_ylabel("Estimated Cost")
    ax.grid(True, which="both", ls="--")
    save_plot(fig, "mag_vs_cost.png", subfolder="scatterplots")

def plot_alert_level_counts(df):
    fig, ax = plt.subplots(figsize=(6,4))
    sns.countplot(x='alert_level', data=df, order=['Green','Yellow','Orange','Red'], palette='coolwarm', ax=ax)
    ax.set_title("Event Count by Alert Level")
    ax.set_xlabel("Alert Level")
    ax.set_ylabel("Number of Events")
    ax.grid(True)
    save_plot(fig, "alert_level_counts.png", subfolder="counts")

def plot_impacts_distribution(df):
    fig, axs = plt.subplots(1,3, figsize=(12,4))
    
    sns.histplot(df['casualties'], bins=30, color='red', kde=False, ax=axs[0])
    axs[0].set_title("Fatalities Distribution")
    axs[0].set_xlabel("Number of Fatalities")
    axs[0].set_ylabel("Frequency")

    sns.histplot(df['injuries'], bins=30, color='orange', kde=False, ax=axs[1])
    axs[1].set_title("Injuries Distribution")
    axs[1].set_xlabel("Number of Injuries")

    sns.histplot(df['displaced'], bins=30, color='purple', kde=False, ax=axs[2])
    axs[2].set_title("Displaced People Distribution")
    axs[2].set_xlabel("Number of Displaced People")

    plt.tight_layout()
    save_plot(fig, "impacts_distribution.png", subfolder="distributions")

def plot_region_distribution(df):
    fig, ax = plt.subplots(figsize=(8,4))
    sns.countplot(x='region', data=df, palette='viridis', ax=ax)
    ax.set_title("Number of Events by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Number of Events")
    ax.grid(True)
    save_plot(fig, "region_distribution.png", subfolder="counts")

if __name__ == "__main__":
    df = pd.read_csv(data_dir / 'synthetic_earthquakes.csv')

    plot_magnitude_distribution(df)
    plot_depth_distribution(df)
    plot_geographic_distribution(df)
    plot_mag_vs_intensity(df)
    plot_mag_vs_cost(df)
    plot_alert_level_counts(df)
    plot_impacts_distribution(df)
    plot_region_distribution(df)

    print(f"✅ Plots saved in folder: {output_dir.resolve()}")


