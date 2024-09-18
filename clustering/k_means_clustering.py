import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def load_filter_clean_data():
    # Load rad datasets 
    df1 = pd.read_csv('../data/processed/vector_data/EPSG_4326/reno_rad_cleaned.csv')  
    df2 = pd.read_csv('../data/processed/vector_data/EPSG_4326/walker_lake_rad_cleaned.csv')  

    # Concatenate datasets into one larger DataFrame
    df = pd.concat([df1, df2], ignore_index=True)

    # Select the columns for clustering
    features = ['Residual magnetic field value (nanoTeslas)', 'Apparent Thorium (ppm eTh)', 'Apparent Potassium (%)']

    # Filter the DataFrame to keep only the selected features
    df_filtered = df[features]

    # Handle missing values if there are any
    df_filtered = df_filtered.dropna()

    # Normalize the selected features (standard scaling)
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_filtered)

    return df, scaled_features

def get_ideal_num_clusters(scaled_features):
    # Calculate inertia for a range of cluster numbers
    inertia = []
    k_values = range(1, 20)

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(scaled_features)
        inertia.append(kmeans.inertia_)  # Inertia is the sum of squared distances to the nearest centroid

    # Plot the inertia to find the elbow point
    plt.figure(figsize=(8, 6))
    plt.plot(k_values, inertia, marker='o')
    plt.title('Elbow Method for Optimal Number of Clusters')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia (Sum of squared distances)')
    plt.show()
    
def perform_clustering(df, scaled_features, n_clusters):
    # Perform K-means clustering
    kmeans = KMeans(n_clusters, random_state=42) 
    kmeans.fit(scaled_features)

    # Add the cluster labels back to the original DataFrame
    df['Cluster'] = kmeans.labels_
    
    # Save the DataFrame with clusters as a CSV file
    df.to_csv("../data/processed/vector_data/EPSG_4326/reno_walker_lake_combined_km_clustered.csv", index=False)
    
    return df, scaled_features

def visualize_clusters(df):
    # Visualize the clusters with Residual Magnetic Field and Thorium
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df, x='Residual magnetic field value (nanoTeslas)', y='Apparent Thorium (ppm eTh)', hue='Cluster', palette='viridis')
    plt.title('K-Means Clustering based on Magnetic Field and Thorium')
    plt.xlabel('Residual Magnetic Field (nT)')
    plt.ylabel('Apparent Thorium (ppm eTh)')
    plt.show()
    
    # Visualize the clusters with Residual Magnetic Field and Potassium
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df, x='Residual magnetic field value (nanoTeslas)', y='Apparent Potassium (%)', hue='Cluster', palette='viridis')
    plt.title('K-Means Clustering based on Magnetic Field and Potassium')
    plt.xlabel('Residual Magnetic Field (nT)')
    plt.ylabel('Apparent Potassium (%)')
    plt.show()

df, scaled_features = load_filter_clean_data()
get_ideal_num_clusters(scaled_features)
n_clusters = 5
perform_clustering(df, scaled_features, n_clusters)
visualize_clusters(df)