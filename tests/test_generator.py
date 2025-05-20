import pytest
import numpy as np
import pandas as pd
from coordgen.generator import (
    assign_plate, alert_level, assign_region,
    calculate_intensity, estimate_cost, estimate_impacts,
    generate_synthetic_data
)

def test_assign_plate():
    assert assign_plate(-70, 0) == 'Antarctic'
    assert assign_plate(45, 60) == 'Eurasian'
    assert assign_plate(20, -140) == 'Pacific'
    assert assign_plate(40, -100) == 'North American'
    assert assign_plate(-20, -60) == 'South American'
    assert assign_plate(-30, 120) == 'Indo-Australian'
    assert assign_plate(0, 0) == 'Other'

def test_alert_level():
    assert alert_level(3.5) == 'Green'
    assert alert_level(4.5) == 'Yellow'
    assert alert_level(6.0) == 'Orange'
    assert alert_level(7.0) == 'Red'

def test_assign_region():
    assert assign_region(-45) == 'Oceania'
    assert assign_region(-15) == 'South America'
    assert assign_region(15) == 'Africa'
    assert assign_region(45) == 'Asia'
    assert assign_region(65) == 'Europe'

def test_calculate_intensity():
    mags = np.array([5.0, 6.0, 7.0])
    depths = np.array([10, 50, 100])
    result = calculate_intensity(mags, depths, 3)
    assert len(result) == 3
    assert np.all(result >= 1)
    assert np.all(result <= 12)

def test_estimate_cost():
    mags = np.array([4.0, 5.0, 6.0])
    intensities = np.array([3.0, 6.0, 9.0])
    result = estimate_cost(mags, intensities, 3)
    assert len(result) == 3
    assert np.all(result >= 0)

def test_estimate_impacts():
    mags = np.array([5.0, 6.0, 7.0])
    intensities = np.array([4.0, 6.0, 8.0])
    casualties, injuries, displaced = estimate_impacts(intensities, mags, 3)
    assert len(casualties) == len(injuries) == len(displaced) == 3
    assert all(x >= 0 for x in casualties)
    assert all(x >= 0 for x in injuries)
    assert all(x >= 0 for x in displaced)

def test_generate_synthetic_data():
    df = generate_synthetic_data(n=100)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 100
    required_columns = [
        'event_id', 'latitude', 'longitude', 'depth', 'mag',
        'date', 'tectonic_plate', 'alert_level', 'intensity_level',
        'estimated_cost', 'casualties', 'injuries', 'displaced', 'region'
    ]
    for col in required_columns:
        assert col in df.columns
