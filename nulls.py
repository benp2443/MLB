import pandas as pd
import numpy as np
pd.set_option('max.rows', 500)

df = pd.read_csv('mlb_gd_full.csv')

##### Filter pitchers #####

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

print('Number of pitchers after filter: {}'.format(len(final_pitchers)))

# Filter df to only include pitchers who met the requirements 
df = df.loc[df['pitcher_id'].isin(final_pitchers), :]


pitcher_per_game = df.groupby(['game_id', 'pitcher_id'])['home_team'].count().reset_index()
pitcher_per_game.rename(columns = {'home_team':'pitch_total'}, inplace = True)
nulls_df = df.loc[df['pitch_type'].isnull(), :]
nulls_per_game = nulls_df.groupby(['game_id', 'pitcher_id'])['home_team'].count().reset_index()
nulls_per_game.rename(columns = {'home_team':'null_total'}, inplace = True)

final = pitcher_per_game.merge(nulls_per_game, how = 'left', on = ['game_id', 'pitcher_id'])
final['null_total'].fillna(0, inplace = True)

final['null_percentage'] = final['null_total']/final['pitch_total']
ten_percent_null = final.loc[final['null_percentage'] > 0.1, :].reset_index()

print(len(final))
print(len(ten_percent_null))

pitchers = ten_percent_null['pitcher_id'].values
games = ten_percent_null['game_id'].values

i = 0
while i < len(pitchers):
    pitcher = pitchers[i]
    game_id = games[i]

    df = df.loc[~((df['pitcher_id'] == pitcher) & (df['game_id'] == game_id)), :]
    
    i += 1

df.reset_index(inplace = True)

columns = df.columns.values.tolist()
##### Pitch type nulls #####
print('Null Values', '\n')
for col in columns:
    null_values = df[col].isnull().sum()
    if null_values > 0:
        print(col)
        print(df[col].isnull().sum())

