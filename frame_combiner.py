import os
import pandas as pd
from multiprocessing import Pool

def frames_combiner(file):
	with open('output/materials/{}'.format(file)) as f:
		return pd.read_csv(f)


materials = os.listdir('output/materials/')

final_df = pd.DataFrame()

if __name__ == '__main__':
  with Pool() as p:
    final_df = final_df.append(p.map(frames_combiner, materials))

final_df.set_index('name', inplace=True)

final_df.to_csv('output/TOTAL_frame.csv')