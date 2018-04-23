# Input this into feature_eng.py script if kept

import pandas as pd
import numpy as np

df = pd.read_csv('../../individual_df/112526.csv')

temp = df.groupby('batter_id')['home_team'].count().reset_index()
temp.rename(columns = {'home_team': 'count'}, inplace = True)
temp.to_csv('pitcher_vs_batter.csv', index = False)

temp2= df.groupby(['batter_id', 'ab_game_num'])['home_team'].count().reset_index()
temp2 = temp2.groupby(['batter_id'])['ab_game_num'].count().reset_index()
temp2.rename(columns = {'ab_game_num':'count'}, inplace = True)
temp2.to_csv('ab_vs_batter.csv', index = False)
