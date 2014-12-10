GWU MSBA
Programming for Analytics (Fall 2014)

Political Selection in the World's Largest Democracy
===============

The code within this repository can be used to scrape candidate data from myneta.info, transform into a data frame, save as a csv, analyse and present in R.Shiny.

CreateMasterDictionary.py includes the code to scrape myneta.info.

DF_from_NestedDict.py converts the nested dictionary from CreateMasterDictionary.py into a data frame, do some initial data cleaning, as well as save the dataframe into mySQL and a csv format.

WB_API_DataCollection.py pulls data on Indian general demographics with regards to education attainment and GDP.

server.R and ui.R includes analysis as well as creation of an interactive way to view candidate characteristic by state comparing the losers and winners.  This includes graphs for age and education, as well as pie charts for criminal cases (grouped by no cases, 1-2 cases, and 3 or more) and whether or not they have party affiliation.

