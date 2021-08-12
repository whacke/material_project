import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm

json_df = pd.read_csv('output/JSON_frame.csv')
cif_df = pd.read_csv('output/CIF_frame.csv')

cif_df = cif_df.set_index(json_df.index)

df_total = json_df.join(cif_df)

df_total['dimension'] = ""
df_total = df_total.fillna(0)

def classify_material(row):
  if (row['e_above_hull'] < 0.1) & (row['min1']!=1) & (row['min2']!=row['min1']) & (row['max2']==row['big_num_sites']):
    result= 3
  elif (row['e_above_hull'] < 0.1) & (row['min1']!=1) & (row['min2']!=row['min1']) & (row['max2']!=row['big_num_sites']) & (row['ratio']==4):
    result= 2
  elif (row['e_above_hull'] < 0.1) & (row['min1']!=1) & (row['min2']!=row['min1']) & (row['max2']!=row['big_num_sites']) & (row['ratio']==2):
    result= 1
  else:
    result= 0  
  return result

print("Classifying Materials...")
for index, mat in tqdm(df_total.iterrows()):
  df_total.at[index, 'dimension'] = classify_material(mat)

print("Exporting to CSV...")
df_total.to_csv('output/TOTAL_frame.csv')