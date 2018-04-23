import pandas as pd
import numpy as np
import argparse

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', help = 'input data path')
args = parser.parse_args()

df = pd.read_csv(args.input)

# Function to return index of column
def column_idx(df, column_name):
    return df.columns.values.tolist().index(column_name)

#Pitch count -> Can delete once incorporated into cleaning
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


for col in df.columns.values:
    print(col)

####### Visualise ########
years = [2014, 2015, 2016]
temp = df.loc[(df['year'].isin(years) & (df['pitch_type'] == 'FF')), :]
temp['pitch_count_bucket'] = (temp['pitch_count']/10).astype(int)
temp.to_csv('visualisations/speed_change/FF_speed.csv', index = False)
temp2 = temp.groupby(['pitch_count_bucket'])['start_speed'].mean().reset_index()
print(temp2)


