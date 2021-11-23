#This little program taks .srs files from ThermoFisher's Omnic and converts it into an easily readable .csv file.

 # -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 11:08:40 2021

@author: Moritz Lang
"""
import os, glob
#import warnings
#warnings.filterwarnings("ignore")

   
# srs File: 
    
# Can be String or List of Strings. Leave empty if all .srs files shall be converted from folder.

filename = ''

output_filename='_Converted' # will be attached to the input filename

# Maximum number of collected spectra. (in case stopping condition doesnt work). Average Number for one measurement.

M_No = 300
No_Avg = 200

# add as many times for Diffspectra as wanted. 
Makediffspecs=False
t_all=[19,104,149]

parent_directory=Path(__file__).parent    
if filename == '':
    filelist=glob.glob(str(Path(parent_directory,'*.srs'))) 
else: 
    filelist=[filename]

#%%Define Functions:

def getSRSData(Settings): #return Wn, time,spectra, info, Spec_Pts, s_count, bg

        filelist=Settings[]
        output_suffix=Settings[5]
        M_No=Settings[0]
        t_all=Settings[1]
        No_Avg=Settings[6]
        
        f=inputdir+'/'+fn

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
            
def srsTreatData(Data,t_all): #in: header, data, Wn, spectra_counter, Spec_Pts, t
       
        Wn=Data['Wn']
        time=Data['time']
        time=[x.round(2) for x in time] # Runde Zeit in Minuten auf 2 Nachkommastellen.
        spectra=Data['spectra']
        
        spectra_counter=Data['s_count']
        Spec_Pts=Data['Spec_Pts']
        t_all=t_all
        bg=Data['Bg']
                
        t=[0]
        for j in t_all:
            for i in range(spectra_counter):
                if time[i]-1<j<time[i]+1:
                    t.append(i)
                    break

        

        
        spectra=[x/100 for x in spectra] #data is saved as 'R' (0-100). (0-1) is needed.]
        #spectra_rec=[1/x for x in spectra]
        spectra_log=[np.log10(1/x) for x in spectra] #log(1/R)

        diffspecs_log=[]        
        n=0
        for td in t:
            diffspecs_log.append([x-spectra_log[td] for x in spectra_log])
        
        Spectra={'Wn': Wn, 'time': time, 'spectra': spectra, 'spectra_log': spectra_log, 'diffspecs_log': diffspecs_log, 'Bg': bg}
        
        return  Spectra

def srsSaveData(fn, Settings, Spectra):
        import numpy as np
        import os, os.path
        from os import path
        
        outputdir=Settings[4] + Settings[5]
        if not path.exists(outputdir):
            os.makedirs(outputdir)
            
        Wn=Spectra['Wn']
        time=[x.round(2) for x in Spectra['time']]
        time.insert(0,0)
        time=np.array(time)
        spectra=Spectra['spectra']
        spectra_log=Spectra['spectra_log']
        diffspecs_log=Spectra['diffspecs_log']
        
        spectra_m=np.array(Wn)
        for i in spectra:
            spectra_m=np.column_stack((spectra_m,i))
        spectra_m=np.vstack((time,spectra_m))    
        
        spectra_log_m=np.array(Wn)
        for i in spectra_log:
            spectra_log_m=np.column_stack((spectra_log_m,i))
        spectra_log_m=np.vstack((time,spectra_log_m))
        
        s = open(outputdir + '/' + fn.removesuffix('.srs')+ '_Spectra.txt', 'w')
        np.savetxt(s,spectra_m)
        s.close()

        s = open(outputdir + '/' + fn.removesuffix('.srs')+'_Spectra_log.txt', 'w')
        np.savetxt(s, spectra_log_m)
        s.close()
        
        n=1
        for ds in diffspecs_log:
            ds_m=np.array(Wn)
            for i in ds:
                ds_m=np.column_stack((ds_m,i))
            ds_m=np.vstack((time,ds_m))  
            
            s = open(outputdir + '/' + fn.removesuffix('.srs')+'_Diffspec_'+ str(n) +'_log.txt', 'w')
            np.savetxt(s, ds_m)
            s.close()
            n=n+1
       

