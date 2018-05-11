import pandas as pd
import numpy as np
import argparse
import sys

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs = '+', help = 'input data path')
args = parser.parse_args()

for pitcher in args.input:
    print(pitcher)
    df = pd.read_csv(pitcher)
    
    df = df.loc[~((df['group_pitch_type'].isnull()) & (df['year'] == 2014)), :].reset_index(drop = True)

    # Replace NA values for prior pitch, prior_px, prior_py
    #df['prior_py'].replace(np.inf, np.nan, inplace = True)
    #df['prior_px'].replace(np.inf, np.nan, inplace = True)
    #df['prior_pitch'].replace('', np.nan, inplace = True)
    #
    #mean_px = df.loc[df['train_test'] == 'train', 'prior_px'].mean()
    #mean_py = df.loc[df['train_test'] == 'train', 'prior_py'].mean()
    #mode_type = df.loc[df['train_test'] == 'train', 'prior_pitch'].mode()[0]
    #
    #df['prior_py'].replace(np.nan, mean_py, inplace = True)
    #df['prior_px'].replace(np.nan, mean_px, inplace = True)
    #df['prior_pitch'].replace(np.nan, mode_type, inplace = True)
    
    # Count
    df['count'] = df['ball_count'].astype(str) + '-' + df['strike_count'].astype(str)
    
    # Function to return index of column
    def column_idx(df, column_name):
        return df.columns.values.tolist().index(column_name)
    
    # Score difference (from the pitchers perspective)
    def score_diff(row):
        if row['inning_half'] == 'top':
            return row['home_runs'] - row['away_runs']
        else:
            return row['away_runs'] - row['home_runs']
    
    df['score_diff'] = df.apply(score_diff, axis = 1)
    
    ##### Global Pitch Frequencies #####
    
    # Find 2014 frequencies
    temp = df.loc[df['year'] == 2014, :]
    pitch_freq = temp.groupby('group_pitch_type')['home_team'].count().reset_index()
    pitch_freq.rename(columns = {'home_team':'count'}, inplace = True)
    pitch_types_2014 = pitch_freq['group_pitch_type'].values.tolist()
    
    temp2 = df.loc[df['train_test'] == 'train', :]
    train_pitch_types = df['group_pitch_type'].unique().tolist()
    
    pitch_count_dict = {}
    prior_columns = []
    for pitch_type in train_pitch_types:
        print(pitch_type)
        sys.stdout.flush()
        col_name = 'global_prior_' + pitch_type
        prior_columns.append(col_name)
        if pitch_type in pitch_types_2014:
            pitch_count_dict[pitch_type] = pitch_freq.loc[pitch_freq['group_pitch_type'] == pitch_type, 'count'].values[0]
        else:
            pitch_count_dict[pitch_type] = 0
    
    # Create null columns for each pitch type
    for col in prior_columns:
        df[col] = np.nan
    
    i = temp2.index.values[0] # First pitch of 2015
    while i < df.index.values[-1]:
        pitch_type = df.loc[i, 'group_pitch_type']
        column_name = 'global_prior_' + pitch_type
        if pitch_type in pitch_count_dict:
            pitch_count_dict[pitch_type] += 1
            df.loc[i+1, column_name] = pitch_count_dict[pitch_type]
        else: # Have not checked this code for new pitch types in test set
            pitch_count_dict[pitch_type] = 0
            df[column_name] = np.nan
            prior_columns.append(column_name)
            continue
        
        i += 1
    
    # Forward fill null values in prior columns, backfill the 2014 values
    for col in prior_columns:
        df[col].fillna(method = 'ffill', inplace = True)
        df[col].fillna(method = 'bfill', inplace = True)
    
    totals = df.loc[:, prior_columns].sum(axis = 1)
    df['total_pitches'] = totals
    
    # Create global percentage columns
    for col in prior_columns:
        column_name = col + '_percent'
        df[column_name] = df[col]/df['total_pitches']
    
    #years = [2015, 2016, 2017]
    #temp = df.loc[df['year'].isin(years), ['year', 'global_prior_SL_percent', 'global_prior_IN_percent', 'global_prior_CH_percent', \
    #                                       'global_prior_FT_percent', 'global_prior_FF_percent']].reset_index(drop = True).reset_index()
    #
    #temp2.rename(columns = {'index':'pitch_id'}, inplace = True)
    #temp2 = pd.melt(temp2, id_vars = ['pitch_id', 'year'])
    #temp2.to_csv('visualisations/pitch_frequencies/pitch_freq.csv', index = False)
    
    # Priors to the specific batter
    batter_specific_cols = []
    
    for col in prior_columns:
        col_name = col + '_to_batter'
        batter_specific_cols.append(col_name)
        df[col_name] = 0.0
    
    
    batter_priors = {}
    i = 0
    while i < len(df):
        batter = df.loc[i, 'batter_id']
        pitch = df.loc[i, 'group_pitch_type']
    
        if batter in batter_priors:
            for col in batter_specific_cols:
                for p_type in train_pitch_types:
                    if p_type in col:
                        df.loc[i, col] = batter_priors[batter][p_type]
                        break
    
            batter_priors[batter][pitch] += 1
    
        else:
            batter_priors[batter] = {}
            for pitch in train_pitch_types: # If they add a new pitch between train and test, too bad.
                batter_priors[batter][pitch] = 0.0
    
            continue
    
        i += 1
    
    df['batter_specific_count'] = df.loc[:, batter_specific_cols].sum(axis = 1)
    
    for col in batter_specific_cols:
         column_name = col + '_percent'
         df[column_name] = df[col]/df['batter_specific_count']
    
    df.drop(prior_columns, axis = 1, inplace = True)
    df.drop(batter_specific_cols, axis = 1, inplace = True)
    df.drop(['total_pitches'], axis = 1, inplace = True)
    
    ##### Looking at runners on base #####
    df['runners_on'] = df['on_first'].astype(int) + df['on_second'].astype(int) + df['on_third'].astype(int)
    df['weighted_runners_on'] = df['on_first'].astype(int) + 2*df['on_second'].astype(int) + 3*df['on_third'].astype(int)
    
    
    # Home or away
    def home_or_away(x):
        if x == 'top':
            return 'Home'
        else:
            return 'Away'
    
    df['home_or_away'] = df['inning_half'].apply(home_or_away)
    

    # Save dataframe as csv
    pitcher_num = df['pitcher_id'].unique()[0]
    print(pitcher_num)
    sys.stdout.flush()
    variable_name = 'individual_df/' + str(pitcher_num) + '_fe.csv'
    df.to_csv(variable_name,index = False)
    
