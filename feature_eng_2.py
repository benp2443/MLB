import pandas as pd
import numpy as np
import argparse

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

parser = argparse.ArgumentParser()
parser.add_argument('--input', help = 'input data path')
args = parser.parse_args()

df = pd.read_csv(args.input)


