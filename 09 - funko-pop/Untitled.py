#!/usr/bin/env python
# coding: utf-8

# ## **Funko Pop - Web Scraping Project**

# ### **Introduction**

# > **If you wanna replicate, maybe you need to install some of the packages with PIP command.**

# ### **Libraries**

# In[1]:


import json
import math
import requests
from framework import get, get_soup, post
import pandas as pd

from tqdm.notebook import tqdm


# ### **Verifying Request and Defining Variables**

# Their API uses only one endpoint to get the queries. Let's define the URL!

# In[2]:


url = 'https://www.funko.com/api/search/template'


# Differently from the Just Watch project, this uses a post request to get the data. 
# 
# The *collection* key value was collected checking the requests from the website, but it's apparently doesn't make any greater difference for this project.

# In[3]:


post_data = {
    'collection': '241066344637',
    'page': 1,
    'pageCount': 50,
    'type': 'shop',
    'sort': {
        'title': 'asc'
    }
}


# To get the data through post request we need to specify which content type we want to receive. 
# 
# Let's create our request headers!

# In[4]:


headers = {
    'content-type': 'application/json', 
}


# Now, let's check if the request is working!

# In[5]:

req = post(url, data=json.dumps(post_data), headers=headers)


# Great! And now the total number of results!

# In[6]:


total = req.json()['total']
total


# The API works with a page system, so let's calculate how many pages there are!

# In[7]:


n_requests = math.ceil(total/post_data['pageCount'])
n_requests


# ### **Scraping**

# The retrieved data from the API contains many unuseful information. We need to encapsulate in a function the data collection of each item!

# In[8]:


def get_item_data(data: dict) -> dict:
    item_data = {
        'uid': data['uid'],
        'title': data['title'],
        'product_type': data['productType'],
        'price': data['price'],
        'interest': data['interest'],
        'license': data['license'],
        'tags': data['tags'],
        'vendor': data['vendor'],
        'form_factor': data['formFactor'],
        'feature': data['feature'],
        'related': data['relatedProducts'],
        'description': data['description'],
        'gid': data['gid'],
        'created_at': data['createdAt'],
        'published_at': data['publishedAt'],
        'updated_at': data['updatedAt'],
        'handle': data['handle'],
        'img': data['media'][0]['src']
    }

    return item_data



# Good. Let's collect all the data!

# In[9]:


data = []

for i in tqdm(range(n_requests)):
    page = i + 1
    req = post(url, data=json.dumps(post_data), headers=headers)
    if req.status_code != 200:
        raise requests.ConnectionError('Connection Error')

    page_data = req.json()['hits']
    for item in page_data:
        data.append(get_item_data(item))


# Checking the total number of items collected.

# In[10]:


len(data)


# Great!! Let's visualize it and save!

# In[11]:


df = pd.DataFrame(data)
df.head()


# In[12]:


df.to_csv('data.csv', index=False)

