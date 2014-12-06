
import urllib2
from bs4 import BeautifulSoup as bs
import re


#beautiful soup
def soup_url(url):
    page = urllib2.urlopen(url)
    soup = bs(page)
    return soup
    
    
#create a dictionary of all states from myneta.info and their associated urls
def get_states(url, searchphrase):
    soup = soup_url(url)
    # find href and save as string
    href = soup.findAll('a', href = True)
    href_string = []
    # save hrefs in a list
    for a in href:
        href_string.append(str(a))
    # find a particular search phrase in the hrefs
    searchlist = []
    for a in href_string:
        if searchphrase in a:
            searchlist.append(a)
    return searchlist

#create dictionary of states (the keys) and their associated urls (the values)
def create_state_dict(state_list):
    dict1 = {}
    for item in state_list:
        value = item[item.find('"')+1:item.find('>')-1] #determine value
        value = value.replace(' ', '%20') #replace white spaces with %20, as they would appear in the url
        key = item[item.find('>')+1:item.find('</a')] #determine key 
        dict1[key] = value
    return dict1

#creates dictionary of state assemblies & urls
state_dict = create_state_dict(get_states("http://myneta.info/", "state_assembly"))



# Getting state assembly-election year links and cleaning them
def get_year_links(url, searchphrase):
    soup = soup_url(url)
    # find href and save it as a new list
    href = soup.findAll('a', text = re.compile(searchphrase))
    href_clean = []
    for item in href:
        a = str(item)
        b = a[a.find('"')+1:a.find('>')-1] 
        href_clean.append(b)
    return href_clean

# append district to dictionary such that {state name: {election year : year url}}
def create_yr_dict(StateDict, searchPhrase):
    for x in StateDict: #for each key in the State Dictionary 
        value = get_year_links(StateDict[x], searchPhrase) # set the value as the function that searches for candidate links 
        yrdict = {}
        for a in value:
            key_a = str(re.findall(r'\d+', a)).strip("[]'")
            if len(key_a) == 2:     #for keys that are only last two digits of year, add first two (20XX)
                key_a = "20" + key_a
            # key_a = str(int(s) for s in str(a).split() if s.isdigit())
            yrdict[key_a] = a # change key label to year
        StateDict[x] = yrdict  
    return StateDict

#create dictionary with years
YearDict = create_yr_dict(state_dict, "All Candidates")



#append district to dictionary such that {state name: {year: {district: url}}}
def create_dist_dict(YrDict):
    for state in YrDict:
        for year in YrDict[state]:
            url = YrDict[state][year]
            soup = soup_url(url)
            district = soup.findAll('h5')
            didict = {}
            for item in district:
                a = str(item)
                district_link = a[a.find('href="')+6:a.find('" style')]
                district_link = district_link.replace('&amp;' , '&')
                district_name = a[a.find(' ">')+3:a.find(' </a>')]
                didict[district_name] = url + district_link
            YrDict[state][year] = didict 
    return YrDict
    
DistrictDict = create_dist_dict(YearDict)

#append AC urls to the dictionary, such that {state name: {year: {district: {ac: url}}}}
def create_AC_dict(DistrictDict):
    for state in DistrictDict:
        for year in DistrictDict[state]:
            for district in DistrictDict[state][year]:
                url = DistrictDict[state][year][district]
                soup = soup_url(url)
                table = soup.find("table", {"id": "table2"})
                ac_href = table.findAll('a', href = True)
                raw_ac = []
                raw_ac = str(ac_href)
                raw_ac = raw_ac.split(', <') 
                new_ac = []
                for ac in raw_ac: 
                    ac = "<" + ac 
                    new_ac.append(ac)
                correct_ac = []
                for a in new_ac:
                    if '><' not in a:
                        correct_ac.append(a)
                # ac_href = ac_href.replace('&amp;', '&')
                # re.compile('constituency_id'))
                acdict = {}
                for a in correct_ac:
                    ac_link = a[a.find('href="')+6:a.find('">')]
                    ac_link = ac_link.replace('&amp;' , '&')
                    ac_name = a[a.find('">')+2:a.find('</a>')]
                    if ac_link[:4] == "http":
                        acdict[ac_name] = ac_link
                    else:
                        acdict[ac_name] = url[:url.find('index.php?')] + ac_link
                DistrictDict[state][year][district] = acdict
    return DistrictDict

masterdict = create_AC_dict(DistrictDict)


#append candidate data to the dictionary, such that {state name: {year: {district: {ac: url}}}}
def create_candidate_dict(masterdict):
    for state in masterdict:
        for year in masterdict[state]:
            for district in masterdict[state][year]:
                for ac in masterdict[state][year][district]:
                    tableData = []
                    url = masterdict[state][year][district][ac]
                    soup = soup_url(url)
                    # if soup.title.string.lower().find('delete') == -1:
                    if soup.find("table",{"id":"table1"}) != None:
                        table = soup.find("table",{"id":"table1"})
                        allRows = table.findAll('tr')
                        for row in allRows:   
                            eachRow = []
                            cells = row.findAll('td')
                            for cell in cells:
                                eachRow.append(cell.text.encode('utf-8').strip())
                            tableData.append(eachRow)
                        tableData = [x for x in tableData if x != []]
                        CandidateCol = [x[0] for x in tableData]
                        PartyCol = [x[1] for x in tableData]
                        CrimesCol = [x[2] for x in tableData]
                        EducationCol = [x[3] for x in tableData]
                        AgeCol = [x[4] for x in tableData]
                        AssetsCol = [x[5] for x in tableData]
                        LiabilityCol = [x[6] for x in tableData]
                        canddict = {}
                        canddict = {
                                    "Candidate Name" : CandidateCol,
                                    "Party" : PartyCol,
                                    "Criminal Cases" : CrimesCol,
                                    "Education" : EducationCol,
                                    "Age" : AgeCol,
                                    "Assets" : AssetsCol,
                                    "Liabilities" : LiabilityCol}
                        masterdict[state][year][district][ac] = canddict      
    return masterdict

masterdict = create_candidate_dict(masterdict)



