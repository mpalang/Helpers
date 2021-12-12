#import os,glob
#from pathlib import Path
import numpy as np
from pathlib import Path
#import matplotlib.pyplot as plt
import logging
import sys

class srsFile:
    def __init__(self,settings):
        self.Settings=settings


    def getSRSData(self.Settings['filename'],M_No=300, No_Avg=200, MakeDiffSpecs=False,t_all=[],output_suffix='_converted'): #return Wn, time,spectra, info, Spec_Pts, s_count, bg

        Spec_Pts = np.fromfile(f, dtype=np.int32 , count=1, offset=14036)[0]
        Max_Wn = np.fromfile(f, dtype=np.single , count=1, offset=14048)[0]
        Min_Wn = np.fromfile(f, dtype=np.single , count=1, offset=14052)[0]
        Wn=np.linspace(Min_Wn, Max_Wn, num=Spec_Pts)
                    
        info_raw=np.fromfile(f, dtype='S1',count=318, offset=15232)
        info=''
        for b in info_raw:
            info=info+b.decode('ascii')
        del b       
                
        spectra=[]
        time=[]
        
        #M_No=200
        Header_Size=25
        Footer_Size=25
        Start_of_Data=49232 #4226*4 #16904
        
        bg=np.fromfile(f, dtype=np.single , count=Spec_Pts, offset= 16904 + 4*(Header_Size))
                
        i=0
        
        s=np.fromfile(f, dtype=np.single , count=Spec_Pts, offset= Start_of_Data+4*(Header_Size))
        scr=np.fromfile(f, dtype=np.uint, count=2, offset= Start_of_Data)
        s_count=1
        
        while scr.shape[0]>1 and scr[0]==No_Avg and i<M_No:
            try:
                spectra.append(s)
                time.append(scr[1]/6000)
                i=i+1
                s_count=i
                s=np.fromfile(f, dtype=np.single , count=Spec_Pts, offset= Start_of_Data+4*Header_Size+4*i*(Spec_Pts+Header_Size))
                scr=np.fromfile(f, dtype=np.uint, count=2, offset= Start_of_Data + 4*i*(Header_Size+Spec_Pts))
            except:
                spectra.append('Error')
                time.append('Error')
                
        #spectra=spectra/100
        print('import data from: ' + f)
        
        Data={'Wn': Wn, 'time': time, 'spectra': spectra, 'info': info, 'Spec_Pts': Spec_Pts, 's_count': s_count, 'Bg': bg}
        return Data


if __name__=='__main__':
    X=srsFile('SRStoCSV/Test.srs')
    X.getSrsData()
