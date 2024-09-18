import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

def prepare_data(file_path):
    df = pd.read_csv(file_path)

    # Prepare the data to include spatial information (Longitude, Latitude) and line index
    X = df[['Flight line number', 'Longitude', 'Latitude', 'Residual magnetic field (comprehensive model CM4)']]

    # Normalize the magnetic values only (optional but recommended for DBSCAN)
    scaler = StandardScaler()
    X.loc[:, 'Residual magnetic field (comprehensive model CM4)'] = scaler.fit_transform(X[['Residual magnetic field (comprehensive model CM4)']])
    
    return df, X

def calculate_k_distance(X):
    # Normalize the magnetic values only
    scaler = StandardScaler()
    X['Residual Magnetic Field (nT)'] = scaler.fit_transform(X[['Residual magnetic field (comprehensive model CM4)']])

    k = 5 
    neigh = NearestNeighbors(n_neighbors=k)
    nbrs = neigh.fit(X)
    distances, _ = nbrs.kneighbors(X)

    distances = np.sort(distances[:, k-1], axis=0)  # Sort the k-th nearest neighbor distances
    plt.figure(figsize=(8, 6))
    plt.plot(distances)
    plt.xlabel('Data Points')
    plt.ylabel(f'{k}-th Nearest Neighbor Distance')
    plt.title('k-distance Graph for Estimating eps')
    plt.show()

def perform_dbscan(df, X):
    dbscan = DBSCAN(eps=0.18, min_samples=8)  # k estimated from k-distance graph; min_samples to be tweaked
    df['Cluster'] = dbscan.fit_predict(X)


    anomalies = df[df['Cluster'] == -1]
    print(f"Number of detected anomalies: {len(anomalies)}")
    print(anomalies)
    
    return anomalies

def visualize_results(df):
    plt.figure(figsize=(10, 6))

    # Plot the magnetic field values for all data points, with different colors for clusters
    for line_number, line_data in df.groupby('Flight line number'):
        plt.plot(line_data.index, line_data['Residual Magnetic Field (nT)'], label=f'Line {line_number}')

    # Plot the detected anomalies in red
    for line_number, line_data in df.groupby('Flight line number'):
        anomalies = line_data[line_data['Cluster'] == -1]
        plt.scatter(anomalies.index, anomalies['Residual Magnetic Field (nT)'], color='red', label=f'Anomalies in Line {line_number}')

    plt.xlabel('Data Points')
    plt.ylabel('Magnetic Field (nT)')
    plt.legend()
    plt.title('Magnetic Field Anomalies Detected by DBSCAN')
    plt.show()

def save_anomalies(anomalies):
    output_file_path = "../data/processed/vector_data/EPSG_4326/walker_lake_mag_anomalies.csv"
    anomalies.to_csv(output_file_path, index=False)
    print(f"Anomalies saved to {output_file_path}")

walker_lake = "../data/processed/vector_data/EPSG_4326/walker_lake_mag.csv" 
df, X = prepare_data(walker_lake)
# calculate_k_distance(X)
anomalies = perform_dbscan(df, X)
save_anomalies(anomalies)
