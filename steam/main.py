#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from framework import get, get_soup
from bs4 import BeautifulSoup


# In[2]:


url = 'https://steamdb.info/apps/page{}/'


# In[15]:


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32",
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'referer': 'https://steamdb.info/',
    'cookie': '__Host-steamdb=0%3B3875264%3B96b066b830263c10e64f53566a4aa3fd13214f70; __Host-cc=ar; cf_chl_2=fad3a9fa26e234c; cf_chl_prog=x12; cf_clearance=Eve2n.HFHigF1BPHip2bgrKc4YPJFareTsRTne63Wg4-1657425143-0-150'
}


# In[12]:


session = requests.Session()


# In[16]:


req = get(url.format("1"), headers=headers)
req.status_code


# In[17]:


print(req.text)


# In[ ]:




