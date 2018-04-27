##### Pitch type nulls #####
print('Null Values', '\n')
for col in columns:
    null_values = df[col].isnull().sum()
    if null_values > 0:
        print(col)
        print(df[col].isnull().sum())

