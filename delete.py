import pandas as pd
import numpy as np

df = pd.read_csv('mlb_gd_2014.csv')
df2 = pd.read_csv('mlb_gd_2015.csv')
df3 = pd.read_csv('mlb_gd_2016.csv')
df4 = pd.read_csv('mlb_gd_2017.csv')

temp = pd.concat([df, df2, df3, df4], axis = 0)

print(temp.shape)

temp.to_csv('mlb_gb_full.csv', index = False)
