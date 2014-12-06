import numpy as np
import pandas as pd

#create dataframe from the nested dictionary
masterDF = pd.DataFrame()   #create blank DF
for state in masterdict: 
   for year in masterdict[state]:
      for district in masterdict[state][year]:
         for ac in masterdict[state][year][district]:
             if type(masterdict[state][year][district][ac]) is dict:    #find lowest dictionary
                candidateDF = pd.DataFrame(masterdict[state][year][district][ac])   #create temporary DF with lowest level dictionary
                candidateDF['ac'] = str(ac)   #add AC, district, year, and state to each row within the DF
                candidateDF['District'] = str(district)
                candidateDF['Year'] = str(year)
                candidateDF['State'] = str(state)
                masterDF = masterDF.append(candidateDF)   #append temporary DF to final DF
