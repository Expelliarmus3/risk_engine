import pandas as pd
import numpy as np

def generate_supply_chain_data(num_samples=1000):
    np.random.seed(42)
    
    # Feature 1: Weather (0-10)
    weather = np.random.uniform(0, 10, num_samples)
    # Feature 2: Port Congestion (0-10)
    congestion = np.random.uniform(0, 10, num_samples)
    # Feature 3: Labor Sentiment (0-10, lower is worse)
    labor = np.random.uniform(0, 10, num_samples)
    # Feature 4: Distance (km)
    distance = np.random.uniform(100, 5000, num_samples)
    
    # Logic for Delay (The 'Ground Truth' the AI must find)
    # Delay = (Dist/100) + (Weather * 2) + (Congestion * 3) - (Labor * 0.5) + noise
    noise = np.random.normal(0, 2, num_samples)
    delay = (distance / 100) + (weather * 1.5) + (congestion * 2.5) + (10 - labor) + noise
    
    # Ensure no negative delays
    delay = np.clip(delay, 0, None)
    
    df = pd.DataFrame({
        'weather_severity': weather,
        'port_congestion': congestion,
        'labor_stability': labor,
        'distance_km': distance,
        'delay_hours': delay
    })
    
    df.to_csv('shipment_data.csv', index=False)
    print(f"Generated {num_samples} records in shipment_data.csv")

if __name__ == "__main__":
    generate_supply_chain_data()