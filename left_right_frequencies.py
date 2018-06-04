import pandas as pd
import numpy as np
import argparse
import sys

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs = '+', help = 'input data path')
args = parser.parse_args()

data = []

for pitcher in args.input:

    print(pitcher)
    sys.stdout.flush()
    df = pd.read_csv(pitcher)
    pitcher = df['pitcher_id'] = df['pitcher_id'].unique()[0]

    df_train = df.loc[df['train_test'] == 'train', :]

    grouped_df = df_train.groupby(['b_handedness', 'group_pitch_type'])['home_team'].count().reset_index()
    grouped_df.rename(columns = {'home_team':'count'}, inplace = True)
    
    try:
        left_group = grouped_df.loc[grouped_df['b_handedness'] == 'L', :]
    except:
        continue

    try:
        right_group = grouped_df.loc[grouped_df['b_handedness'] == 'R', :]
    except:
        continue

    datasets = [left_group, right_group]

    for ds in datasets:
        sum_ = np.sum(ds['count'])
        ds['percent'] = np.round((ds['count']/sum_)*100,2)
    
    left_group = left_group.loc[:, ['group_pitch_type', 'percent']]
    right_group = right_group.loc[:, ['group_pitch_type', 'percent']]

    merged_df = pd.merge(left = left_group, right = right_group, on = 'group_pitch_type', how = 'inner')
    merged_df['percent_x'].fillna(0.0, inplace = True) # percent column names change on merge to _x, _y
    merged_df['percent_y'].fillna(0.0, inplace = True)

    merged_df['diff'] = np.sqrt(np.square(merged_df['percent_x'] - merged_df['percent_y']))
    average_diff = np.round(np.mean(merged_df['diff']),2)

    data.append([pitcher, average_diff])

output_df = pd.DataFrame(data, columns = ['Pitcher', 'difference'])
print(output_df)
output_df.to_csv('left_vs_right_freqs.csv', index = False)

