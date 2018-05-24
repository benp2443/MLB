import pandas as pd
import numpy as np
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs = '+', help = 'input data path')
args = parser.parse_args()

df = pd.DataFrame()
for pitcher in args.input:
    temp = pd.read_csv(pitcher)
    temp = temp.loc[:, ['pitcher_id', 'pitch_type', 'group_pitch_type', 'type_confidence', 'year', 'home_team']]
    df = pd.concat([df, temp], axis = 0)

df = df.loc[df['year'] != 2014, :]
df['type_confidence'] = df['type_confidence']/2

df[['type_confidence']].to_csv('visualisations/type_confidence/pitch_type_confidence.csv', index = False)

mean_conf = df.groupby(['pitcher_id'])['type_confidence'].mean().reset_index()
print(mean_conf[['type_confidence']].mean())
print(mean_conf[['type_confidence']].std())
mean_conf.to_csv('visualisations/type_confidence/pitchers_mean_conf.csv', index = False)

threseholds = [0.00, 0.20, 0.40, 0.60, 0.80]

#output_df = pd.DataFrame()
#for confidence in threseholds:
#    temp = df.loc[df['type_confidence'] >= confidence, :]
#    temp = temp.groupby(['pitcher_id'])['home_team'].count().reset_index()
#    temp.rename(columns = {'home_team':'count'}, inplace = True)
#    temp['thresehold'] = confidence
#
#    temp2 = temp[['count', 'thresehold']]
#
#    if len(output_df) == 0:
#        output_df = temp2
#    else:
#        output_df = pd.concat([output_df, temp2], axis = 0)
#
#output_df.to_csv('visualisations/type_confidence/pitches_by_count.csv', index = False)


#pitchers_df = pd.DataFrame([[0.00, 0],[0.20, 0], [0.40, 0], [0.60, 0], [0.80, 0]], columns = ['confidence', 'pitchers_count'])
#
#def pitcher_counter(df, thresehold):
#
#    temp = df.loc[df['type_confidence'] >= thresehold]
#    pitchers_list = temp['pitcher_id'].unique()
#
#    # Create dataframe which has the pitcher id, year, and number of pitchers thrown in each row
#    pitcher_count = temp.groupby(['pitcher_id', 'year'])['home_team'].count().reset_index()
#    pitcher_count.columns = ['pitcher_id', 'year', 'pitch_count']
#    
#    # Create column which is True if pitcher threw over 500 pitches for that year and False otherwise
#    def over_500(pitch_count_column):
#        if pitch_count_column >= 500:
#            return True
#        else:
#            return False
#    
#    pitcher_count['over_500'] = pitcher_count['pitch_count'].apply(over_500)
#    
#    # Filter pitchers based on years played and pitchers thrown per season
#    final_pitchers = []
#    
#    for pitcher in pitchers_list:
#        temp2 = pitcher_count.loc[pitcher_count['pitcher_id'] == pitcher, :]
#    
#        # exclude pitcher if he has not pitched in all four seasons
#        if len(temp2) != 3:
#            continue 
#    
#        # exclude pitchers which have not thrown more than 500 pitches in each season
#        years_over_500_column = temp2['over_500'].sum()
#        if years_over_500_column != 3:
#            continue
#    
#        final_pitchers.append(pitcher)
#
#    return len(final_pitchers)
#
#for confidence in threseholds:
#    count_pitchers = pitcher_counter(df, confidence)
#    print(count_pitchers)
#    pitchers_df.loc[pitchers_df['confidence'] == confidence, 'pitchers_count'] = count_pitchers
#    print(pitchers_df.loc[pitchers_df['confidence'] == confidence, 'pitchers_count'])
#
#pitchers_df.to_csv('visualisations/type_confidence/pitchers_count.csv', index = False)
