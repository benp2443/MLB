import pandas as pd
import numpy as np
import sys
import argparse

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs = '+', help = 'input data path')
args = parser.parse_args()

#df = pd.DataFrame()
#if len(args.input) > 1:
#    for pitcher in args.input:
#        temp = pd.read_csv(pitcher)
#        df = pd.concat([df, temp], axis = 0)
#else:
#    df = pd.read_csv(args.input[0])
#
#print(np.mean(df.rf))
#df['best_model'] = df[['rf', 'svm']].idxmax(axis = 1)
#df['max_value'] = df[['rf', 'svm']].max(axis = 1)
#print(np.mean(df.rf))
#
#def pos_neg(x):
#    if x > 0.0:
#        return 'pos'
#    elif x < 0.0:
#        return 'neg'
#    else:
#        return 'neutral'
#
#
#df['pos_neg'] = df['max_value'].apply(pos_neg)
#
#df['difference'] = -np.inf
#
#i = 0
#while i < len(df):
#    rf = df.iloc[i,1]
#    svm = df.iloc[i,2]
#
#    if rf >= svm:
#        df.loc[i,'difference'] = rf - svm
#    else:
#        df.loc[i,'difference'] = svm - rf
#
#    i += 1
#
#print(df['best_model'].value_counts())
#print(df['max_value'].mean())
#print(df['pos_neg'].value_counts())
#
#print(df['difference'].mean())
#print(df.groupby('best_model')['difference'].mean().reset_index())
#
#df.to_csv('visualisations/model_analysis/test.csv')
#
df = pd.read_csv('feature_importance_all.csv')
print(df.head())
print(df.shape)

median_list = np.median(df, axis = -1).sort_values(ascending = False)
print(median_list)
median_series = pd.Series(median_list, df.columns.values).sort_values(ascending = False)
print(median_series)
df = df[median_series.index.tolist()]

df = df.melt()
df.to_csv('feature_importance_ordered.csv', index = False)


##### Count Accuracy #####
df = pd.read_csv('count_accuracy.csv')
df.rename(columns = {'count_dummy':'count_0-0'}, inplace = True)
melted_df = pd.melt(df)
melted_df.to_csv('visualisations/model_analysis/count_accuracy.csv', index = False)


##### Probability and Correct Prediction ######
df = pd.read_csv('prob_pred.csv')
df.columns = ['Pitcher', 'Probability', 'Correct']
print(df.head(), 20)

df['Probability'] = np.round(df['Probability'].values, 1)

grouped_df = df.groupby(['Pitcher', 'Probability'])['Correct'].mean().reset_index()
grouped_df.to_csv('visualisations/model_analysis/average_over_probs.csv', index = False)

print(grouped_df)

grouped_df  = df.groupby(['Pitcher', 'Probability'])['Correct'].count().reset_index()
print(grouped_df)
