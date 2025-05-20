# fetch_earthquake_data.py

import requests
import pandas as pd
import io
from time import sleep

BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Base parameters for the query
COMMON_PARAMS = {
    "format": "csv",
    "minmagnitude": 3.0,
    "orderby": "time"
}

def fetch_year(year: int) -> pd.DataFrame:
    """Downloads earthquake data for a specific year."""
    print(f"Fetching data for {year}...")
    params = {
        **COMMON_PARAMS,
        "starttime": f"{year}-01-01",
        "endtime": f"{year + 1}-01-01"
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed for year {year}: {response.status_code}")
    
    df = pd.read_csv(io.StringIO(response.text))
    print(f"  Found {len(df)} earthquakes")
    return df

def main():
    all_data = []
    for year in range(1975, 2025):
        try:
            df_year = fetch_year(year)
            all_data.append(df_year)
        except Exception as e:
            print(e)
        sleep(1)  # USGS recommends avoiding too many requests in a row

    # Concatenate all and save to CSV
    full_df = pd.concat(all_data, ignore_index=True)
    full_df.to_csv("coordgen/data/earthquake_data.csv", index=False)
    print(f"✅ Saved {len(full_df)} total earthquakes to coordgen/data/earthquake_data.csv")

if __name__ == "__main__":
    main()
