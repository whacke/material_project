import os
import json
import pandas as pd
from multiprocessing import Pool
from pymatgen.io.cif import CifParser
import pymatgen.analysis.dimensionality as pad

def asyncCIF(file):
  try:
    with open('input/CIFs/{}'.format(file)) as f:
      parser = CifParser(f)
      structure = parser.get_structures()[0]

      connected_atoms=pad.find_connected_atoms(structure)
      max1,min1,_=tuple(pad.find_clusters(structure,connected_atoms))

      big_structure=structure.copy()
      big_structure.make_supercell(2)
      big_num_sites=big_structure.num_sites

      big_connected_atoms=pad.find_connected_atoms(big_structure)
      max2,min2,_=tuple(pad.find_clusters(big_structure,big_connected_atoms))

      ratio=max2/max1

  except Exception as e: 
      #print(e)
      ratio = 0

  return [max1,min1,max2,min2,big_num_sites,ratio]

print("Starting CIFs...")
cifs = os.listdir('input/CIFs/')

if __name__ == '__main__':
  with Pool() as p:
    data = p.map(asyncCIF, cifs)

cif_df = pd.DataFrame(data)

cif_df.columns = ['max1','min1','max2','min2','big_num_sites','ratio']

cif_df.to_csv('output/CIF_frame.csv')