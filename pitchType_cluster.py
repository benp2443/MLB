import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing

df = pd.read_csv('per_pitch_confidence.csv')

temp = df.loc[df['pitcher_id'] == 465657, ['pfx_x', 'pfx_z', 'start_speed', 'pitch_type']]
number_clusters = len(temp['pitch_type'].unique())

kmeans = KMeans(n_clusters = number_clusters, n_init = 20, random_state = 0)

X_scaled = preprocessing.scale(temp.iloc[:, 0:-1].values) 
clusters = kmeans.fit_predict(X_scaled)

temp['cluster'] = kmeans.labels_

results = temp.groupby(['cluster', 'pitch_type'])['pfx_x'].count().reset_index()
results.rename(columns = {'pfx_x':'count'}, inplace = True)
print(results)

pitch_types = []
for i in range(0, number_clusters):
    temp2 = results.loc[results['cluster'] == i, :].reset_index(drop = True)

    length = float(len(temp2))
    cluster_total = float(temp2['count'].sum())

    two_pitch_thresehold = 0.3
    other_pitch_thresehold = 1/length

    aa = []
    j = 0
    while j < length:
        pitch_type = temp2.iloc[j, 1]
        pitch_count = float(temp2.iloc[j, 2])
        pitch_percent = pitch_count/cluster_total

        if length <= 3:
            if pitch_percent > two_pitch_thresehold:
                aa.append(pitch_type)
        else:
            if pitch_percent > other_pitch_thresehold:
                aa.append(pitch_type)

        j += 1

    pitch_types.append(aa)
print(pitch_types)

clusters_types = {'FF':'FF/FT/FC', 'FT':'FF/FT/FC', 'FC':'FF/FT/FC', 'CU':'CU', 'SL':'SL', 'CH':'CH'}

temp['clustered_type'] = temp['pitch_type'].map(clusters_types)
temp.to_csv('delete.csv', index = False)
