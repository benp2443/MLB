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

##### Drop pitch outs and intentional balls #####

# Replace unknown pitches with null
df.replace('UN', np.nan, inplace = True)
print(df['pitch_type'].unique())

drop_pitches = ['IN', 'PO']
df = df.loc[~(df['pitch_type'].isin(drop_pitches)), :]


temp = df.loc[~(df['pitch_type'].isnull()), :]

# Replace most 'AB' with the pitchers most common pitch
print(temp.loc[temp['pitch_type'] == 'AB', ['pitcher_id', 'pitch_type', 'game_id', 'ab_game_num', 'start_speed', 'type_confidence']]) # Pitch confidence is 0.0 

print(temp.loc[df['type_confidence'].isnull(), ['game_id', 'pitch_type',]])
print(temp.loc[df['type_confidence'] == 0.0, ['game_id', 'pitch_type']])

print(len(temp.loc[df['type_confidence'] == 0.0, ['game_id', 'pitch_type']]))
print(len(temp.loc[df['type_confidence'] < 0.1, ['game_id', 'pitch_type']]))

print(temp.loc[df['type_confidence'] < 0.1, ['game_id', 'pitch_type']])
# Analysis of pitch confidence



#temp = df.loc[~(df['pitch_type'].isnull()), :]
# Visualise new pitch set
#temp = df.loc[~(df['pitch_type'].isnull()), :]
#print(temp['pitch_type'].unique())
#temp2 = temp.groupby('pitch_type')['home_team'].count().reset_index()
#temp2.columns = ['pitch_type', 'count']
#temp2.to_csv('visualisations/pitch_types/pitch_type_count.csv', index = False)
