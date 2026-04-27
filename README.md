# Anticipatory Risk Engine (ARE)

## Description

*The Anticipatory Risk Engine (ARE) is a professional-grade logistics dashboard that transforms supply chain management from reactive to predictive. Utilizing a Random Forest Classifier hosted on a Render backend (Python 3.11/FastAPI), the system performs real-time inference on vessel telemetry to identify potential maritime disruptions. These insights are synchronized via Google Cloud Firestore to a high-performance Vercel frontend, where a Leaflet.js geospatial dashboard visualizes active shipments and automatically generates alternate "AI Strategy" routes when risk exceeds a 70% threshold.*

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/risk-engine.git

# Install Python dependencies for the Backend and Simulation scripts
pip install -r requirements.txt
```

## Usage

```bash
# To trigger the real-time risk escalation simulation:
python scenario.py

# To access the live dashboard:
# Open your Vercel URL:https://risk-engine-kyjv.vercel.app/
and enter the passkey: 123
```

## Features

- **Real-Time Risk Telemetry**: *Seamlessly synchronizes vessel coordinates and environmental data from edge simulations to the cloud dashboard using Google Cloud Firestore, ensuring sub-second updates.*

- **Predictive AI Inference**: *Integrates a custom-trained Random Forest Classifier that evaluates multiple risk factors (weather, geopolitical tension, and port congestion) to generate a dynamic 0–100% risk score.*

- **Automated Strategy Orchestration**: *When high-risk thresholds (>70%) are detected, the system automatically triggers AI Strategy Cards that suggest optimal rerouting paths (e.g., "Deep Sea Alternative" or "Cape of Good Hope").*

- **Geospatial Intelligence**: *Built with Leaflet.js to provide a high-performance interactive map interface, featuring real-time vessel tracking and dashed-line visualizations for AI-projected routes.*

- **Encrypted Authentication**: *Includes a secure, lightweight passkey-protected entry system to prevent unauthorized access to sensitive logistical data.*

- **Anticipatory ETA Analysis**: *Every AI-suggested route provides a calculated trade-off analysis, comparing the increase in transit time against the reduction in disruption risk.*

