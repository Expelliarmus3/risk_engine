import time
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def run_storm_scenario():
    print("Starting Demo Scenario: 'Approaching Storm in Suez'...")
    shipment_ref = db.collection('alerts').document('SHP-SUEZ-001')

    # Simulate weather getting worse every 5 seconds
    for severity in range(1, 11):
        print(f"Weather Severity is now: {severity}/10")
        # Use .set with merge=True instead of .update
        shipment_ref.set({
            'weather_severity': severity,
            'port_congestion': severity,
            'status': "Processing..."
        }, merge=True)
        time.sleep(5)
    
    print("Scenario Complete.")

if __name__ == "__main__":
    run_storm_scenario()