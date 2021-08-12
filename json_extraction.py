import os
import json
import pandas as pd
from multiprocessing import Pool

#this function provided by Shaurya Khurana
def process_dict(data, properties = {}):
    for k in data.keys():
        if isinstance(data.get(k),float) or isinstance(data.get(k),int) or isinstance(data.get(k),bool):
            properties[k]= data.get(k)
        
        if isinstance(data.get(k), dict):
            temp = data.get(k)
            properties = process_dict(temp,properties)
            
        if isinstance(data.get(k), list):
            if len(data.get(k)) and isinstance(data.get(k)[0], dict):
                properties = process_dict(data.get(k)[0],properties)
                
    return properties

def asyncJSON(file):
  try:
    with open('input/JSONs/{}'.format(file)) as f:
        data = json.loads(f.read())
    properties = process_dict(data, {})
    properties['name'] = file.split('.')[0]
    return properties
  except:
    print("Error parsing at {}".format(file))


print("Starting JSONs...")
jsons = os.listdir('input/JSONs/')

if __name__ == '__main__':
  with Pool() as p:
    materials = p.map(asyncJSON, jsons)

json_df = pd.DataFrame(materials)
json_df.set_index('name',inplace=True)
json_df.to_csv('output/JSON_frame.csv')