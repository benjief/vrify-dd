import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

def prepare_data(fp_1, fp_2):
    df1 = pd.read_csv(fp_1)  
    df2 = pd.read_csv(fp_2)  
    
    # Concatenate datasets into one larger DataFrame
    df = pd.concat([df1, df2], ignore_index=True)

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
    dbscan = DBSCAN(eps=0.18, min_samples=8)  # k estimated from k-distance graph; min_samples can be tweaked
    df['Cluster'] = dbscan.fit_predict(X)


    anomalies = df[df['Cluster'] == -1]
    print(f"Number of detected anomalies: {len(anomalies)}")
    print(anomalies)
    
    return anomalies

def save_anomalies(anomalies):
    output_file_path = "../data/processed/vector_data/EPSG_4326/reno_walker_lake_combined_mag_anomalies_dbscan.csv"
    anomalies.to_csv(output_file_path, index=False)
    print(f"Anomalies saved to {output_file_path}")

fp_1 = '../data/processed/vector_data/EPSG_4326/reno_mag.csv'
fp_2 = '../data/processed/vector_data/EPSG_4326/walker_lake_mag.csv'
df, X = prepare_data(fp_1, fp_2)
calculate_k_distance(X)
# anomalies = perform_dbscan(df, X)
# save_anomalies(anomalies)
