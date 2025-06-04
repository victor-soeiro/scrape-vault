#!/usr/bin/env python
# coding: utf-8

# ## **Webtoons - WebScraping Project**

# <img src="https://media-exp1.licdn.com/dms/image/C561BAQF7mhzUFFpGQg/company-background_10000/0/1588199218989?e=2147483647&v=beta&t=jmdPaw4ITMyXHwfx5vv7QJ6TnzTNhYhpuX3wUfLrCgg" width="100%">
# 
# > **Disclaimer:** This is a personal project to practice webscraping skills and exploratory data analysis. I do not recommend to use for other purposes. Use it at your own risk.

# ### **Libraries**

# All comics on webtoons are on only one page, but it has extra information on their unique page. The scraping process will use only the main tools. 
# 
# > **If you wanna replicate, maybe you need to install some of the packages with PIP command.**

# In[1]:


import math
import requests
from framework import get, get_soup
import pandas as pd

from tqdm.notebook import tqdm
from bs4 import BeautifulSoup


# Let's define the URL to request the comics HTML page.

# In[2]:


url = 'https://www.webtoons.com/en/genre'


# Let's start the extracting process of the comics.

# In[3]:




soup = get_soup(url)


# Each container has comics from a genre. It's a total of 16 containers and over 1400 comics. Let's collect all the comics.

# In[5]:


containers = soup.findAll('ul', attrs={'class': 'card_lst'})
len(containers)


# In[6]:


items = [i for c in containers for i in c.findAll('li')]
len(items)


# To collect the release date information requires knowing how many episodes pages have to make another request. Let's encapsulate it on a function. 

# In[7]:


def get_item_released_information(url, page):
    bs = get_soup(url, params={'page': page})

    first_episode = bs.find('ul', attrs={'id': '_listUl'}).findAll('li')[-1]
    released_data = first_episode.find('span', attrs={'class': 'date'}).text.strip()

    return released_data


# The comic information is on a unique page. Let's encapsulate it too on a function.

# In[8]:


def get_item_information(url):
    bs = get_soup(url)

    item_data = {}

    item_data['webtoon_id'] = url.split('=')[-1]
    item_data['title'] = bs.find('h1', attrs={'class': 'subj'}).text.strip() 
    item_data['genre'] = bs.find('h2', attrs={'class': 'genre'}).text.strip()
    item_data['thumbnail'] = bs.find('span', attrs={'class': 'thmb'}).img['src']
    item_data['summary'] = bs.find('p', attrs={'class': 'summary'}).text.strip()
    item_data['episodes'] = bs.find('ul', attrs={'id': '_listUl'}).findAll('li')[0]['data-episode-no']

    authors_container = bs.find('div', attrs={'class': '_authorInnerContent'})
    authors_categories = authors_container.findAll('p', attrs={'class': 'by'})
    authors_names = authors_container.findAll('h3', attrs={'class': 'title'})
    for c, n in zip(authors_categories, authors_names):
        item_data[c.text.strip()] = n.text.strip()

    stats_container = bs.find('p', attrs={'class': 'summary'}).parent.find('ul').findAll('li')
    for s in stats_container:
        item_data[s.span.text.strip()] = s.em.text.strip()

    last_page = int(math.ceil(int(item_data['episodes']) / 10))
    item_data['released_date'] = get_item_released_information(url, last_page)
    item_data['url'] = url

    return item_data


# The collected data will be on a list.

# In[18]:


data = []


# Now, let's start the looping process to collect all the information!

# In[19]:


done = []


# In[20]:


for i in tqdm(items):    
    href = i.a['href']
    if href in done:
        continue

    item_data = get_item_information(href)
    item_data['cover'] = i.find('img')['src']
    item_data['likes'] = i.find('em', attrs={'class': 'grade_num'}).text.strip()  

    data.append(item_data)
    done.append(href)


# The scraping process took around 35 minutes, with two requests per comic. 
# 
# As the data are a list of dictionaries, we don't need to define all the column's names. Let's parse the data to a DataFrame.

# In[21]:


df = pd.DataFrame(data)
df.head()


# And finally, let's save the data.

# In[24]:


df.to_csv('data.csv', index=False)


# In[ ]:




