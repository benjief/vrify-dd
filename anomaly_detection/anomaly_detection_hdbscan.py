import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import hdbscan
from sklearn.preprocessing import StandardScaler

def prepare_data(fp_1, fp_2):
    df1 = pd.read_csv(fp_1)  
    df2 = pd.read_csv(fp_2)  
    
    # Concatenate datasets into one larger DataFrame
    df = pd.concat([df1, df2], ignore_index=True)

    # Prepare the data to include spatial information (Longitude, Latitude) and line index
    X = df[['Flight line number', 'Longitude', 'Latitude', 'Residual magnetic field (comprehensive model CM4)']]

    # Normalize the magnetic values only
    scaler = StandardScaler()
    X.loc[:, 'Residual magnetic field (comprehensive model CM4)'] = scaler.fit_transform(X[['Residual magnetic field (comprehensive model CM4)']])
    
    return df, X

def perform_hdbscan(df, X):
    # Perform HDBSCAN clustering
    hdb = hdbscan.HDBSCAN(min_cluster_size=30, min_samples=2) # Tweak these values
    df['Cluster'] = hdb.fit_predict(X)

    # Detect anomalies: points classified as noise (-1)
    anomalies = df[df['Cluster'] == -1]
    print(f"Number of detected anomalies: {len(anomalies)}")
    print(anomalies)
    
    return anomalies

def save_anomalies(anomalies):
    output_file_path = "../data/processed/vector_data/EPSG_4326/reno_walker_lake_combined_mag_anomalies_hdbscan.csv"
    anomalies.to_csv(output_file_path, index=False)
    print(f"Anomalies saved to {output_file_path}")

fp_1 = '../data/processed/vector_data/EPSG_4326/reno_mag.csv'
fp_2 = '../data/processed/vector_data/EPSG_4326/walker_lake_mag.csv'
df, X = prepare_data(fp_1, fp_2)
anomalies = perform_hdbscan(df, X)
save_anomalies(anomalies)
