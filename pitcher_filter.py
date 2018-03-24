import pandas as pd
import numpy as np

df = pd.read_csv('gameday_data/mlb_gameday.csv')

pitchers_list = df['pitcher_id'].unique().tolist()
print('Number of pitchers: {}'.format(len(pitchers_list)))

df['year'] = df['game_id'].str[4:8].astype(int)

pitcher_count = df.groupby(['pitcher_id', 'year'])['home'].count().reset_index()
pitcher_count.columns = ['pitcher_id', 'year', 'pitch_count']

def over_500(pitch_count_column):
    if pitch_count_column >= 500:
        return True
    else:
        return False

pitcher_count['over_500'] = pitcher_count['pitch_count'].apply(over_500)

final_pitchers = []

for pitcher in pitchers_list:
    temp = pitcher_count.loc[pitcher_count['pitcher_id'] == pitcher, :]

    # exclude pitcher if he has not pitched in all four seasons
    if len(temp) != 4:
        continue 

    # exclude pitchers which have not thrown more than 500 pitches in each season
    over_500_column = temp['over_500'].sum()
    if over_500_column != 4:
        continue

    final_pitchers.append(pitcher)

print('Number of pitchers after initial filter: {}'.format(len(final_pitchers)))

final_df = df.loc[df['pitcher_id'].isin(final_pitchers), :]
print('raw data shape: {}'.format(df.shape))
print('filtered data shape: {}'.format(final_df.shape))

final_df.to_csv('filtered_pitchers.csv', index = False)
