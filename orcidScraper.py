
# coding: utf-8

# In[1]:

import requests
import secrets
from datetime import date
import csv
import json
import pprint
import math


# The first step is to use credentials to get a token. These can be generated from an individual ORCID account page under "Developer Tools." This search uses the public API. 
# 
# Modify the empty "secrets.py" file in this directory to load in credentials.

# In[2]:

url = 'https://pub.orcid.org/oauth/token'
headers = {"Accept":"application/json"} 
payload = {'client_id': secrets.clientID(), 
           'client_secret': secrets.secret(),
           'scope':'/read-public',
           'grant_type' : 'client_credentials'}


# In[3]:

r = requests.post(url, headers = headers, data = payload)


# In[4]:

token = r.json()['access_token']


# With the token in hand, we can now execute queries against the public api. Some documentation on how to format a search query can be found at [http://members.orcid.org/api/tutorial-searching-data-using-api](http://members.orcid.org/api/tutorial-searching-data-using-api)

# In[53]:

search = '3298+AND+MASON+OR+email:*@gmu.edu+OR+email:*@masonlive.gmu.edu'


# In[54]:

# This is a helper function to get the number of search results for pagination purposes.

def getNumberofResults(search):
    searchURL = 'https://pub.orcid.org/v1.2/search/orcid-bio?q={}'.format(search)
    headers = {"Content-Type":"application/orcid+json", 
               "Accept":"application/json", 
               "Authorization":"Bearer {}".format(token)}
    r = requests.get(searchURL, headers = headers)
    return(r.json()['orcid-search-results']['num-found'])


# In[55]:

# This is the search function, which is called in the `queryOrcidApi` function below.

def orcidSearch(search, token, start, rows):
    searchURL = 'https://pub.orcid.org/v1.2/search/orcid-bio?q={}&start={}&rows={}'.format(search, str(start),str(rows))
    headers = {"Content-Type":"application/orcid+json", 
               "Accept":"application/json", 
               "Authorization":"Bearer " + token}
    r = requests.get(searchURL, headers = headers)
    return(r)


# In[56]:

# This is the compiled search function which takes the token from above and the search string. The API only return 100
# results at a time, so the function first determines if the total is under 100. If yes, it pull them all. If it is
# greater than 100, it iterates through as many times as it takes to get all of the pages of 100 results and returns
# them as a list.

def queryOrcidApi(search, token):
    num_results = getNumberofResults(search)
    print('{} search results found'.format(num_results))
    results = []
    if num_results < 100:
        start = 0
        rows = num_results
        r = orcidSearch(search, token, start, rows)
        results.append(r.json())
    else:
        for i in range(math.ceil(num_results/100)): 
            start = i * 100
            print('Pulling records starting from {}'.format(start))
            rows = 100 
            r = orcidSearch(search, token, start, rows)
            results.append(r.json())
    return(results)


# In[57]:

results = queryOrcidApi(search, token)


# With all of the search results in hand, we can now create a single list of the individual result dictionaries.

# In[49]:

searchResults = []

for each in results:
    blob = each['orcid-search-results']['orcid-search-result']
    for blip in blob:
        searchResults.append(blip)


# In[50]:

len(searchResults)


# Finally, we can write the results to a CSV file. Some of the results (3) did not include the family and given name in the public information. As a result, here I am checking for these fields of interest and including a blank value if it is not provided. The error message will alert if additional missing values are encountered.

# In[51]:

with open('{}-orcid-output.csv'.format(str(date.today())), 'wt') as f:
    writer = csv.writer(f)
    writer.writerow(["family-name", "given-name", "orcid-id", "orcid-url"])
    for each in searchResults:
        try:
            family_name = each['orcid-profile']['orcid-bio']['personal-details']['family-name']['value']
        except:
            family_name = ""
        try:
            given_name = each['orcid-profile']['orcid-bio']['personal-details']['given-names']['value']
        except:
            given_name = ""
        try:
            identifier = each['orcid-profile']['orcid-identifier']['path']
            uri = each['orcid-profile']['orcid-identifier']['uri']
        
        except TypeError:
            print('There was an error processing record {}'.format(searchResults.index(each)))
            
        writer.writerow([family_name, given_name, identifier, uri])


# In[ ]:



