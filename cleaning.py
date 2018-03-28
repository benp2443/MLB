import pandas as pd
import numpy as np

df = pd.read_csv('filtered_pitchers.csv')

print(df.columns.values)

#df['home_runs'].replace(-1, np.nan, inplace = True)
#df['away_runs'].replace(-1, np.nan, inplace = True)
#
#games = df.loc[df['home_runs'].isnull(), 'game_id'].drop_duplicates().tolist()
#print(games)
#temp = df.loc[df['game_id'] == games[0], :]
#temp_idx = temp.index.values
#start_idx = temp_idx[0]
#end_idx = temp_idx[-1]
#
#start_value = temp.loc[start_idx, 'home_runs']
#
#if start_value == None:
#    temp.loc[start_idx, 'home_runs'] = 0
#
#temp['home_runs'].fillna(method = 'ffill', inplace = True)
#df.loc[temp_idx, 'home_runs'] = temp['home_runs']
#
#print(len(df.loc[(df['home_runs'].isnull()) & (df['game_id'] == games[0]), :]))
#
# Remove all star games
df = df.loc[df['season_period'] != 'A', :] 

# Drop unwanted columns
drop_columns = ['ab_start_date_time', 'ab_end_date_time', 'ab_event_number', 'season_period', 'league_home', 'league_away', \
        'cc', 'mt', 'id_', 'code', 'location', 'nasty', 'ab_event_number', 'p_time', 'x', 'y', 'balls', 'strikes', 'event_num', \
        'px', 'pz', 'x0', 'y0', 'z0', 'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 'break_y', 'break_angle', 'break_length', 'zone', \
        'spin_dir', 'spin_rate']

df = df.drop(drop_columns, axis = 1)

df.to_csv('filtered_data.csv')
#
#
## Find columns with null values and count
#columns = df.columns.values.tolist()
#
#for column in columns:
#    print('{0}: {1}'.format(column, sum(df[column].isnull())))
