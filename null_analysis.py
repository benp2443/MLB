import pandas as pd
import numpy as np
import sys

pd.set_option('max.rows', 500)

df = pd.read_csv('mlb_gd_full.csv')

# Create list of pitcher id's
pitchers_list = df['pitcher_id'].unique().tolist()
print('Number of pitchers: {}'.format(len(pitchers_list)))

# Create year column
df['year'] = df['game_id'].str[4:8].astype(int)

# Create dataframe which has the pitcher id, year, and number of pitchers thrown in each row
pitcher_count = df.groupby(['pitcher_id', 'year'])['home_team'].count().reset_index()
pitcher_count.columns = ['pitcher_id', 'year', 'pitch_count']

# Create column which is True if pitcher threw over 500 pitchers for that year and null otherwise
def over_500(pitch_count_column):
    if pitch_count_column >= 500:
        return True
    else:
        return False

pitcher_count['over_500'] = pitcher_count['pitch_count'].apply(over_500)

# Filter pitchers based on years played and pitchers thrown per season
final_pitchers = []

for pitcher in pitchers_list:
    temp = pitcher_count.loc[pitcher_count['pitcher_id'] == pitcher, :]

    # exclude pitcher if he has not pitched in all four seasons
    if len(temp) != 4:
        continue 

    # exclude pitchers which have not thrown more than 500 pitches in each season
    years_over_500_column = temp['over_500'].sum()
    if years_over_500_column != 4:
        continue

    final_pitchers.append(pitcher)

print('Number of pitchers after filter: {}'.format(len(final_pitchers)), '\n')

# Filter df to only include pitchers who met the requirements 
df = df.loc[df['pitcher_id'].isin(final_pitchers), :]
print('Length of filtered df')
print(len(df), '\n')

columns = df.columns.values.tolist()

# Function to return index of column
def column_idx(df, column_name):
    return df.columns.values.tolist().index(column_name)

##### Null Analysis #####
print('Null Values', '\n')
for col in columns:
    null_values = df[col].isnull().sum()
    if null_values > 0:
        print(col)
        print(df[col].isnull().sum())
print('')

nulls_df = df.loc[df['pitch_type'].isnull(), :]

nulls_by_year = nulls_df.groupby(['year'])['home_team'].count().reset_index()
nulls_by_year.rename(columns = {'home_team':'nulls'}, inplace = True)
nulls_by_year['type'] = 'Total nulls'
print(nulls_by_year)

nulls_df2 = nulls_df.loc[:, ['year', 'game_id', 'home_team']].drop_duplicates()
games_with_nulls = nulls_df2.groupby(['year'])['home_team'].count().reset_index()
games_with_nulls.rename(columns = {'home_team':'nulls'}, inplace = True)
games_with_nulls['type'] = 'Games with nulls'
print(games_with_nulls)

nulls_df3 = pd.concat([nulls_by_year, games_with_nulls], axis = 0)
print(nulls_df3)
nulls_df3.to_csv('visualisations/nulls/pitch_type_nulls.csv', index = False)

nulls_by_game = nulls_df.groupby(['year', 'game_id'])['home_team'].count().reset_index()
nulls_by_game.rename(columns = {'home_team':'nulls'}, inplace = True)
nulls_by_game.to_csv('visualisations/nulls/nulls_by_game.csv', index = False)

## dropping pitchers with too many null pitch_types in a game
games = nulls_df['game_id'].unique().tolist()

for game in games:
    print(game)
    temp = nulls_df.loc[nulls_df['game_id'] == game, :]
    pitchers = temp['pitcher_id'].unique().tolist()
    for pitcher in pitchers:
        pitcher_df = temp.loc[temp['pitcher_id'] == pitcher, :]
        pitches_thrown = float(len(pitcher_df))
        nulls = float(len(pitcher_df.loc[pitcher_df['pitch_type'].isnull(), :]))
        null_percent = nulls/pitches_thrown

        if null_percent > 0.20:
            df = df.loc[~((df['game_id'] == game) & (df['pitcher_id'] == pitcher)), :]
            print(nulls)
            print(pitches_thrown)
            print(null_percent)
        



#temp = df.loc[df['pitch_type'].isnull(), :]
#games = temp['game_id'].values.tolist()
#unique_games = set(games)
#for game in unique_games:
#    print(game)
#
#test = df.loc[~(df['pitch_type'].isnull()), :]
#for col in columns:
#    print(col)
#    print(test[col].isnull().sum(), '\n')
#
#df['ab_event_num'] = df['ab_event_number'].astype(int)
#df['event_num'] = df['event_num'].astype(int)
#df['zone'] = df['zone'].astype(int)
#
#for col in columns:
#    print(col)
#    print(df.loc[0, col])
#    print(type(df.loc[0, col]), '\n')
