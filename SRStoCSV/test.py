from srsLib import srsFile

Settings={  
#Make your settings from here: -->
# srs File:    
# Can be String or List of Strings. Leave empty if all .srs files shall be converted from folder.
    'filename': '', #output_filename='_Converted' # will be attached to the input filename and has to be added to the getSRSData Function.
# Maximum number of collected spectra (should not be necessary...just in case stopping condition doesnt work). 
    'M_No': 300,
#Average Number for one spectrum (from experiment settings).
    'No_Avg': 200,
# add as many times for Differencespectra as you want. 
    'MakeDiffSpecs': False,
    't_all': [19,104,149]
#<-- up to here.
}

X=srsFile(Settings)

print(X.Settings)