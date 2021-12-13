from srsLib import srsFile

#Make your settings from here: -->
# srs File:    
# Can be String or List of Strings. Leave empty if all .srs files shall be converted from folder.
filename= 'Test.srs' #output_filename='_Converted' # will be attached to the input filename and has to be added to the getSRSData Function.

#TODO: Make settings adjustable...for now just default values in srsLib work!
#Average Number for one spectrum (from experiment settings).
No_Avg= 200
# add as many times for Differencespectra as you want. 
MakeDiffSpecs= False
t_all= [19,104,149]
# Maximum number of collected spectra (should not be necessary...just in case stopping condition doesnt work). 
M_No= 300
#<-- up to here.

X=srsFile(filename)
X.getData()
Data=X.Data

#print(f'{X.Spec_Pts}\n{X.info}')