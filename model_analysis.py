import pandas as pd
import numpy as np
import sys
import argparse

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs = '+', help = 'input data path')
args = parser.parse_args()

df = pd.DataFrame()
if len(args.input) > 1:
    for pitcher in args.input:
        temp = pd.read_csv(pitcher)
        df = pd.concat([df, temp], axis = 0)
else:
    df = pd.read_csv(args.input[0])

df['best_model'] = df[['rf', 'svm']].idxmax(axis = 1)
df['max_value'] = df[['rf', 'svm']].max(axis = 1)

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
        df.loc[i,'difference'] = rf - svm
    else:
        df.loc[i,'difference'] = svm - rf

    i += 1

print(df['best_model'].value_counts())
print(df['max_value'].mean())
print(df['pos_neg'].value_counts())

print(df['difference'].mean())
print(df.groupby('best_model')['difference'].mean().reset_index())

df.to_csv('visualisations/model_analysis/test.csv')
