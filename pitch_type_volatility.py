import pandas as pd
import numpy as np
import argparse
import sys

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs = '+', help = 'input data path')
args = parser.parse_args()

def volatility_calc(df):

    # Remove 2014 from the data
    train_test_split = {2014:'prep', 2015:'train', 2016:'train', 2017:'test'}    
    df['train_test'] = df['year'].map(train_test_split)
    temp = df.loc[df['train_test'] != 'prep', :]
     
    # Create new dataframes - pitch type column from training set and add another column of zeros. Do the same for test set
    temp2 = pd.DataFrame(temp.loc[temp['train_test'] == 'train', 'group_pitch_type'].values, columns = ['group_pitch_type'])
    temp2['count_train'] = 0
    temp3 = pd.DataFrame(temp.loc[temp['train_test'] == 'test', 'group_pitch_type'].values, columns = ['group_pitch_type'])
    temp3['count_test'] = 0
    
    # Group the df's above on the pitch type and use added column to sum the grouped counts
    train_grouped = temp2.groupby('group_pitch_type').count().reset_index()
    test_grouped = temp3.groupby('group_pitch_type').count().reset_index()
    
    # Merge df's on pitch type. Outer join so nulls occur where the same pitch type is not in both df's
    merged_df = train_grouped.merge(test_grouped, how = 'outer', on = 'group_pitch_type')
    merged_df.fillna(0.0, inplace = True) # Fill nulls with 0.0
    
    # Find length of each dataset
    count_train = np.sum(merged_df['count_train'])
    count_test = np.sum(merged_df['count_test'])
    
    # Find Percentage of each pitch type
    merged_df['percent_train'] = merged_df['count_train']/count_train
    merged_df['percent_test'] = merged_df['count_test']/count_test
    
    # Find square difference then the change
    merged_df['sq_diff'] = np.square(merged_df['percent_train'] - merged_df['percent_test'])
    change = np.sqrt(np.mean(merged_df['sq_diff']))
    return change

pitcher_volatility = []

for pitcher in args.input:

    df = pd.read_csv(pitcher)
    pitcher_id = df.loc[0, 'pitcher_id']
    print(pitcher_id)
    sys.stdout.flush()
    volatility = volatility_calc(df)
    pitcher_volatility.append([pitcher_id, volatility])

volatility_df = pd.DataFrame(pitcher_volatility, columns = ['pitcher_id', 'change_value'])

print(volatility_df)
volatility_df.to_csv('visualisations/pitch_frequencies/volatility.csv', index = False)

#volatility_df.sort_values(by = ['change_value'], inplace = True)
#volatility_df = volatility_df.reset_index()
#
## Find four pitchers from the top and bottom 10%
#length = len(volatility_df)
#bottom_10_idx = int(length*0.1)
#top_10_idx = int(length*0.9)
#
#bottom_10_df = volatility_df.loc[0:bottom_10_idx, :]
#top_10_df = volatility_df.loc[top_10_idx:, :]
#
#pitchers_bottom = bottom_10_df.sample(n = 4, random_state = 1)['pitcher_id'].values.tolist()
#pitchers_top = top_10_df.sample(n = 4, random_state = 1)['pitcher_id'].values.tolist()
#
#def name_later(list_name):
#
#    df2 = pd.DataFrame()
#
#    for pitcher in list_name:
#        file_path = 'individual_df/' + str(pitcher) + '.csv'
#        df = pd.read_csv(file_path)
#        
#        train_test_split = {2014:'prep', 2015:'train', 2016:'train', 2017:'test'}
#        df['train_test'] = df['year'].map(train_test_split)
#        temp = df.loc[df['train_test'] != 'prep', :]
#
#        temp = temp.groupby(by = ['train_test', 'pitch_type'])['home_team'].count().reset_index()
#        temp.rename(columns = {'home_team':'count'}, inplace = True)
#
#        temp2 = temp.groupby(by = 'train_test')['count'].sum().reset_index()
#        temp2.rename(columns = {'count':'pitches_thrown'}, inplace = True)
#
#        temp3 = temp.merge(temp2, how = 'inner', on = 'train_test')
#
#        temp3['percent'] = round((temp3['count']/temp3['pitches_thrown'])*100,2)
#
#        temp3['pitcher_id'] = pitcher
#
#        if len(df2) == 0:
#            df2 = temp3
#        else:
#            df2 = pd.concat([df2, temp3])
#
#    return df2
#
#
#bottom_df = name_later(pitchers_bottom)
#top_df = name_later(pitchers_top)
#
#print(bottom_df)
#print(top_df)
#
#bottom_df.to_csv('visualisations/pitch_frequencies/bottom_vol.csv', index = False)
#top_df.to_csv('visualisations/pitch_frequencies/top_vol.csv', index = False)

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
