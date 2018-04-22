import pandas as pd
import numpy as np
import argparse

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', help = 'input data path')
args = parser.parse_args()

df = pd.read_csv(args.input)

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

## Pitch count -> Can delete once incorporated into cleaning
#df['pitch_count'] = 0
#
#pitch_count = {}
#
#pitcher_id_col = column_idx(df, 'pitcher_id')
#pitch_count_col = column_idx(df, 'pitch_count')
#game_col = column_idx(df, 'game_id')
#
#last_game = df.loc[0, 'game_id']
#
#i = 0
#while i < len(df):
#    game = df.iat[i, game_col]
#
#    if game != last_game:
#        pitch_count = {} # Reset dictionary for new game
#        last_game = game
#        continue # Don't increase i. At next iteration, game == last_game on the same row
#
#    pitcher_id = df.iat[i, pitcher_id_col]
#
#    if pitcher_id in pitch_count:
#        df.iat[i, pitch_count_col] = pitch_count[pitcher_id]
#        pitch_count[pitcher_id] += 1
#    else:
#        pitch_count[pitcher_id] = 1
#
#    i += 1


# Prior pitch, prior location, prior result
df['prior_pitch'] = ''
df['prior_px'] = np.inf
df['prior_py'] = np.inf
#df['prior_result'] = ''

game_col = column_idx(df, 'game_id')
prior_pitch_col = column_idx(df, 'prior_pitch')
prior_x_loc_col = column_idx(df, 'prior_px')
prior_y_loc_col = column_idx(df, 'prior_py')
ab_col = column_idx(df, 'ab_game_num')
pitch_col = column_idx(df, 'pitch_type')
x_loc_col = column_idx(df, 'px')
y_loc_col = column_idx(df, 'py')
#prior_result_col = column_idx(df, 'prior_result')

last_pitch = ''
last_x_loc = np.inf 
last_y_loc = np.inf
last_game = df.iat[0, game_col]
last_ab = df.iat[0, ab_col]

i = 0
while i < len(df):
    game = df.iat[i, game_col]
    ab = df.iat[i, ab_col]

    if ab != last_ab or game != last_game:
  
        last_pitch = ''
        last_x_loc = np.inf
        last_y_loc = np.inf
        last_ab = ab
        last_game = game
        continue
     
    df.iat[i, prior_pitch_col] = last_pitch 
    df.iat[i, prior_x_loc_col] = last_x_loc
    df.iat[i, prior_y_loc_col] = last_y_loc

    last_pitch = df.iat[i, pitch_col]
    last_x_loc = df.iat[i, x_loc_col]
    last_y_loc = df.iat[i, y_loc_col]

    last_ab = ab
    last_game = game

    i += 1

##### Global Pitch Frequencies #####

# Find 2014 frequencies
df = df.loc[~(df['pitch_type'].isnull()), :].reset_index() # remove this line when going through the proper pipeline

temp = df.loc[df['year'] == 2014, :]
pitch_freq = temp.groupby('pitch_type')['home_team'].count().reset_index()
pitch_freq.rename(columns = {'home_team':'count'}, inplace = True)
pitch_types_2014 = pitch_freq['pitch_type'].values.tolist()

train_years = [2015, 2016]
temp2 = df.loc[df['year'].isin(train_years), :]
train_pitch_types = df['pitch_type'].unique().tolist()

pitch_count_dict = {}
prior_columns = []
for pitch_type in train_pitch_types:
    col_name = 'global_prior_' + pitch_type
    prior_columns.append(col_name)
    if pitch_type in pitch_types_2014:
        pitch_count_dict[pitch_type] = pitch_freq.loc[pitch_freq['pitch_type'] == pitch_type, 'count'].values[0]
    else:
        pitch_count_dict[pitch_type] = 0

# Create null columns for each pitch type
for col in prior_columns:
    df[col] = np.nan

i = temp2.index.values[0] # First pitch of 2015
while i < df.index.values[-1]:
    pitch_type = df.loc[i, 'pitch_type']
    column_name = 'global_prior_' + pitch_type
    if pitch_type in pitch_count_dict:
        pitch_count_dict[pitch_type] += 1
        df.loc[i+1, column_name] = pitch_count_dict[pitch_type]
    else: # Have not checked this code for new pitch types in test set
        pitch_count_dict[pitch_type] = 0
        df[column_name] = np.nan
        prior_column.append(column_name)
        continue
    
    i += 1

# Forward fill null values in prior columns, backfill the 2014 values
for col in prior_columns:
    df[col].fillna(method = 'ffill', inplace = True)
    df[col].fillna(method = 'bfill', inplace = True)

totals = df.loc[:, prior_columns].sum(axis = 1)
df['total_pitches'] = totals
print(df.loc[:, ['global_prior_SL', 'global_prior_IN', 'global_prior_CH', 'global_prior_FT', 'global_prior_FF', 'total_pitches']])

# Create global percentage columns
for col in prior_columns:
    column_name = col + '_percent'
    df[column_name] = np.nan




