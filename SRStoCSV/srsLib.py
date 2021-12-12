#import os,glob
#from pathlib import Path
import numpy as np
from pathlib import Path
#import matplotlib.pyplot as plt
import logging
import sys
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #logging.FileHandler("Logging.log"),
        logging.StreamHandler(sys.stdout)
    ])

class srsFile:
    def __init__(self,filename):
        self.Filename=Path(filename)
        self.Data={}
        self.Spec_Pts = np.fromfile(self.Filename, dtype=np.int32 , count=1, offset=14036)[0]
        Max_Wn = np.fromfile(self.Filename, dtype=np.single , count=1, offset=14048)[0]
        Min_Wn = np.fromfile(self.Filename, dtype=np.single , count=1, offset=14052)[0]
        self.Wn=np.linspace(Min_Wn, Max_Wn, num=self.Spec_Pts)
        info_raw=np.fromfile(self.Filename, dtype='S1',count=318, offset=15232)
        self.info=''
        for b in info_raw:
            self.info=self.info+b.decode('ascii')
        del b 
   

    def getData(self):
        f=Path(self.Filename)
        logging.info(f'Get Data from {f}.')

