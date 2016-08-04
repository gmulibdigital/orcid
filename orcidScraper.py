
# coding: utf-8

# In[1]:

import requests
import secrets


# In[2]:

url = 'https://pub.sandbox.orcid.org/oauth/token'
headers = {"Accept":"application/json"} 
payload = {'client_id': secrets.clientID(), 
           'client_secret': secrets.secret(),
           'scope':'/read-public',
           'grant_type' : 'client_credentials'}


# In[3]:

r = requests.post(url, headers = headers, data = payload)


# In[4]:

token = r.json()['access_token']


# In[5]:

searchURL = 'https://api.sandbox.orcid.org/v1.2/search/orcid-bio?q=3298'
headers = {"Content-Type":"application/orcid+json", "Accept":"application/json", "Authorization":"Bearer " + token}


# In[6]:

r = requests.get(searchURL, headers = headers)


# In[7]:

r.json()


# In[ ]:



