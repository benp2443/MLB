import pandas as pd
import numpy as np
import sys
import argparse
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn import metrics
from sklearn.metrics import pairwise_distances

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs = '+', help = 'input data path')
args = parser.parse_args()

def cluster_pitch_types(df_path):
    df2 = pd.read_csv(df_path)

    temp = df2.loc[df2['year'] != 2014, ['pfx_x', 'pfx_y', 'start_speed', 'pitch_type']]
    temp.dropna(axis = 0, how = 'any', inplace = True)
    number_clusters = len(temp['pitch_type'].unique())
    X_scaled = preprocessing.scale(temp.iloc[:, 0:-1].values)

    cluster_labels = []
    scores = []
    for i in range(2, number_clusters + 1):
        kmeans = KMeans(n_clusters = i, n_init = 20, random_state = 0).fit(X_scaled)
        labels = kmeans.labels_.tolist()

        cluster_labels.append(labels)
        scores.append(metrics.calinski_harabaz_score(X_scaled, labels))

    max_idx = scores.index(max(scores))
    if max_idx + 1 == len(scores):
        temp['cluster'] = cluster_labels[max_idx]
    else:
        temp['cluster'] = cluster_labels[max_idx+1]

    results = temp.groupby(['cluster', 'pitch_type'])['pfx_x'].count().reset_index()
    results.rename(columns = {'pfx_x':'count'}, inplace = True)
    print(results)
    
    pitch_types = results['pitch_type'].unique()
    pitch_grouping = {}
    for pitch in pitch_types:
        pitch_grouping[pitch] = {'cluster':-1, 'count':-1, 'idx':-1}

    i = 0
    while i < len(results):
        pitch_type = results.iloc[i, 1]
        count = results.iloc[i, 2]
        
        if count > pitch_grouping[pitch_type]['count']:  # What if count is equal -> which cluster to assign to?
            cluster = results.iloc[i,0]
            pitch_grouping[pitch_type]['cluster'] = cluster
            pitch_grouping[pitch_type]['count'] = count
            pitch_grouping[pitch_type]['idx'] = i

        i += 1
    
    idx_list = []
    for pitch in pitch_types:
        idx_list.append(pitch_grouping[pitch]['idx'])

    results2 = results.iloc[idx_list, :].reset_index(drop = True).sort_values(by = 'pitch_type', axis = 0)

    number_of_clusters = results2['cluster'].unique()

    mapper = {}
    for cluster in number_of_clusters:
        mapper[cluster] = ''

    i = 0
    while i < len(results2):
        cluster = results2.iat[i, 0]
        pitch_type = results2.iat[i, 1]
        if mapper[cluster] == '':
            mapper[cluster] = pitch_type
        else:
            mapper[cluster] += '-' + pitch_type

        i += 1
                
    results2['group'] = results2['cluster'].map(mapper)

    final_mapper = dict(zip(results2['pitch_type'], results2['group']))

    df2['group_pitch_type'] = df2['pitch_type'].map(final_mapper)
    
    return df2

for pitcher in args.input:
    print(pitcher)
    sys.stdout.flush()
    new_df = cluster_pitch_types(pitcher)
    new_df.to_csv(pitcher)
