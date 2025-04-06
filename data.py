import pandas as pd
import numpy as np
from datetime import datetime

# Constants and thresholds
sensor_threshold_smoke = 100  
sensor_threshold_co = 50     
brightness_threshold = 300   
confidence_threshold = 0.8  
frp_threshold = 200         

# Helper function to generate realistic sensor data
def generate_sensor_data():
    smoke_ppm = np.random.uniform(0, 150)  
    co_ppm = np.random.uniform(0, 100)    
    return smoke_ppm, co_ppm

# Helper function to generate satellite data
def generate_satellite_data():
    brightness = np.random.uniform(0, 500) 
    confidence = np.random.uniform(0, 1)    
    frp = np.random.uniform(0, 300)         
    daynight = np.random.choice(['Day', 'Night'])
    return brightness, confidence, frp, daynight

# Helper function to determine if fire is detected (labeling function)
def label_fire_detected(smoke_ppm, co_ppm, satellite_data=None):
    if satellite_data is not None:
        brightness, confidence, frp, _ = satellite_data
        if brightness > brightness_threshold and confidence > confidence_threshold and frp > frp_threshold:
            return 1  # Fire confirmed by satellite data
        else:
            return 0  # No fire detected by satellite data
    
    # Use sensor data alone if no satellite data is available
    if smoke_ppm > sensor_threshold_smoke or co_ppm > sensor_threshold_co:
        return 1  # Fire likely based on sensor readings
    return 0  # No fire detected based on sensor readings

# Date and time range for the dataset
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='h')

# Generating 1 million data points
n_samples = 1000000

# Initialize lists to store data
timestamps = []
smoke_ppm_values = []
co_ppm_values = []
satellite_brightness = []
satellite_confidence = []
satellite_frp = []
satellite_daynight = []
fire_detected = []

# Loop through and generate data
for _ in range(n_samples):
    timestamp = np.random.choice(date_range)
    smoke_ppm, co_ppm = generate_sensor_data()
    satellite_data = None
    if np.random.rand() < 0.2:  # 20% chance of satellite data being available
        satellite_data = generate_satellite_data()
    
    fire_label = label_fire_detected(smoke_ppm, co_ppm, satellite_data)
    
    # Collecting data for the final dataset
    timestamps.append(timestamp)
    smoke_ppm_values.append(smoke_ppm)
    co_ppm_values.append(co_ppm)
    
    if satellite_data is not None:
        brightness, confidence, frp, daynight = satellite_data
        satellite_brightness.append(brightness)
        satellite_confidence.append(confidence)
        satellite_frp.append(frp)
        satellite_daynight.append(daynight)
    else:
        satellite_brightness.append(np.nan)
        satellite_confidence.append(np.nan)
        satellite_frp.append(np.nan)
        satellite_daynight.append(np.nan)
    
    fire_detected.append(fire_label)

# Create the DataFrame with generated data
data = pd.DataFrame({
    'timestamp': timestamps,
    'smoke_ppm': smoke_ppm_values,
    'co_ppm': co_ppm_values,
    'satellite_brightness': satellite_brightness,
    'satellite_confidence': satellite_confidence,
    'satellite_frp': satellite_frp,
    'satellite_daynight': satellite_daynight,
    'fire_detected': fire_detected
})

# Display the first few rows
data.head()
data.to_csv("data.csv", index=False)
