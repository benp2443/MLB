import pandas as pd
import numpy as np
pd.set_option('max.rows', 500)

df = pd.read_csv('filtered_data.csv')

df = df.drop(['Unnamed: 0'], axis = 1)
columns = df.columns.values.tolist()
print(columns)

## Remove all star games
#df = df.loc[df['season_period'] != 'A', :] 
#
## Drop unwanted columns
#drop_columns = ['ab_start_date_time', 'ab_end_date_time', 'ab_event_number', 'season_period', 'league_home', 'league_away', \
#        'cc', 'mt', 'id_', 'code', 'location', 'nasty', 'ab_event_number', 'p_time', 'x', 'y', 'balls', 'strikes', 'event_num', \
#        'px', 'pz', 'x0', 'y0', 'z0', 'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 'break_y', 'break_angle', 'break_length', 'zone', \
#        'spin_dir', 'spin_rate']
#
#df = df.drop(drop_columns, axis = 1)

# Replace null home and away run values

df['home_runs'].replace(-1, np.nan, inplace = True)
df['away_runs'].replace(-1, np.nan, inplace = True)

def replace_run_nulls(df, HomeOrAway_runs, game_id_column):

        games = df.loc[df[HomeOrAway_runs].isnull(), game_id_column].drop_duplicates().tolist()

        for game in games:
                temp = df.loc[df['game_id'] == game, :]
                temp_idx = temp.index.values
                start_idx = temp_idx[0]
                start_value = temp.loc[start_idx, HomeOrAway_runs]
                
                # If the first value is null, replace with 0
                if (pd.isnull(start_value)):
                        temp.loc[start_idx, HomeOrAway_runs] = 0

                # Forward fill the null value by using the most recent recorded non null value during the game
                temp[HomeOrAway_runs].fillna(method = 'ffill', inplace = True)
                df.loc[temp_idx, HomeOrAway_runs] = temp[HomeOrAway_runs]

replace_run_nulls(df, 'home_runs', 'game_id')
replace_run_nulls(df, 'away_runs', 'game_id')

# Update outs for when base runners get caught stealing or picked off

df['test_outs'] = df['outs']

i = 0
while i < len(df):
        prev = df.loc[i, 'ab_game_num']
        next_ = df.loc[i+1, 'ab_game_num']

        if next_ - prev > 1:
                print(next_ - prev)

        i += 1
                
                
