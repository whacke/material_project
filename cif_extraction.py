import os
import json
import pandas as pd
from multiprocessing import Pool
from pymatgen.io.cif import CifParser
import pymatgen.analysis.dimensionality as pad

def asyncCIF(file):
  checklist = os.listdir('temp/CIFs')
  checklist [:] = (elem[:-4] for elem in checklist)
  if(file[:-4] not in checklist):
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
    file = file[:-4]
    name = file
    diction = {'max1':max1,'max2':max2,'min1':min1,'min2':min2, 'big_num_sites':big_num_sites,'ratio':ratio,'name':name}
    df = pd.DataFrame([diction])
    df.set_index('name',inplace=True)
    df.to_csv('temp/CIFs/{}.csv'.format(file))

print("Starting CIFs...")
cifs = os.listdir('input/CIFs/')

if __name__ == '__main__':
  with Pool() as p:
    p.map(asyncCIF, cifs)