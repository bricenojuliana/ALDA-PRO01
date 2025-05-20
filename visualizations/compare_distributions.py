import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

sns.set_theme(style="whitegrid")

def load_data():
    data_dir = Path(__file__).parent.parent / 'coordgen' / 'data'
    real_path = data_dir / 'earthquake_data.csv'          # real data
    synth_path = data_dir / 'synthetic_earthquakes.csv'   # synthetic data

    real_df = pd.read_csv(real_path, parse_dates=['time'], low_memory=False)
    synth_df = pd.read_csv(synth_path, parse_dates=['date'], low_memory=False)
    return real_df, synth_df

def plot_lat_lon(real_df, synth_df, save_dir):
    plt.figure(figsize=(10,6))
    plt.scatter(real_df['longitude'], real_df['latitude'], alpha=0.3, label='Real', s=10)
    plt.scatter(synth_df['longitude'], synth_df['latitude'], alpha=0.3, label='Synthetic', s=10)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Coordinate Distribution (Real vs Synthetic)')
    plt.legend()
    save_path = save_dir / 'lat_lon_comparison.png'
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def plot_histogram_compare(real_df, synth_df, column, save_dir, bins=30):
    plt.figure(figsize=(8,5))
    sns.histplot(real_df[column], color='blue', label='Real', kde=True, stat='density', bins=bins)
    sns.histplot(synth_df[column], color='orange', label='Synthetic', kde=True, stat='density', bins=bins)
    plt.title(f'Distribution Comparison: {column}')
    plt.legend()
    save_path = save_dir / f'{column}_distribution_comparison.png'
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def main():
    real_df, synth_df = load_data()

    # Sampling if there is too much data to make plots faster
    if len(real_df) > 5000:
        real_df = real_df.sample(5000, random_state=42)
    if len(synth_df) > 5000:
        synth_df = synth_df.sample(5000, random_state=42)

    save_dir = Path(__file__).parent / 'plots'
    save_dir.mkdir(exist_ok=True)

    plot_lat_lon(real_df, synth_df, save_dir)
    plot_histogram_compare(real_df, synth_df, 'mag', save_dir)
    plot_histogram_compare(real_df, synth_df, 'depth', save_dir)
    
    print(f"Plots saved in {save_dir.resolve()}")


if __name__ == "__main__":
    main()
