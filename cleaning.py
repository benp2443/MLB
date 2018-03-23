import pandas as pd
import numpy as np

df = pd.read_csv('filtered_pitchers.csv')

print(df.columns.values)

columns = ['ab_event', 'outs', 'home_runs', 'away_runs', 'p_description', 'type']

for column in columns:
    print(df[column].unique())

## Remove all star games
#df = df.loc[df['season_period'] != 'A', :] 
#
## Drop unwanted columns
#drop_columns = ['ab_start_date_time', 'ab_end_date_time', 'ab_event_number', 'season_period', 'league_home', 'league_away', \
#        'cc', 'mt', 'id_', 'code', 'location', 'nasty', 'ab_event_number', 'p_time', 'x', 'y']
#
#df = df.drop(drop_columns, axis = 1)
#
#
## Find columns with null values and count
#columns = df.columns.values.tolist()
#
#for column in columns:
#    print('{0}: {1}'.format(column, sum(df[column].isnull())))
