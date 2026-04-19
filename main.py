import os
import pandas as pd
import joblib
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. SETUP & MODELS
class ShipmentRequest(BaseModel):
    shipment_id: str
    current_lat: float
    current_lon: float
    dest_lat: float
    dest_lon: float

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Load ML Model
model = joblib.load('risk_engine_model.pkl')

# Initialize Firebase (Ensure serviceAccountKey.json is in the folder)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

@app.get("/")
def home():
    return {"status": "Risk Engine Online"}

@app.post("/predict-and-route")
async def predict_and_route(request: ShipmentRequest):
    try:
        # 1. Pull data from Firestore (Scenario script updates this)
        shipment_doc = db.collection('alerts').document(request.shipment_id).get()
        
        if shipment_doc.exists:
            data = shipment_doc.to_dict()
            weather = data.get('weather_severity', 0.0) # Default to 0
            congestion = data.get('port_congestion', 0.0) # Default to 0
        else:
            # If the document doesn't exist yet, it's a new shipment
            weather, congestion = 0.0, 0.0
            
        labor = 5.0 # Constant for now

        # 2. ML Prediction with proper Feature Names
        input_df = pd.DataFrame(
            [[weather, congestion, labor, 500.0]], 
            columns=['weather_severity', 'port_congestion', 'labor_stability', 'distance_km']
        )
        prediction = model.predict(input_df)[0]
        risk_score = min(round((prediction / 60) * 100, 2), 100)

        # 3. Rerouting Logic (Multi-Option Strategy)
        recommendation = "RE-ROUTE RECOMMENDED" if risk_score > 70 else "Maintain Route"
        
        # We create a dictionary of options instead of a single list
        route_options = {}
        
        if risk_score > 70:
            route_options = {
                "Balanced": {
                    "path": [
                        {"lat": request.current_lat, "lng": request.current_lon},
                        {"lat": request.current_lat + 0.8, "lng": request.current_lon + 0.8}, 
                        {"lat": request.dest_lat, "lng": request.dest_lon}
                    ],
                    "advantage": "Optimized fuel & safety",
                    "eta_impact": "+2.5h"
                },
                "Deep_Sea": {
                    "path": [
                        {"lat": request.current_lat, "lng": request.current_lon},
                        {"lat": request.current_lat + 1.5, "lng": request.current_lon + 2.0}, 
                        {"lat": request.dest_lat, "lng": request.dest_lon}
                    ],
                    "advantage": "Maximum safety (Lowest Risk)",
                    "eta_impact": "+5.2h"
                },
                "Coastal": {
                    "path": [
                        {"lat": request.current_lat, "lng": request.current_lon},
                        {"lat": request.current_lat + 0.4, "lng": request.current_lon + 0.2}, 
                        {"lat": request.dest_lat, "lng": request.dest_lon}
                    ],
                    "advantage": "Fastest recovery",
                    "eta_impact": "+1.1h"
                }
            }
        else:
            # Standard straight path if risk is low
            route_options = {
                "Standard": [
                    {"lat": request.current_lat, "lng": request.current_lon},
                    {"lat": request.dest_lat, "lng": request.dest_lon}
                ]
            }

        # 4. Sync back to Firestore
        db.collection('alerts').document(request.shipment_id).set({
            'risk_score': risk_score,
            'status': recommendation,
            'route_options': route_options, # Note the name change here
            'last_updated': firestore.SERVER_TIMESTAMP
        }, merge=True)

        # 5. THE RETURN
        print(f"--- SUCCESS: ID {request.shipment_id} | Risk: {risk_score} ---")
        return {
            "shipment_id": request.shipment_id,
            "risk_score": risk_score,
            "action": recommendation,
            "route_options": route_options # Sending the dictionary to frontend
        }

    except Exception as e:
        print(f"--- ERROR: {str(e)} ---")
        return {"error": str(e)}