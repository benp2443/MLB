import pandas as pd
import numpy as np
import sys
import argparse

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

df = pd.read_csv('results.csv')

print('mean naive acc')
print(df['naive_acc'].mean())
print('rf mean acc')
print(df['rf_mean_acc'].mean())
print('comp mean acc')
print(df['rf_comp_mean_acc'].mean())

df['score_train'] = np.round((df['rf_comp_mean_acc']/df['naive_acc'])*100,2)
print(df['score_train'].mean())

print('test mean naive acc')
print(df['rf_test_naive_acc'].mean())
print('test rf mean acc')
print(df['rf_test_acc'].mean())
print('test comp mean acc')
print(df['rf_test_comp_acc'].mean())

df['score_test'] = np.round((df['rf_test_comp_acc']/df['rf_test_naive_acc'])*100,2)
print(df['score_test'].mean())


temp = df[['rf_comp_mean_acc', 'rf_test_comp_acc']]
temp.rename(columns = {'rf_comp_mean_acc':'Train', 'rf_test_comp_acc':'Test'}, inplace = True)
temp = pd.melt(temp)
temp.to_csv('visualisations/model_analysis/temp1.csv', index = False)

def pos_neg(x):
    if x > 0.0:
        return 'Positive'
    elif x < 0.0:
        return 'Negative'
    else:
        return 'Neutral'

aa




df['best_model'] = df[['rf_comp_mean_acc', 'svm_comp_mean_acc']].idxmax(axis = 1)
df['max_value'] = df[['rf_comp_mean_acc', 'svm_comp_mean_acc']].max(axis = 1)

name_mapper = {'rf_comp_mean_acc':'Random Forest', 'svm_comp_mean_acc':'Support Vector Machine'}
df['best_model'] = df['best_model'].map(name_mapper)

def pos_neg(x):
    if x > 0.0:
        return 'Positive'
    elif x < 0.0:
        return 'Negative'
    else:
        return 'Neutral'


df['pos_neg'] = df['max_value'].apply(pos_neg)

df['difference'] = -np.inf
df['test_value'] = -np.inf
df['best_model_std'] = -np.inf

i = 0
while i < len(df):

    rf = df.loc[i, 'rf_comp_mean_acc']
    svm = df.loc[i, 'svm_comp_mean_acc']

    if rf >= svm:
        df.loc[i,'difference'] = rf - svm
    else:
        df.loc[i,'difference'] = svm - rf

    if df.loc[i, 'best_model'] == 'Random Forest':
        df.loc[i, 'test_value'] = df.loc[i, 'rf_test_comp_acc']
        df.loc[i, 'best_model_std'] = df.loc[i, 'rf_comp_std']
    else:
        df.loc[i, 'test_value'] = df.loc[i, 'svm_test_comp_acc']
        df.loc[i, 'best_model_std'] = df.loc[i, 'svm_comp_std']

    i += 1


df.to_csv('visualisations/model_analysis/results.csv', index = False)

print(df['best_model'].value_counts())
print(df['max_value'].mean())
print(df['test_value'].mean())
print(df['pos_neg'].value_counts())
print(df['difference'].mean())
print(df.groupby('best_model')['difference'].mean().reset_index())

df3 = pd.read_csv('feature_importance_all.csv')
median_list = np.median(df3, axis = 0)
median_series = pd.Series(median_list, df3.columns.values).sort_values(ascending = False)
print(median_series)
df3 = df3[median_series.index.tolist()]

df3 = pd.melt(df3)
print(df3)
df3.to_csv('feature_importance_ordered.csv', index = False)

##### Count Accuracy #####
df4 = pd.read_csv('count_accuracy.csv')
df4['model'] = df4['model'].map({'rf':'Random Forest', 'svm':'Support Vector Machine'})
temp = df[['pitcher_id', 'best_model']]
df4 = pd.merge(df4, temp, how = 'inner', left_on = ['pitcher', 'model'], right_on = ['pitcher_id', 'best_model'])
df4.drop(['pitcher', 'model', 'pitcher_id', 'best_model'], axis = 1, inplace = True)
df4.rename(columns = {'count_dummy':'count_0-0'}, inplace = True)
print(df4)
melted_df = pd.melt(df4)
print(melted_df)
melted_df.to_csv('visualisations/model_analysis/count_accuracy.csv', index = False)


aa
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
