import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from .config import ROW_COUNT, RANDOM_SEED

np.random.seed(RANDOM_SEED)

coord_kde_path = Path(__file__).parent / 'data' / 'kde_coords.pkl'
mag_kde_path = Path(__file__).parent / 'data' / 'kde_mag.pkl'

with open(coord_kde_path, 'rb') as f:
    coord_kde = pickle.load(f)

with open(mag_kde_path, 'rb') as f:
    mag_kde = pickle.load(f)

def assign_plate(lat, lon):
    if lat <= -60:
        return 'Antarctic'
    elif lon <= -130 and lat >= -60 and lat <= 60:
        return 'Pacific'
    elif lat >= 30 and lon >= -30 and lon <= 150:
        return 'Eurasian'
    elif lat >= 0 and lat < 60 and lon >= -170 and lon <= -50:
        return 'North American'
    elif lat < 0 and lat > -60 and lon >= -90 and lon <= -30:
        return 'South American'
    elif lat >= -45 and lat <= 0 and lon >= 100 and lon <= 180:
        return 'Indo-Australian'
    else:
        return 'Other'


def alert_level(mag):
    if mag < 4.0:
        return 'Green'
    elif mag < 5.5:
        return 'Yellow'
    elif mag < 6.5:
        return 'Orange'
    else:
        return 'Red'

def assign_region(lat):
    if lat < -30:
        return 'Oceania'
    elif lat < 0:
        return 'South America'
    elif lat < 30:
        return 'Africa'
    elif lat < 60:
        return 'Asia'
    else:
        return 'Europe'

def generate_event_ids(n):
    return ['EVT{:07d}'.format(i) for i in range(1, n+1)]

def generate_random_dates(n, start='1975-01-01', end='2025-01-01'):
    start = pd.Timestamp(start)
    end = pd.Timestamp(end)
    return pd.to_datetime(
        np.random.randint(start.value//10**9, end.value//10**9, n), unit='s'
    )

def calculate_intensity(mags, depths, n):
    return np.clip(
        (mags - depths / 100) + np.random.normal(0, 0.5, n),
        1,
        12
    ).round(1)

def estimate_cost(mags, intensities, n):
    base_cost = (mags ** 3) * (intensities / 10) * 10000
    noise = np.random.normal(0, 10000, n)
    return np.round(np.clip(base_cost + noise, 0, None), 2)

def estimate_impacts(intensities, mags, n):
    casualties = np.random.poisson(lam=(intensities * mags) / 10)
    injuries = np.random.poisson(lam=(intensities * 2))
    displaced = np.random.poisson(lam=(intensities * 5))
    return casualties, injuries, displaced

def generate_synthetic_data(n=ROW_COUNT):
    coords = coord_kde.sample(n)
    df = pd.DataFrame(coords, columns=["latitude", "longitude", "depth"])
    mags = mag_kde.sample(n).flatten()
    df['mag'] = mags
    df['event_id'] = generate_event_ids(n)
    df['date'] = generate_random_dates(n)
    df['tectonic_plate'] = [assign_plate(lat, lon) for lat, lon in zip(df['latitude'], df['longitude'])]
    df['alert_level'] = df['mag'].apply(alert_level)
    df['intensity_level'] = calculate_intensity(df['mag'], df['depth'], n)
    df['estimated_cost'] = estimate_cost(df['mag'], df['intensity_level'], n)
    casualties, injuries, displaced = estimate_impacts(df['intensity_level'], df['mag'], n)
    df['casualties'] = casualties
    df['injuries'] = injuries
    df['displaced'] = displaced
    df['region'] = df['latitude'].apply(assign_region)
    return df

if __name__ == "__main__":
    df = generate_synthetic_data()
    output_path = Path(__file__).parent / "data" / "synthetic_earthquakes.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} synthetic earthquake events to {output_path}")
