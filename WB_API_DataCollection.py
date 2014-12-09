#this code allows us to pull statistics about education and GNI for India from the World Bank API, for a comparison against the candidate information

import wbdata
import pandas as pd
import datetime

#the country we want to pull data for
countries = ["IN"]
 
#the indicators that we are interested in collecting data on
indicators = {'NY.GNP.PCAP.CD':'GNI per Capita',
              'MYS.PROP.15UP.NED.MF' : 'Pop % - No Education (Age: 15+)',
              'MYS.PROP.15UP.PRI.MF' : 'Pop % - Primary (Age: 15+)',
              'MYS.PROP.15UP.SEC.MF' : 'Pop % - Secondary (Age: 15+)',
              'MYS.PROP.15UP.TER.MF' : 'Pop % - Tertiary (Age: 15+)'}
 
#start and end date for data request
years = (datetime.datetime(2010, 1, 1), datetime.datetime(2010, 12, 12))  #chose 2010, because it had data available for the indicators, and was in the middle of the election data we had available
 
#grab indicators for selected country and timeframe and load into data frame
df = wbdata.get_dataframe(indicators, country=countries, data_date=years)

#df is "pivoted", pandas' unstack function reshapes it into something plottable
wb_df = df.unstack(level=0)

#save data into a CSV for access in R
wb_df.to_csv("G:\ProgrammingForAnalytics\Assignments\GroupProject\WB_data.csv")
