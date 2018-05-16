import pandas as pd
import numpy as np
import sys

df = pd.read_csv('predictions.csv')

df['best_model'] = df[['rf', 'ovo_rbf_svm']].idxmax(axis = 1)
df['max_value'] = df[['rf', 'ovo_rbf_svm']].max(axis = 1)

def pos_neg(x):
    if x > 0.0:
        return 'pos'
    elif x < 0.0:
        return 'neg'
    else:
        return 'neutral'


df['pos_neg'] = df['max_value'].apply(pos_neg)

df['difference'] = -np.inf

i = 0
while i < len(df):
    rf = df.iloc[i,1]
    svm = df.iloc[i,2]

    if rf >= svm:
        df.iloc[i,6] = rf - svm
    else:
        df.iloc[i,6] = svm - rf

    i += 1

print(df['best_model'].value_counts())
print(df['max_value'].mean())
print(df['pos_neg'].value_counts())

print(df['difference'].mean())
print(df.groupby('best_model')['difference'].mean().reset_index())

