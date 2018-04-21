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
pitcher_count = df.groupby(['pitcher_id', 'year'])['home'].count().reset_index()
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
    if over_500_column != 4:
        continue

    final_pitchers.append(pitcher)

print('Number of pitchers after filter: {}'.format(len(final_pitchers)))

# Filter df to only include pitchers who met the requirements 
df = df.loc[df['pitcher_id'].isin(final_pitchers), :]

##### Replace null home and away run values #####

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

##### Update outs for when base runners get caught stealing or picked off #####

columns = df.columns.values.tolist()

# Function to return index of column
def column_idx(df, column_name):
    return df.columns.values.tolist().index(column_name)

df['outs_test'] = df['outs']

on_first_col = column_idx(df, 'on_first')
on_second_col = column_idx(df, 'on_second')
on_third_col = column_idx(df, 'on_third')
ab_col = column_idx(df, 'ab_game_num')
outs_col = column_idx(df, 'outs')
outs_test_col = column_idx(df, 'outs_test')

prev_base_sum = df.iat[0, on_first_col].astype(int) + df.iat[0, on_second_col].astype(int) + df.iat[0, on_third_col].astype(int) # With the filtered df, games/innings may start with runners on base
prev_ab = df.iat[0, ab_col]
ab_start_outs = df.iat[0, outs_col]
run_out = 0

i = 0
while i < len(df):
    base_sum = df.iat[i, on_first_col].astype(int) + df.iat[i, on_second_col].astype(int) + df.iat[i, on_third_col].astype(int)
    ab = df.iat[i, ab_col]

    if ab != prev_ab:
        ab_start_outs = df.iat[i, outs_col]
        run_out = 0

    if ab == prev_ab and base_sum != prev_base_sum:
        run_out += 1

    if ab == prev_ab and run_out > 0:
        df.iat[i, outs_test_col] = ab_start_outs + run_out

    prev_base_sum = base_sum
    prev_ab = ab

    i += 1

# Can delete the column below I think
df['diff'] = df['outs_test'] - df['outs']

##### Look at pitch types and remove pitch outs #####


