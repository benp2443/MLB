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

pitch_groupings = {}
for pitcher in args.input:
    print(pitcher)
    df = pd.read_csv(pitcher)
    groupings = df['group_pitch_type'].unique().tolist()
    for group in groupings:
        if group in pitch_groupings:
            pitch_groupings[group] += 1
        else:
            pitch_groupings[group] = 1


dictlist = []
for key, value in pitch_groupings.items():
    temp = [key,value]
    dictlist.append(temp)
   
df = pd.DataFrame(dictlist, columns = ['group', 'count'])
df.to_csv('visualisations/pitch_types/pitch_groupings.csv', index = False)

