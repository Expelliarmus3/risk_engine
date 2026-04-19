import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def train_risk_engine():
    # Load data
    df = pd.read_csv('shipment_data.csv')
    
    # Features (X) and Target (y)
    X = df[['weather_severity', 'port_congestion', 'labor_stability', 'distance_km']]
    y = df['delay_hours']
    
    # Split for testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train Random Forest
    # n_estimators=100 is plenty for a prototype
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save the model to a file
    joblib.dump(model, 'risk_engine_model.pkl')
    print("Model trained and saved as risk_engine_model.pkl")

    # Quick test: Feature Importance
    for feature, importance in zip(X.columns, model.feature_importances_):
        print(f"Feature: {feature}, Importance: {importance:.2f}")

if __name__ == "__main__":
    train_risk_engine()