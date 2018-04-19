import pandas as pd
import numpy as np
import sys

df = pd.read_csv('test.csv')

starters = []

# Simplyfy it to starters vs relievers
# Starters throw the first pitch of the first inning

# Function to return index of column
def column_idx(df, column_name):
    return df.columns.values.tolist().index(column_name)

# Flag the start of a new game
df['game_shift'] = df['game_id'].shift(1).fillna(df['game_id'])
df['new_game'] = df['game_id'] != df['game_shift']
new_game_idx = df.loc[df['new_game'] == True, :].index.values.tolist()

if df.loc[0, 'inning_half'] == 'top' and df.loc[0, 'inning'] == 1 and df.loc[0, 'ab_game_num'] == 1:
    df.loc[0, 'new_game'] = True
    new_game_idx_list = [0] + new_game_idx


for idx in new_game_idx_list:
    inning = df.loc[idx, 'inning']
    if inning != 1:
        continue
    
    pitcher = df.loc[idx, 'pitcher_id']
    if pitcher not in starters:
        starters.append(pitcher)

    i = idx + 3
    while inning == 1:
        inning = df.loc[i, 'inning']
        inning_h = df.loc[i, 'inning_half']
        if inning_h == 'bottom':
            pitcher = df.loc[i, 'pitcher_id']
            if pitcher not in starters:
                starters.append(pitcher)
                continue
                
        i += 1

# Tag the starters vs relievers
def StartVsRelief(pitcher_id):
    if pitcher_id in starters:
        return 'Starter'
    else:
        return 'Reliever'

df['StartVsRelief'] = df['pitcher_id'].apply(StartVsRelief)

#### Manipulate data for visualisations (R) ####

# Games played
temp = df[['pitcher_id', 'StartVsRelief', 'game_id', 'pitch_type']]

gamesplayed_df = temp.drop_duplicates()
gamesplayed_df.drop(['pitch_type'], axis = 1, inplace = True)
gamesplayed_df = gamesplayed_df.groupby(['pitcher_id', 'StartVsRelief']).count().reset_index()
gamesplayed_df.rename(columns = {'game_id':'games_played'}, inplace = True)

gamesplayed_df.to_csv('visualisations/StarterVsClosers/games_played.csv', index = False)

# Pitchers per game
pitch_per_game_df = temp.groupby(['pitcher_id', 'game_id', 'StartVsRelief']).count().reset_index()
pitch_per_game_df.rename(columns = {'pitch_type':'pitch_count'}, inplace = True)
print(pitch_per_game_df)

pitch_per_game_df.to_csv('visualisations/StarterVsClosers/pitch_per_game.csv', index = False)

# Total pitches thrown
total_pitches = pitch_per_game_df.groupby(['pitcher_id', 'StartVsRelief']).sum().reset_index()
print(total_pitches)

total_pitches.to_csv('visualisations/StarterVsClosers/total_pitches.csv', index = False)

# Total pitches split by type
total_pitchers = temp.drop(['game_id', 'pitch_type'], axis = 1).drop_duplicates()
total_pitchers = total_pitchers.groupby(['StartVsRelief']).count().reset_index()
total_pitchers.rename(columns = {'pitcher_id':'Count'}, inplace = True)

print(total_pitchers)

total_pitchers.to_csv('visualisations/StarterVsClosers/total_pitchers.csv', index = False)

