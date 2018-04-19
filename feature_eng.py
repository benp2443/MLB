import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

df = pd.read_csv('test.csv')

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

# Pitch count
df['pitch_count'] = 0

pitch_count = {}

pitcher_id_col = column_idx(df, 'pitcher_id')
pitch_count_col = column_idx(df, 'pitch_count')
game_col = column_idx(df, 'game_id')

last_game = df.loc[0, 'game_id']

i = 0
while i < len(df):
    game = df.iat[i, game_col]

    if game != last_game:
        pitch_count = {} # Reset dictionary for new game
        last_game = game
        continue # Don't increase i. At next iteration, game == last_game on the same row

    pitcher_id = df.iat[i, pitcher_id_col]

    if pitcher_id in pitch_count:
        df.iat[i, pitch_count_col] = pitch_count[pitcher_id]
        pitch_count[pitcher_id] += 1
    else:
        pitch_count[pitcher_id] = 1

    i += 1

# Prior pitch, prior location, prior result
df['prior_pitch'] = ''
df['prior_px'] = np.inf
df['prior_py'] = np.inf
#df['prior_result'] = ''

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

# TBC
