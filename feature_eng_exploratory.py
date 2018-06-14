import pandas as pd
import numpy as np
import sys
import argparse

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

#### Line chart wrangling
df = pd.read_csv('players.csv')

df = pd.read_csv('individual_df/fe/453265_fe.csv')

temp = df.loc[df['year'] != 2014, ['a_global_prior_SI_percent', 'a_global_prior_SL_percent', 'a_global_prior_CH_percent', \
                                   'b_global_prior_SI_weighted_percent', 'b_global_prior_SL_weighted_percent', \
                                   'b_global_prior_CH_weighted_percent']]
len_temp = np.arange(len(temp))
temp['pitch_count'] = len_temp
temp = pd.melt(temp, id_vars = ['pitch_count'])
mapper = {'a_global_prior_SI_percent': 'Historic SI Percent', 'a_global_prior_SL_percent': 'Historic SL Percent', \
          'a_global_prior_CH_percent': 'Historic CH Percent', 'b_global_prior_SI_weighted_percent': 'Weighted SI Percent', \
          'b_global_prior_SL_weighted_percent': 'Weighted SL Percent', 'b_global_prior_CH_weighted_percent': 'Weighted CH Percent'}
temp['variable'] = temp['variable'].map(mapper)

temp.to_csv('visualisations/pitch_frequencies/pitch_frequencies_weighted.csv', index = False)


aa

temp.drop_duplicates(subset = ['game_id'], keep = 'last', inplace = True)
temp2 = pd.melt(temp, id_vars = ['game_id'])
temp2.to_csv('visualisations/pitch_frequencies/pitch_frequencies_change.csv', index = False)

temp3 = df.loc[df['year'] != 2014, ['c_w_40_SI_percent', 'd_w_120_SI_percent', 'e_w_360_SI_percent']]
len_temp = np.arange(len(temp3))
temp3['pitch_count'] = len_temp
temp4 = pd.melt(temp3, id_vars = ['pitch_count'])
temp4.to_csv('visualisations/pitch_frequencies/pitch_frequencies_windows.csv', index = False)
print(temp4.head())
print(temp4.tail())
a

parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs = '+', help = 'input data path')
args = parser.parse_args()

count = []

for pitcher in args.input:
    print(pitcher)
    sys.stdout.flush()
    df = pd.read_csv(pitcher)

    # Find number of pitchers thrown to each batter
    temp = df.groupby('batter_id')['home_team'].count()
    count = count + temp.values.tolist()

p_to_b = pd.DataFrame(data = count, columns = ['count'])
p_to_b.to_csv('visualisations/exploratory_analysis/count_pitches_to_batter.csv', index = False)
print(p_to_b)
