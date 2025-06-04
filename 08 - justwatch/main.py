#!/usr/bin/env python
# coding: utf-8

# ## **JustWatch - Webscraping Project**

# ### **Introduction**

# **JustWatch** website uses ajax to consumes their API using **GraphQL queries**. The data returns as a **JSON** file. To get the data all we need is the **requests** package. It will not be necessary any other package.
# 
# > **If you wanna replicate, maybe you need to install some of the packages with PIP command.**

# In[1]:


import os
import json
from framework import post
import pandas as pd

from tqdm.notebook import tqdm


# To get the data we need the **reference code** of the streaming to pass as a **GraphQL variable**. I collected an amount of great **streamings** references codes and parses as a **dictionary**!

# In[2]:


streamings = dict(
    amazon='amp',
    disney='dnp',
    darkmatter='dkm',
    rakuten_viki='vik',
    hbo='hbm',
    netflix='nfx',
    hulu='hlu',
    paramount='pmp',
    funimation='fmn',
    crunchyroll='cru',
    starz='stz',
    appletv='atp'
)


# Their **API** uses only one **endpoint** to get the queries. So, we need just change the **parameters** and the **query** to collect the streamings data.

# In[3]:


url = "https://apis.justwatch.com/graphql"


# The website **prevents** a robot to get their data **without** specifying a **User-Agent**. Let's create our request headers!

# In[4]:


headers = {
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32",
    "accept-encoding": "gzip, deflate, br"
}


# This project **doesn't aims to explain how the query works, or how it was modified**, but the post data and the query was stored on a file to save us time. 
# 
# Check the following files:
# 
# - **postData.json**
# - **query.graphql**
# 
# Let's **open** those files and **saves to a variable** to use it.

# In[5]:


with open('src/postData.json', 'r', encoding='utf-8') as file:
    post_data = json.load(file)


# In[6]:


with open('src/query.graphql', 'r', encoding='utf-8') as file:
    query = file.read()


# In[7]:


post_data['query'] = query


# The post data **not specify** which **stream** we will get the data. Let's encapsulate in a function this process.

# In[8]:


def set_streaming(key: str):
    """ Set the streaming on query variables. """

    post_data['variables']['popularTitlesFilter']['packages'] = [streamings[key]]


# Some streamings has **over 3k movies and shows**. The query **only returns** a total of **1960 results**, which is not enough to collect all data. 
# 
# To get through this, we will use the **released year filter** to create a **cluster** of items with **below 1960 items**.

# In[9]:


clusters = [1899, 1950, 1980, 1990, 2000, 2010, 2012, 2014, 2016, 2018, 2020, 2022]


# Let's create a **loop function** to get **all titles available** on a given **streaming**.

# In[10]:


def get_titles(streaming: str, cursor: str = None, titles: list = None, start: bool = True):
    """ Get all titles available of a streaming. """

    if not titles:
        titles = []

    if cursor and not start:
        post_data['variables']['popularAfterCursor'] = cursor
    else:
        post_data['variables']['popularAfterCursor'] = ""

    set_streaming(streaming)
    req = post(url, data=json.dumps(post_data), headers=headers)

    results = req.json()['data']['popularTitles']
    titles.extend(results['edges'])   

    if results['pageInfo']['hasNextPage']:
        cursor = results['pageInfo']['endCursor']
        get_titles(streaming=streaming, cursor=cursor, titles=titles, start=False)

    return titles


# The returned data is well formatted, but it's nested. Let's **parse** the data to a **unique dictionary** containing the correctly fields names.

# In[11]:


def parse_title_content(title: dict):
    """ Parse the title content to a dictionary. """

    content = {}

    title = title['node']
    content['id'] = title['id']
    content['title'] = title['content']['title']
    content['type'] = title['objectType']
    content['description'] = title['content']['shortDescription']
    content['release_year'] = title['content']['originalReleaseYear']
    content['age_certification'] = title['content']['ageCertification']
    content['runtime'] = title['content']['runtime']
    content['genres'] = [i['technicalName'] for i in title['content']['genres']]
    content['production_countries'] = title['content']['productionCountries']
    content['seasons'] = title.get('totalSeasonCount', None)
    content['imdb_id'] = title['content']['externalIds']['imdbId']
    content['imdb_score'] = title['content']['scoring']['imdbScore']
    content['imdb_votes'] = title['content']['scoring']['imdbVotes']
    content['tmdb_popularity'] = title['content']['scoring']['tmdbPopularity']
    content['tmdb_score'] = title['content']['scoring']['tmdbScore']

    credits = [
        {
            'person_id': i['personId'],
            'id': content['id'],
            'name': i['name'],
            'character': i['characterName'],
            'role': i['role']
        } for i in title['content']['credits']
    ]

    return content, credits


# In[12]:


def parse_and_save_data(data: list, save: bool = True, path: str = ''):
    """ Parse a list of titles and save it to a file. """

    titles, credits = [], []
    for d in data:
        t, c = parse_title_content(d)
        titles.append(t)
        credits.extend(c)

    if save:
        titles_df = pd.DataFrame(titles)
        titles_df.to_csv(path+'titles.csv', index=False)

        credits_df = pd.DataFrame(credits)
        credits_df.to_csv(path+'credits.csv', index=False)

    return titles, credits


# All the functions are defined, let's group together to get **all titles available on a streaming**.

# In[13]:


def get_all_titles_by_streaming(streaming: str, save: bool = True, path: str = ''):
    """ Get all titles available on a given streaming. """
    raw = []
    for i in range(len(clusters) - 1):
        filter_range = {'min': clusters[i]+1, 'max': clusters[i+1]}

        post_data['variables']['popularTitlesFilter']['releaseYear'] = filter_range  # Set the filter

        cluster_titles = get_titles(streaming=streaming)
        raw.extend(cluster_titles)

    if save:
        file_path = f'{path}/{streaming}/'
        if not os.path.exists(file_path):
            os.mkdir(file_path)

    titles, credits = parse_and_save_data(data=raw, save=save, path=file_path)

    return titles, credits


# And now, a function to get **all titles** from **all the streamings**!

# In[14]:


def get_all_titles(save: bool = True, path:str = ''):
    """ Get all titles available on the available streamings. """

    all_titles = {}
    for key in tqdm(streamings.keys()):
        titles, credits = get_all_titles_by_streaming(streaming=key, save=save, path=path)
        all_titles[key] = {'titles': titles, 'credits': credits}

    return all_titles


# **Let's save it!**

# In[15]:


data = get_all_titles(save=True, path='data')
len(data['netflix']['titles'])

