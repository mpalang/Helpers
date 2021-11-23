import os,glob
from pathlib import Path
import matplotlib.pyplot as plt


parent_directory=Path(__file__).parent
Liste=glob.glob(str(Path(parent_directory,'*.srs')))
#print(Path(parent_directory+'*srs'))
print(parent_directory)
print(Liste)
