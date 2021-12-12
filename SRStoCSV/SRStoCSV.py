

 # -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 11:08:40 2021

@author: Moritz Lang
"""
#This little program takes .srs files from Thermo Fisher's Omnic and converts it into an easily readable .csv file.



import os
import glob
import numpy as np
from pathlib import Path
import logging
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.WARNING)
#import warnings
#warnings.filterwarnings("ignore")

Settings={  

#Make your settings from here: -->
# srs File:    
# Can be String or List of Strings. Leave empty if all .srs files shall be converted from folder.

'filename': '', #output_filename='_Converted' # will be attached to the input filename and has to be added to the getSRSData Function.

# Maximum number of collected spectra. (in case stopping condition doesnt work). Average Number for one measurement.
'M_No': 300,
'No_Avg': 200,

# add as many times for Diffspectra as you want. 
'MakeDiffSpecs': False,
't_all': [19,104,149]

#<-- up to here.
}



#%% Define Functions:
####

def getFileList(Settings):
    Settings['parent_directory']=Path(__file__).parent    
    if Settings['filename'] == '':
        Settings['filelist']=glob.glob(str(Path(Settings['parent_directory'],'*.srs'))) 
    else: 
        Settings['filelist']=Settings['filename']
    return Settings

def getSRSData(f,M_No=300, No_Avg=200, MakeDiffSpecs=False,t_all=[],output_suffix='_converted'): #return Wn, time,spectra, info, Spec_Pts, s_count, bg

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
            
def srsTreatData(Data,Settings): #in: header, data, Wn, spectra_counter, Spec_Pts, t
       
    Wn=Data['Wn']
    time=Data['time']
    time=[x.round(2) for x in time] # Runde Zeit in Minuten auf 2 Nachkommastellen.
    spectra=Data['spectra']
    
    spectra_counter=Data['s_count']
    Spec_Pts=Data['Spec_Pts']
    bg=Data['Bg']
            
    spectra=[x/100 for x in spectra] #data is saved as 'R' (0-100). (0-1) is needed.]
    #spectra_rec=[1/x for x in spectra]
    spectra_log=[np.log10(1/x) for x in spectra] #log(1/R)
    
    Spectra={'Wn': Wn, 'time': time, 'spectra': spectra, 'spectra_log': spectra_log, 'Bg': bg}
    
    if Settings['MakeDiffSpecs']:
        Spectra['diffspecs_log']=[]   
        t=[0]
        for j in Data['t_all']:
            for i in range(spectra_counter):
                if time[i]-1<j<time[i]+1:
                    t.append(i)
                    break

        for td in t:
            Spectra['diffspecs_log'].append([x-spectra_log[td] for x in spectra_log])
    
    return  Spectra

def srsSaveData(f,Spectra, Settings):

    
    sn=Path(Path(f).parent,'CSV_Data',Path(f).name.replace('.srs',''))

    print('savename: '+str(sn))  
    Wn=Spectra['Wn']
    time=[x.round(2) for x in Spectra['time']]
    time.insert(0,0)
    time=np.array(time)
    spectra=Spectra['spectra']
    spectra_log=Spectra['spectra_log']
    if Settings['MakeDiffSpecs']:
        diffspecs_log=Spectra['diffspecs_log']
    
    spectra_m=np.array(Wn)
    for i in spectra:
        spectra_m=np.column_stack((spectra_m,i))
    spectra_m=np.vstack((time,spectra_m))    
    
    spectra_log_m=np.array(Wn)
    for i in spectra_log:
        spectra_log_m=np.column_stack((spectra_log_m,i))
    spectra_log_m=np.vstack((time,spectra_log_m))
    
    s = open(sn+'_Spectra.csv', 'w')
    np.savetxt(s,spectra_m, delimiter=',')
    s.close()

    s = open(sn+'_Spectra_log.txt', 'w')
    np.savetxt(s, spectra_log_m, delimiter=',')
    s.close()
    
    if Settings['MakeDiffSpecs']:
        n=1
        for ds in diffspecs_log:
            ds_m=np.array(Wn)
            for i in ds:
                ds_m=np.column_stack((ds_m,i))
            ds_m=np.vstack((time,ds_m))  
            
            s = open(sn+'_Diffspec_'+ str(n) +'_log.txt', 'w')
            np.savetxt(s, ds_m, delimiter=',')
            s.close()
            n=n+1
    

#%% Run Code

Settings=getFileList(Settings)
Data={}
Spectra={}
for f in Settings['filelist']:
    Data=getSRSData(f,Settings)
    Spectra=srsTreatData(Data,Settings)
    for key in Spectra.keys():
        print(len(Spectra[key]))
    print(len(Data['spectra']))
    #srsSaveData(f,Spectra, Settings)


