import numpy as np
import pandas as pd
import MySQLdb as myDB
import pandas.io.sql as psql

#this code assumes that the scrapping portion has been completed.  The code for the scrapping can be found at: https://github.com/abdouglass/My_NETA/blob/master/CreateMasterDictionary.py

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

#initial data cleaning 
#create a copy for cleaning, so the original data is still available unchanged
themasterDF = masterDF.copy()


#creating an Education Rank column as education is ordinal instead of categorical
themasterDF["EduRank"] = 0
edurank = {
            "others" : 0,
            "not given": 0,
            "illiterate": 1,
            "literate": 2,
            "5th pass": 3,
            "8th pass": 4,
            "10th pass": 5,
            "12th pass": 6,
            "graduate": 7,
            "graduate professional": 8,
            "post graduate": 9,
            "doctorate": 10
            }

for a_val, b_val in edurank.iteritems():
    themasterDF["EduRank"][themasterDF.education==a_val] = b_val

#renaming columns
themasterDF.rename(columns={'candidate name':'cand_name', 'criminal cases':'criminal_cases'}, inplace=True)

#creating a winner column & binary win column
themasterDF["WinnerTF"] = themasterDF.cand_name.str.contains('winner')
themasterDF["Winner"] = np.where(themasterDF["WinnerTF"]==True,1,0)

#creating a clean assets column
themasterDF["Asset"] = themasterDF["assets"].map(lambda x:x.lstrip('rsÂ ').split(" ~")[0].replace(",", ""))

#creating a clean liabilities column
themasterDF["Liability"] = themasterDF["liabilities"].map(lambda x:x.lstrip('rsÂ ').split(" ~")[0].replace(",", ""))


if themasterDF.cand_name.str.contains('winner'):
    themasterDF["Winner"] = 1
else:
    themasterDF["Winner"] = 0
        
    
#saving to mySQL (adjust username, password, etc. to prefered)
dbConnect = myDB.connect(host='localhost',
                            user='root',
                            passwd='root',
                            db='classwork') # this assumed the database has already been established

themasterDF.to_sql(con=dbConnect,
                name='mynetasql',
                if_exists='replace',
                flavor='mysql')

#Read data from mySQL back into Pandas data frame
masterDF_mysql = psql.frame_query('select * from mynetasql;', con=dbConnect)

#saving to csv (adjust location to preference for saving)
masterDF_mysql.to_csv("masterdictdump.csv")

