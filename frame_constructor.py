import os
import json
import pandas as pd
import numpy as np
#from tqdm import tqdm
from multiprocessing import Pool

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

cifs = os.listdir('temp/CIFs/')
jsons = os.listdir('temp/JSONs/')

def construct_frames(file):
  checklist = os.listdir('output/materials')
  checklist [:] = (elem[:-4] for elem in checklist)
  if(file[:-4] not in checklist):
    with open('temp/JSONs/{}'.format(file)) as json_f:
      temp_json = pd.read_csv(json_f)
      temp_json.set_index('name',inplace=True)
    with open('temp/CIFs/{}'.format(file)) as cif_f:
      temp_cif = pd.read_csv(cif_f)
    
    temp_cif = temp_cif.set_index(temp_json.index)

    df_total = temp_json.join(temp_cif)

    df_total['dimension'] = ""
    df_total = df_total.fillna(0)

    for index, mat in df_total.iterrows():
      df_total.at[index, 'dimension'] = classify_material(mat)

    df_total.to_csv('output/materials/{}'.format(file))

if __name__ == '__main__':
  with Pool() as p:
    p.map(construct_frames, cifs)