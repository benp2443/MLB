import pandas as pd
import numpy as np
import argparse
import sys

pd.set_option('max.rows', 500)

df = pd.read_csv('individual_df/fe/279571_fe.csv')

 # hand difference
def same_hand(row):
    if row['p_handedness'] == row['b_handedness']:
        return 1
    else:
        return 0

df['hand'] = df.apply(same_hand, axis = 1)

print(df[['p_handedness', 'b_handedness', 'hand']])
##### Global Pitch Frequencies #####

# Create columns and lists for each pitch type
u_pitches = df['group_pitch_type'].unique()
pitch_count_dict = {}
prior_columns = []
weighted_count_dict = {}
weighted_cols = []

for pitch_type in u_pitches:
    col_name = 'global_prior_' + pitch_type
    prior_columns.append(col_name)
    pitch_count_dict[pitch_type] = 0
    df[col_name] = np.nan
    df.loc[0, col_name] = 0

    weighted_name = col_name + '_weighted'
    weighted_cols.append(weighted_name)
    weighted_count_dict[weighted_name] = 0
    df[weighted_name] = np.nan
    df.loc[0, weighted_name] = 0

# loop through df, updating prior cols and weighted cols, window cols
i = 0
while i < len(df) - 1:
    pitch_type = df.loc[i, 'group_pitch_type']
    column_name = 'global_prior_' + pitch_type
    weighted_name = column_name + '_weighted'
    pitch_count_dict[pitch_type] += 1
    weighted_count_dict[weighted_name] += i + 1
    df.loc[i+1, column_name] = pitch_count_dict[pitch_type]
    df.loc[i+1, weighted_name] = weighted_count_dict[weighted_name]
    
    i += 1

# Forward fill null values in prior columns, backfill the 2014 values
for col in prior_columns:
    df[col].fillna(method = 'ffill', inplace = True)
    df[col].fillna(method = 'bfill', inplace = True)

    weighted_col =  col + '_weighted'
    df[weighted_col].fillna(method = 'ffill', inplace = True)
    df[weighted_col].fillna(method = 'bfill', inplace = True)

df['total_pitches'] = df[prior_columns].sum(axis = 1)
df['weighted_total_pitches'] = df[weighted_cols].sum(axis = 1)

# Create global percentage columns
for col in prior_columns:
    column_name = 'a_' + col + '_percent'
    df[column_name] = df[col]/df['total_pitches']

    weighted_col = col + '_weighted'
    percent_col = 'b_' + weighted_col + '_percent'
    df[percent_col] = df[weighted_col]/df['weighted_total_pitches']


##### Pitch Frequencies in windows #####
w_40 = np.array([])
w_120 = np.array([])
w_360 = []
w_40_cols = []
w_120_cols = []
w_360_cols = []
w_40_percent_cols = []
w_120_percent_cols = []
w_360_percent_cols = []

for pitch_type in u_pitches:
    col_name = 'w_40_' + pitch_type
    w_40_cols.append(col_name)
    df[col_name] = 0

    col_name2 = 'w_120_' + pitch_type
    w_120_cols.append(col_name2)
    df[col_name2] = 0

    col_name3 = 'w_360_' + pitch_type
    w_360_cols.append(col_name3)
    df[col_name3] = 0


i = 0
w_40_full = False
w_120_full = False
w_360_full = False

while i < len(df) - 1:
    pitch_type = df.loc[i, 'group_pitch_type']
    col_name = 'w_40_' + pitch_type
    col_name2 = 'w_120_' + pitch_type
    col_name3 = 'w_360_' + pitch_type

    temp = np.array([pitch_type])
    w_40 = np.append(w_40, temp)
    w_120 = np.append(w_120, temp)
    w_360 = np.append(w_360, temp)

    if len(w_40) > 40:
        w_40_full = True
    if len(w_120) > 120:
        w_120_full = True
    if len(w_360) > 360:
        w_360_full = True

    if w_40_full == True:
        w_40 = w_40[1:] 
    if w_120_full == True:
        w_120 = w_120[1:]
    if w_360_full == True:
        w_360 = w_360[1:]

    for col in w_40_cols:
        pitch = col.split('_')[-1]
        df.loc[i + 1, col] = len(w_40[w_40 == pitch])

    for col in w_120_cols:
        pitch = col.split('_')[-1]
        df.loc[i + 1, col] = len(w_120[w_120 == pitch])

    for col in w_360_cols:
        pitch = col.split('_')[-1]
        df.loc[i + 1, col] = len(w_360[w_360 == pitch])


    i += 1

for col in w_40_cols:    
    percent_col = 'c_' + col + '_percent'
    df[percent_col] = df[col]/40

for col in w_120_cols:    
    percent_col = 'd_' + col + '_percent'
    df[percent_col] = df[col]/120

for col in w_360_cols:    
    percent_col = 'e_' + col + '_percent'
    df[percent_col] = df[col]/360


# Priors to the specific batter
batter_specific_cols = []

for col in prior_columns:
    col_name = col + '_to_batter'
    batter_specific_cols.append(col_name)
    df[col_name] = np.nan


batter_priors = {}
i = 0
while i < len(df):
    batter = df.loc[i, 'batter_id']
    pitch = df.loc[i, 'group_pitch_type']

    if batter in batter_priors:
        for col in batter_specific_cols:
            for p_type in u_pitches:
                if p_type in col:
                    df.loc[i, col] = batter_priors[batter][p_type]
                    break

        batter_priors[batter][pitch] += 1

    else:
        batter_priors[batter] = {}
        for pitch in u_pitches: # If they add a new pitch between train and test, too bad.
            batter_priors[batter][pitch] = 0.0

        continue

    i += 1

df['batter_specific_count'] = df.loc[:, batter_specific_cols].sum(axis = 1)

for col in batter_specific_cols:
    df[col].fillna(method = 'ffill', inplace = True)
    df[col].fillna(method = 'bfill', inplace = True)

for col in batter_specific_cols:
    beta = 6
    column_name = col + '_percent'
    pitch = column_name.split('_')[2]
    hist_prior_col = 'e_w_360_{}_percent'.format(pitch)
    hist_prior = df[hist_prior_col]
    batter_prior = df[col]/df['batter_specific_count']

    weighted_col = 'f_' + column_name + '_weighted'
    df[weighted_col] = (df['batter_specific_count']*batter_prior + beta * hist_prior)/(df['batter_specific_count'] + beta)



print(df[['e_w_360_SL_percent', 'global_prior_SL_to_batter', 'batter_specific_count', 'f_global_prior_SL_to_batter_percent_weighted']]) 
df.drop(prior_columns, axis = 1, inplace = True)
df.drop(batter_specific_cols, axis = 1, inplace = True)
df.drop(['total_pitches'], axis = 1, inplace = True)
 
print(df.columns.values)
aa
#### Line chart wrangling

#temp = df.loc[df['year'] != 2014, ['game_id', 'global_prior_SL_percent', 'global_prior_FF_percent', \
#                                   'global_prior_CU_percent', 'global_prior_CH-FT_percent', \
#                                   'global_prior_SL_weighted_percent', 'global_prior_FF_weighted_percent', \
#                                   'global_prior_CU_weighted_percent', 'global_prior_CH-FT_weighted_percent']]
#
#
#temp.drop_duplicates(subset = ['game_id'], keep = 'last', inplace = True)
#temp2 = pd.melt(temp, id_vars = ['game_id'])
#temp2.to_csv('visualisations/pitch_frequencies/pitch_frequencies_change.csv', index = False)
#
#temp2 = df.loc[df['year'] != 2014, ['game_id', 'w_40_SL_percent', 'w_40_FF_percent', 'w_40_CH-FT_percent', 'w_40_CU_percent', \
#                                               'w_120_SL_percent', 'w_120_FF_percent', 'w_120_CH-FT_percent', 'w_120_CU_percent', \
#                                               'w_360_SL_percent', 'w_360_FF_percent', 'w_360_CH-FT_percent', 'w_360_CU_percent']]
#
#temp2 = pd.melt(temp2, id_vars = ['game_id'])
#temp2.to_csv('visualisations/pitch_frequencies/pitch_frequencies_windows.csv', index = False)
