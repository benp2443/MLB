import pandas as pd
import numpy as np
import argparse
import sys

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs = '+', help = 'input data path')
args = parser.parse_args()

team_counts = {}
number_of_pitch_types = []
games_played = []
ppg_df = pd.DataFrame([], columns = ['count', 'StarterVsCloser'])
left_count = 0
right_count = 0
pitch_types_count_dict = {}

for pitcher in args.input:
    df = pd.read_csv(pitcher)
    last_index = len(df) - 1
    
    # Assign pitcher to last team they played for
    if df.loc[last_index, 'inning_half'] == 'top':
        team = df.loc[last_index, 'home_team']
    else:
        team = df.loc[last_index, 'away_team']

    if team in team_counts:
        team_counts[team] += 1
    else:
        team_counts[team] = 1

    # Number of pitch types
    unique_pitch_types = df['group_pitch_type'].unique()
    pitches = len(unique_pitch_types)
    p_type = df.loc[0, 'StartVsRelief']
    number_of_pitch_types.append([pitches, p_type]) 

    # Total games
    g_played = len(df['game_id'].unique())
    games_played.append([g_played, p_type])

    # Pitches per game
    p_per_game = df.groupby('game_id')['home_team'].count().reset_index()
    p_per_game.rename(columns = {'home_team':'count'}, inplace = True)
    p_per_game['StarterVsCloser'] = p_type
    p_per_game.drop(['game_id'], axis = 1, inplace = True)
    ppg_df = pd.concat([ppg_df, p_per_game], axis = 0)

    # Left verse Right
    hand = df.loc[0, 'p_handedness']
    if hand == 'R':
        right_count += 1
    else:
        left_count += 1

    # Pitch types
    for pitch_type in unique_pitch_types:
        print(pitch_type)
        if pitch_type in pitch_types_count_dict:
            pitch_types_count_dict[pitch_type] += 1
        else:
            pitch_types_count_dict[pitch_type] = 1



teams_list = []
for key, value in team_counts.items():
    temp = [key,value]
    teams_list.append(temp)
    
df = pd.DataFrame(teams_list, columns = ['team', 'count'])
#print('teams')
#print(df, '\n')
df.to_csv('visualisations/exploratory_analysis/teams.csv', index = False)

pitch_types_count = pd.DataFrame(number_of_pitch_types, columns = ['count', 'StarterVsCloser'])
#print('number of pitch types')
#print(pitch_types_count, '\n')
pitch_types_count.to_csv('visualisations/exploratory_analysis/pitch_type_counts.csv', index = False)

ppg_df.reset_index(drop = True, inplace = True)
#print('pitches per game')
#print(ppg_df)
ppg_df.to_csv('visualisations/exploratory_analysis/pitches_per_game.csv', index = False)

hand_df = pd.DataFrame([['Right', right_count],['Left', left_count]], columns = ['hand', 'count'])
#print(hand_df)
hand_df.to_csv('visualisations/exploratory_analysis/handedness.csv', index = False)

gp_df = pd.DataFrame(games_played, columns = ['count', 'StarterVsCloser'])
#print(gp_df)
gp_df.to_csv('visualisations/exploratory_analysis/games_played.csv', index = False)

pitch_type_list = []
for key, value in pitch_types_count_dict.items():
    temp = [key, value]
    pitch_type_list.append(temp)

type_df = pd.DataFrame(pitch_type_list, columns = ['Pitch_Type', 'Count'])
type_df = type_df.loc[~type_df['Pitch_Type'].isnull(), :]
type_df.to_csv('visualisations/exploratory_analysis/pitch_types.csv', index = False)
