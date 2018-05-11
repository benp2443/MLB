import pandas as pd
import numpy as np
import argparse

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs = '+', help = 'input data path')
args = parser.parse_args()

pitcher_volatility = []

for pitcher in args.input:

    df = pd.read_csv(pitcher)
    pitcher_id = df.loc[0, 'pitcher_id']

    # Pitch change between train and test
    train_test_split = {2014:'prep', 2015:'train', 2016:'train', 2017:'test'}
    
    df['train_test'] = df['year'].map(train_test_split)
    
    temp = df.loc[df['train_test'] != 'prep', :]
    
    # Calculate pitch type percentage for train and test periods
    pitch_count_df = temp.groupby(['train_test', 'pitch_type'])['home_team'].count().reset_index()
    pitch_count_df.rename(columns = {'home_team':'pitch_count'}, inplace = True)
    
    period_count_df = pitch_count_df.groupby('train_test')['pitch_count'].sum().reset_index()
    period_count_df.rename(columns = {'pitch_count':'train_test_count'}, inplace = True)
    
    percent_df = pitch_count_df.merge(period_count_df, how = 'inner', left_on = 'train_test', right_on = 'train_test')
    
    percent_df['percent'] = round((percent_df['pitch_count']/percent_df['train_test_count'])*100, 2)
    percent_df.drop(['pitch_count', 'train_test_count'], axis = 1, inplace = True)
    
    #Add columns to percent_df that are in test but not train. Set pitch percentage to 0.0
    test_pitches = percent_df.loc[percent_df['train_test'] == 'test', 'pitch_type'].values.tolist()
    train_pitches = percent_df.loc[percent_df['train_test'] == 'train', 'pitch_type'].values.tolist()
    
    df = pd.DataFrame()
    data = []
    for pitch in test_pitches:
        if pitch not in train_pitches:
            data.append(['train', pitch, 0.0])
    
    if len(data) > 0:
        df = pd.DataFrame(data, columns = percent_df.columns.values)
        percent_df = percent_df.append(df)
    
    # Drop pitch types that are in train but not test
    drop = []
    for pitch in train_pitches:
        if pitch not in test_pitches:
            drop.append(pitch)
    
    if len(drop) > 0:
        percent_df = percent_df.loc[~((percent_df['pitch_type'].isin(drop)) & (percent_df['train_test'] == 'train')), :]
    
    # Need to re-weight train so it adds up to 100% -> Make this cleaner so it doesn't happen when nothing has been dropped
    train = percent_df.loc[percent_df['train_test'] == 'train', :]
    train_sum = np.sum(train['percent'])
    train.loc[:, 'reweight_percent'] = round((train['percent']/train_sum)*100,2)
    train.drop(['train_test', 'percent'], axis = 1, inplace = True)
    
    test = percent_df.loc[percent_df['train_test'] == 'test', :]
    test.drop(['train_test'], axis = 1, inplace = True)
    
    final = train.merge(test, how = 'inner', on = 'pitch_type')

    final['square_change'] = np.square(final['percent'] - final['reweight_percent'])
    
    change_value = np.sqrt(np.mean(final['square_change']))
    
    pitcher_volatility.append([pitcher_id, change_value])

volatility_df = pd.DataFrame(pitcher_volatility, columns = ['pitcher_id', 'change_value'])

print(volatility_df)
volatility_df.to_csv('visualisations/pitch_frequencies/volatility.csv', index = False)

volatility_df.sort_values(by = ['change_value'], inplace = True)
volatility_df = volatility_df.reset_index()

# Find four pitchers from the top and bottom 10%
length = len(volatility_df)
bottom_10_idx = int(length*0.1)
top_10_idx = int(length*0.9)

bottom_10_df = volatility_df.loc[0:bottom_10_idx, :]
top_10_df = volatility_df.loc[top_10_idx:, :]

pitchers_bottom = bottom_10_df.sample(n = 4, random_state = 1)['pitcher_id'].values.tolist()
pitchers_top = top_10_df.sample(n = 4, random_state = 1)['pitcher_id'].values.tolist()

def name_later(list_name):

    df2 = pd.DataFrame()

    for pitcher in list_name:
        file_path = 'individual_df/' + str(pitcher) + '.csv'
        df = pd.read_csv(file_path)
        
        train_test_split = {2014:'prep', 2015:'train', 2016:'train', 2017:'test'}
        df['train_test'] = df['year'].map(train_test_split)
        temp = df.loc[df['train_test'] != 'prep', :]

        temp = temp.groupby(by = ['train_test', 'pitch_type'])['home_team'].count().reset_index()
        temp.rename(columns = {'home_team':'count'}, inplace = True)

        temp2 = temp.groupby(by = 'train_test')['count'].sum().reset_index()
        temp2.rename(columns = {'count':'pitches_thrown'}, inplace = True)

        temp3 = temp.merge(temp2, how = 'inner', on = 'train_test')

        temp3['percent'] = round((temp3['count']/temp3['pitches_thrown'])*100,2)

        temp3['pitcher_id'] = pitcher

        if len(df2) == 0:
            df2 = temp3
        else:
            df2 = pd.concat([df2, temp3])

    return df2


bottom_df = name_later(pitchers_bottom)
top_df = name_later(pitchers_top)

print(bottom_df)
print(top_df)

bottom_df.to_csv('visualisations/pitch_frequencies/bottom_vol.csv', index = False)
top_df.to_csv('visualisations/pitch_frequencies/top_vol.csv', index = False)

#temp = df.groupby(by = ['game_id', 'pitch_type'])['home_team'].count().reset_index()
#temp.rename(columns = {'home_team':'pitch_type_count'}, inplace = True)
#
#temp2 = temp.groupby(by = 'game_id')['pitch_type_count'].sum().reset_index()
#temp2.rename(columns = {'pitch_type_count':'pitch_count'}, inplace = True)
#
#pitch_freqs = temp.merge(temp2, how = 'inner', left_on = 'game_id', right_on = 'game_id')
#
#pitch_freqs['percentage'] = round((pitch_freqs['pitch_type_count']/pitch_freqs['pitch_count'])*100,2)
#pitch_freqs['year'] = pitch_freqs['game_id'].str[4:8]
#
#pitch_freqs.to_csv('visualisations/pitch_frequencies/pitch_freq_changes.csv', index = False)
#
#pitch_freqs2 = pitch_freqs.groupby(['year', 'pitch_type'])['percentage'].mean().reset_index()
#print(pitch_freqs2)
#pitch_freqs2.to_csv('visualisations/pitch_frequencies/pitch_freq_yearly_changes.csv', index = False)
#
