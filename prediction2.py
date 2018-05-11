import pandas as pd
import numpy as np

df = pd.read_csv('predictions.csv')
vol_df = pd.read_csv('visualisations/pitch_frequencies/volatility.csv')

df = df.merge(vol_df, how = 'inner', on = 'pitcher_id')

print(len(df))

cols = df.columns.values.tolist()
result_cols = [col for col in cols if col not in ['pitcher_id', 'change_value']]

for col in result_cols:
    print(col)
    print(len(df.loc[df[col] == -1, :]))

aa    

temp = df.loc[:, result_cols]

temp['best_model'] = temp.idxmax(axis = 1)
temp['max_value'] = temp.max(axis = 1)

df['best_model'] = temp['best_model']
df['max_value'] = temp['max_value']

def pos_neg(x):
    if x > 0:
        return 'pos'
    elif x < 0:
        return 'neg'
    else:
        return 'same'

df['pos_neg'] = df['max_value'].apply(pos_neg)

df['discrete_change'] = (df['change_value']/10).astype(int)

print(df.groupby('discrete_change')['max_value'].mean())

#print(df['pos_neg'].value_counts())
#print(df.groupby('pos_neg')['max_value'].mean())
#print(df['best_model'].value_counts())
#
#print(len(df))

