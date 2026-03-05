import pandas as pd

df = pd.read_csv('CC GENERAL.csv')

print('TENURE Statistics:')
print(f'Min: {df["TENURE"].min()}')
print(f'Max: {df["TENURE"].max()}')
print(f'Mean: {df["TENURE"].mean():.1f}')
print(f'Std: {df["TENURE"].std():.1f}')
print(f'Unique values: {sorted(df["TENURE"].unique())}')
