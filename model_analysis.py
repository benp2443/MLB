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
df = pd.read_csv('results.csv')
print(df['pitcher_id'].value_counts())
print(len(df))
df = df.loc[~df['birth_year'].isnull(), :] # Merge in predictions.py cause problems!
print(len(df))
df.drop_duplicates(inplace = True)
print(len(df))
print(len(np.unique(df['pitcher_id'])))
aa

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

age_df = df[['rf', 'birth_year']]
age_df = age_df.loc[~age_df['birth_year'].isnull(), :]
age_df['age'] = 2017.0 - age_df['birth_year']
print(age_df)
age_df.to_csv('visualisations/model_analysis/age_vs_accuracy.csv', index = False)

aa


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
temp = df[['pitcher_id', 'best_model']]
df4 = pd.merge(df4, temp, how = 'inner', left_on = ['pitcher', 'model'], right_on = ['pitcher_id', 'best_model'])
df4.drop(['pitcher', 'model', 'pitcher_id', 'best_model'], axis = 1, inplace = True)
df4.rename(columns = {'count_dummy':'count_0-0'}, inplace = True)
melted_df = pd.melt(dfd)
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
