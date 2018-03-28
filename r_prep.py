import pandas as pd
import numpy as np

df = pd.read_csv('filtered_pitchers.csv')

# Output csv with mean pitch type confidence for each pitcher
pitch_conf_df = df.groupby('pitcher_id')['type_confidence'].mean().reset_index()
pitch_conf_df.to_csv('type_confidence.csv', index = False)

# Randomly selected 4 pitchers in the bottom/top 10% of mean pitch type confidence
pitch_conf_df.sort_values(by = ['type_confidence'], inplace = True)

bot_10_percent = pitch_conf_df.iloc[0:18, :] # ~ 180 pitchers in data. Hence first 18 rows are in bottome 10 percent
bot_sample = bot_10_percent.sample(4)
print(bot_sample)
top_10_percent = pitch_conf_df.iloc[-18:, :]
top_sample = top_10_percent.sample(4)
print(top_sample)

# With the sample pitchers, find the mean confidence for each of there pitch types
pitchers = bot_sample['pitcher_id'].tolist() + top_sample['pitcher_id'].tolist()

temp = df.loc[df['pitcher_id'].isin(pitchers), ['pitcher_id', 'pitch_type', 'type_confidence', 'pfx_x', 'pfx_z', 'start_speed']]
conf_by_pitch = temp.groupby(['pitcher_id', 'pitch_type'])['type_confidence'].mean().reset_index()

# Create new df which only includes pitch types which are thrown with more than 5% frequency (individually for each pitcher)
pitch_counts = temp.groupby(['pitcher_id', 'pitch_type'])['type_confidence'].count().reset_index()
pitch_counts.columns = ['pitcher_id', 'pitch_type', 'count']

final = pd.DataFrame()
for pitcher in pitchers:
    counts = pitch_counts.loc[pitch_counts['pitcher_id'] == pitcher, :]
    pitchers_thrown = float(counts['count'].sum())

    keep_pitch_types = []
    i = 0
    while i < len(counts):
        pitch_type = counts.iloc[i, 1]
        pitch_count = float(counts.iloc[i, 2])
        pitch_percent = pitch_count/pitchers_thrown

        if pitch_percent > 0.05:
            keep_pitch_types.append(pitch_type)

        i += 1

    temp2 = temp.loc[(temp['pitcher_id'] == pitcher) & (temp['pitch_type'].isin(keep_pitch_types)), :]

    if len(final) == 0:
        final = temp2
    else:
        final = pd.concat([final, temp2])

# Add column to final df which says if pitch from top or bottom and save final csv
bot_pitchers = bot_sample['pitcher_id'].drop_duplicates().tolist()
final['class'] = ['bottom' if x in bot_pitchers else 'top' for x in final['pitcher_id']]

final.to_csv('per_pitch_confidence.csv', index = False)



