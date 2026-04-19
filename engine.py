import joblib
import networkx as nx
import numpy as np

import numpy as np
import networkx as nx
import joblib

model = joblib.load('risk_engine_model.pkl')

def generate_ai_path(start_coords, end_coords):
    """
    Creates a dynamic grid between start and end, 
    calculates risk for each leg, and finds the safest path.
    """
    G = nx.Graph()
    
    # Simple 3-step grid generation between two points
    lats = np.linspace(start_coords[0], end_coords[0], 4)
    lons = np.linspace(start_coords[1], end_coords[1], 4)
    
    nodes = []
    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            node_id = f"{i}_{j}"
            # Simulate environment data for this specific coordinate
            # In production, you'd fetch weather/congestion for this LAT/LON
            weather = np.random.uniform(1, 9) 
            congestion = np.random.uniform(1, 9)
            
            # Predict Risk for this 'zone'
            risk_pred = model.predict([[weather, congestion, 8.0, 100]])[0]
            risk_weight = np.clip((risk_pred / 15) * 100, 1, 100)
            
            G.add_node(node_id, pos=(lat, lon), risk=risk_weight)
            nodes.append(node_id)

    # Connect adjacent nodes in the grid
    for i in range(3):
        for j in range(3):
            G.add_edge(f"{i}_{j}", f"{i+1}_{j}", weight=G.nodes[f"{i+1}_{j}"]['risk'])
            G.add_edge(f"{i}_{j}", f"{i}_{j+1}", weight=G.nodes[f"{i}_{j+1}"]['risk'])

    # Find shortest path based on RISK weight, not distance
    path_nodes = nx.shortest_path(G, source="0_0", target="3_3", weight='weight')
    
    # Convert node IDs back to coordinate objects for Leaflet.js
    path_coords = [{"lat": G.nodes[n]['pos'][0], "lng": G.nodes[n]['pos'][1]} for n in path_nodes]
    return path_coords

# # Load our Random Forest model
# model = joblib.load('risk_engine_model.pkl')

# def get_risk_score(weather, congestion, labor, distance):
#     """Predicts delay and converts it to a 0-100 score."""
#     prediction = model.predict([[weather, congestion, labor, distance]])[0]
#     # Simple normalization: 0 hours = 0 score, 15+ hours = 100 score
#     score = np.clip((prediction / 15) * 100, 0, 100)
#     return round(score, 2)

# def calculate_best_path(graph, start_node, end_node):
#     """
#     Uses Dijkstra's to find a path. 
#     In our 'Risk Engine', the 'weight' of an edge is the Risk Score.
#     Dijkstra will naturally pick the path with the lowest total risk.
#     """
#     path = nx.shortest_path(graph, source=start_node, target=end_node, weight='risk')
#     return path

# # --- MOCKING THE WORLD MAP ---
# # Let's create a small grid of coordinates (Lat, Long)
# G = nx.Graph()

# # Nodes represent Ports/Hubs (Lat, Long)
# hubs = {
#     'Port_A': (34.05, -118.24), # Los Angeles
#     'Port_B': (36.16, -115.13), # Las Vegas
#     'Port_C': (37.77, -122.41), # San Francisco
#     'Port_D': (45.51, -122.67)  # Portland
# }

# # Add edges with a 'Risk Score' we calculated
# # Example: Port_A to Port_C is risky due to a storm
# G.add_edge('Port_A', 'Port_C', risk=85) 
# G.add_edge('Port_A', 'Port_B', risk=10) 
# G.add_edge('Port_B', 'Port_C', risk=15)
# G.add_edge('Port_C', 'Port_D', risk=20)

# # If we want to go from A to C:
# # Direct (A->C) weight is 85. 
# # Indirect (A->B->C) weight is 10 + 15 = 25.
# # Dijkstra will choose A -> B -> C.
# best_route = calculate_best_path(G, 'Port_A', 'Port_C')
# print(f"Optimized Route to bypass risk: {best_route}")