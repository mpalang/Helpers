#import os
#import glob
from pathlib import Path
import numpy as np
import logging
import sys
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #logging.FileHandler("Logging.log"),
        logging.StreamHandler(sys.stdout)
    ])

# def getFileList(Settings):
#     Settings['parent_directory']=Path(__file__).parent    
#     if Settings['filename'] == '':
#         Settings['filelist']=glob.glob(str(Path(Settings['parent_directory'],'*.srs'))) 
#     else: 
#         Settings['filelist']=Settings['filename']
#     return Settings

class srsFile:
    def __init__(self,filename):
        self.Filename=Path(filename)
        self.Data={}
        self.Spec_Pts = np.fromfile(self.Filename, dtype=np.int32 , count=1, offset=14036)[0]
        self.Max_Wn = np.fromfile(self.Filename, dtype=np.single , count=1, offset=14048)[0]
        self.Min_Wn = np.fromfile(self.Filename, dtype=np.single , count=1, offset=14052)[0]
        info_raw=np.fromfile(self.Filename, dtype='S1',count=318, offset=15232)
        self.info=''
        for b in info_raw:
            self.info=self.info+b.decode('ascii')
        del b 
   

    def getData(self,No_Avg=200,Header_Size=25,Footer_Size=25,Start_of_Data=49232,Percent=False,M_No=500):
#        Start_of_Data=49232 #4226*4 #original Value from Matlab script: 16904
#        Default Values must be adjusted to current experiment!
        
        f=Path(self.Filename)
        logging.info(f'Get Data from {f}.')       
        
        Wn=np.linspace(self.Min_Wn, self.Max_Wn, num=self.Spec_Pts)
        spectra=[]
        time=[]

        bg=np.fromfile(f, dtype=np.single , count=self.Spec_Pts, offset= 16904 + 4*(Header_Size))
                
        i=0
        
        s=np.fromfile(f, dtype=np.single , count=self.Spec_Pts, offset= Start_of_Data+4*(Header_Size))
        scr=np.fromfile(f, dtype=np.uint, count=2, offset= Start_of_Data)
        s_count=1
        
        while scr.shape[0]>1 and scr[0]==No_Avg and i<M_No:
            try:
                spectra.append(s)
                time.append(scr[1]/6000)
                i=i+1
                s_count=i
                s=np.fromfile(f, dtype=np.single , count=self.Spec_Pts, offset= Start_of_Data+4*Header_Size+4*i*(self.Spec_Pts+Header_Size))
                scr=np.fromfile(f, dtype=np.uint, count=2, offset= Start_of_Data + 4*i*(Header_Size+self.Spec_Pts))
            except:
                spectra.append('Error')
                time.append('Error')
                
        #spectra=spectra/100
        
        self.Data={'Wn': Wn, 'time': time, 'spectra': spectra, 'number of spectra': s_count, 'Bg': bg}
        
        return self

