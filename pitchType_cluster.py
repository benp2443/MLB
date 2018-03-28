import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing

def cluster_pitch_types(df, pitcher_id):
    df2 = pd.read_csv(df)

    temp = df2.loc[df2['pitcher_id'] == pitcher_id, ['pfx_x', 'pfx_z', 'start_speed', 'pitch_type']]
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

    return pitch_types

test1 = cluster_pitch_types('per_pitch_confidence.csv', 465657) 
print(test1)
test2 = cluster_pitch_types('per_pitch_confidence.csv', 593372)
print(test2)
test3 = cluster_pitch_types('per_pitch_confidence.csv', 434378)
print(test3)

#clusters_465657 = {'FF':'FF/FT/FC', 'FT':'FF/FT/FC', 'FC':'FF/FT/FC', 'CU':'CU', 'SL':'SL', 'CH':'CH'}
#clusters_593372 = {'CH':'CH', 'FF':'FF/FT', 'FT':'FF/FT', 'CU':'CU/SL', 'SL':'CU/SL'}

#pitchers = [465657, 593372]

#temp = pd.read_csv('per_pitch_confidence.csv')
#temp1 = temp.loc[temp['pitcher_id'] == pitchers[0], :]
#temp2 = temp.loc[temp['pitcher_id'] == pitchers[1], :]

#temp1['cluster'] = temp1['pitch_type'].map(clusters_465657)
#temp2['cluster'] = temp2['pitch_type'].map(clusters_593372)

#final = pd.concat([temp1, temp2], axis = 0)
#print(final.head(10))
#print(final.tail(10))

#final.to_csv('delete.csv', index = False)
