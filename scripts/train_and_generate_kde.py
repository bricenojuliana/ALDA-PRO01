# train_and_generate_kde.py

import pandas as pd
import numpy as np
from sklearn.neighbors import KernelDensity
import pickle
from pathlib import Path

# Configurable parameters
DATA_PATH = Path("coordgen/data/earthquake_data.csv")
OUTPUT_PATH = Path("coordgen/data/synthetic_earthquakes.csv")
KDE_COORD_PATH = Path("coordgen/data/kde_coords.pkl")
KDE_MAG_PATH = Path("coordgen/data/kde_mag.pkl")

# Read CSV and filter columns of interest
df = pd.read_csv(DATA_PATH, usecols=["latitude", "longitude", "mag", "depth"])
df = df.dropna()

# Convert to array for KDE
X = df[["latitude", "longitude", "depth"]].values

# Train KDE
coord_kde = KernelDensity(bandwidth=0.3, kernel='gaussian')
coord_kde.fit(X)

# KDE para magnitud (1D)
mag_kde = KernelDensity(bandwidth=0.1, kernel='gaussian')
mag_kde.fit(df[["mag"]])

# Save the trained model
with open(KDE_COORD_PATH, "wb") as f:
    pickle.dump(coord_kde, f)

with open(KDE_MAG_PATH, "wb") as f:
    pickle.dump(mag_kde, f)
    
    
print("✅ KDE models (coords + mag) trained and saved.")

