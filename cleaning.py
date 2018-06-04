import pandas as pd
import numpy as np
import sys

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

# Create column which is True if pitcher threw over 500 pitches for that year and False otherwise
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
print('Through pitcher filter')
sys.stdout.flush()

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

prev_base_sum = df.iat[0, on_first_col].astype(int) + df.iat[0, on_second_col].astype(int) + \
                df.iat[0, on_third_col].astype(int) # With the filtered df, games/innings may start with runners on base
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

print('Outs updated')
sys.stdout.flush()

##### Drop pitch outs and intentional balls #####

drop_pitches = ['IN', 'PO']
df = df.loc[~(df['pitch_type'].isin(drop_pitches)), :].reset_index(drop = True)

##### Replace pitch type 'FA' with 'FF' #####
df.replace('FA', 'FF', inplace = True)

##### Replace unknown (UN) pitch types or pitches with 0.0 confidence with null #####

df.replace('UN', np.nan, inplace = True)

zero_confidence_idx = df.loc[(df['type_confidence'] == 0.0) & (~df['pitch_type'].isnull()), ].index.values
df.loc[zero_confidence_idx, 'pitch_type'] = np.nan

###### Add game pitch count and at bat pitch count columns before removing rows #####

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
        pitch_count[pitcher_id] = 1 # pitch count already set to 0, so don't need to set here

    i += 1


df['ab_pitch_count'] = -1

ab_pitch_count_col = column_idx(df, 'ab_pitch_count')
at_bat_col = column_idx(df, 'ab_game_num')

last_ab_num = -1
last_game = ''

pitch_count = 0

i = 0
while i < len(df):
    ab_num = df.iat[i, at_bat_col]
    game = df.iat[i, game_col]

    if ab_num != last_ab_num or game != last_game:
        pitch_count = 0
        last_game = game
        last_ab_num = ab_num
        continue
    else:
        df.iat[i, ab_pitch_count_col] = pitch_count
        pitch_count += 1

    i += 1

print('game and at bat count added')
sys.stdout.flush()

###### Prior pitch, prior location, prior result #####

df['prior_pitch'] = ''
df['prior_px'] = np.inf
df['prior_py'] = np.inf
df['prior_speed'] = np.inf

game_col = column_idx(df, 'game_id')
prior_pitch_col = column_idx(df, 'prior_pitch')
prior_x_loc_col = column_idx(df, 'prior_px')
prior_y_loc_col = column_idx(df, 'prior_py')
prior_pitch_speed_col = column_idx(df, 'prior_speed')
ab_col = column_idx(df, 'ab_game_num')
pitch_col = column_idx(df, 'pitch_type')
x_loc_col = column_idx(df, 'px')
y_loc_col = column_idx(df, 'py')
speed_col = column_idx(df, 'start_speed')

last_pitch = ''
last_x_loc = np.inf 
last_y_loc = np.inf
last_speed = np.inf
last_game = df.iat[0, game_col]
last_ab = df.iat[0, ab_col]

i = 0
while i < len(df):
    game = df.iat[i, game_col]
    ab = df.iat[i, ab_col]

    if ab != last_ab or game != last_game:
  
        last_pitch = ''
        last_x_loc = np.inf
        last_y_loc = np.inf
        last_speed = np.inf
        last_ab = ab
        last_game = game
        continue
     
    df.iat[i, prior_pitch_col] = last_pitch 
    df.iat[i, prior_x_loc_col] = last_x_loc
    df.iat[i, prior_y_loc_col] = last_y_loc
    df.iat[i, prior_pitch_speed_col] = last_speed

    last_pitch = df.iat[i, pitch_col]
    last_x_loc = df.iat[i, x_loc_col]
    last_y_loc = df.iat[i, y_loc_col]
    last_speed = df.iat[i, speed_col]

    last_ab = ab
    last_game = game

    i += 1

print('priors added')
sys.stdout.flush()
##### Pitch type nulls #####

nulls_df = df.loc[df['pitch_type'].isnull(), :]

# Calculate amount of null pitch types per year
nulls_by_year = nulls_df.groupby(['year'])['home_team'].count().reset_index()
nulls_by_year.rename(columns = {'home_team':'nulls'}, inplace = True)
nulls_by_year['type'] = 'Total nulls'

# Calculate the amount of games with nulls, split by year
nulls_df2 = nulls_df.loc[:, ['year', 'game_id', 'home_team']].drop_duplicates()
games_with_nulls = nulls_df2.groupby(['year'])['home_team'].count().reset_index()
games_with_nulls.rename(columns = {'home_team':'nulls'}, inplace = True)
games_with_nulls['type'] = 'Games with nulls'

# Join the two dataframes above to allow for a side by side plot of data in r
nulls_df3 = pd.concat([nulls_by_year, games_with_nulls], axis = 0)
print(nulls_df3)
nulls_df3.to_csv('visualisations/nulls/pitch_type_nulls.csv', index = False)

# Calculate nulls per game (for games with nulls), split by year
nulls_by_game = nulls_df.groupby(['year', 'game_id'])['home_team'].count().reset_index()
nulls_by_game.rename(columns = {'home_team':'nulls'}, inplace = True)
nulls_by_game.to_csv('visualisations/nulls/nulls_by_game.csv', index = False)

# Calculate the amount of consecutive nulls 
null_idx = nulls_df.index.values.tolist()
i = 0
count = 0
consec_nulls = []
while i < len(null_idx) - 1:
    if null_idx[i+1] - null_idx[i] == 1:
        count += 1
    else:
        consec_nulls.append(count)
        count = 0
         
    i += 1

consec_nulls = pd.DataFrame(consec_nulls, columns = ['consec_nulls'])
consec_nulls.to_csv('visualisations/nulls/consec_nulls.csv', index = False)

# dropping pitchers with too many null pitch types in a game
#games = nulls_df['game_id'].unique().tolist()
#
#for game in games:
#    temp = nulls_df.loc[nulls_df['game_id'] == game, :]
#    pitchers = temp['pitcher_id'].unique().tolist()
#    for pitcher in pitchers:
#        # Calculate amount of nulls for the specific pitcher in the game
#        pitcher_df = temp.loc[temp['pitcher_id'] == pitcher, :]
#        nulls = float(len(pitcher_df))
#
#        # Calculate the amount of pitchers thrown by the pitcher in the game
#        full_df = df.loc[((df['pitcher_id'] == pitcher) & (df['game_id'] == game)), :]
#        pitches_thrown = float(len(full_df))
#
#        # Calculate null percent for game
#        null_percent = nulls/pitches_thrown
#
#        if null_percent > 0.10:
#            nulls_in_full = full_df.loc[full_df['pitch_type'].isnull(), :].index.values.tolist()
#            df = df.drop(nulls_in_full, axis = 0)
#

# Delete rows with null pitch types
df = df.loc[~(df['pitch_type'].isnull()), :].reset_index(drop = True)

# train and test split
data_split = {2014:'pre', 2015:'train', 2016:'train', 2017:'test'}
df['train_test'] = df['year'].map(data_split)

# Replace NA values for prior pitch, prior_px, prior_py
df['prior_py'].replace(np.inf, np.nan, inplace = True)
df['prior_px'].replace(np.inf, np.nan, inplace = True)
df['prior_pitch'].replace('', np.nan, inplace = True)

mean_px = df.loc[df['train_test'] == 'train', 'prior_px'].mean()
mean_py = df.loc[df['train_test'] == 'train', 'prior_py'].mean()
mode_type = df.loc[df['train_test'] == 'train', 'prior_pitch'].mode()[0]

df['prior_py'].replace(np.nan, mean_py, inplace = True)
df['prior_px'].replace(np.nan, mean_px, inplace = True)
df['prior_pitch'].replace(np.nan, mode_type, inplace = True)

columns = df.columns.values.tolist()

###### Starters vs Closers ######
# Flag the start of a new game
df.reset_index(drop = True, inplace = True)

df['game_shift'] = df['game_id'].shift(1).fillna(df['game_id'])
df['new_game'] = df['game_id'] != df['game_shift']
new_game_idx = df.loc[df['new_game'] == True, :].index.values.tolist()

if df.loc[0, 'inning_half'] == 'top' and df.loc[0, 'inning'] == 1 and df.loc[0, 'ab_game_num'] == 1:
    df.loc[0, 'new_game'] = True
    new_game_idx_list = [0] + new_game_idx
else:
    new_game_idx_list = new_game_idx

starters = []
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
                
            break
                
                
        i += 1

# Tag the starters vs relievers
def StartVsRelief(pitcher_id):
    if pitcher_id in starters:
        return 'Starter'
    else:
        return 'Reliever'

df['StartVsRelief'] = df['pitcher_id'].apply(StartVsRelief)

print('Null Values', '\n')
for col in df.columns.values.tolist():
    null_values = df[col].isnull().sum()
    if null_values > 0:
        print(col)
        print(df[col].isnull().sum())

# Output seperate dataframe's for each pitcher
pitchers = df['pitcher_id'].unique().tolist()

for pitcher in pitchers:
    temp = df.loc[df['pitcher_id'] == pitcher, :].reset_index(drop = True)
    file_path = 'individual_df/' + str(pitcher) + '.csv'
    temp.to_csv(file_path, index = False)
