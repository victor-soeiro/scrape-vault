#!/usr/bin/env python
# coding: utf-8

# ## **Tapas - WebScraping Project**
# 

# <img src="https://scontent-gig2-1.xx.fbcdn.net/v/t1.6435-9/67064783_1590702974393670_4265688551187808256_n.jpg?_nc_cat=111&ccb=1-5&_nc_sid=e3f864&_nc_eui2=AeE_Z804yhpjzF7_JAf_PnTHWNIs4NRB_E5Y0izg1EH8TsrAj0E_gbN2MOy5PvW0ZgkHk7rXzlw_12lQjclXLBEf&_nc_ohc=65rkqjb3FksAX-ELv1a&_nc_ht=scontent-gig2-1.xx&oh=00_AT8lz-1dWIgLQ38E6C1uNO00oTxw-H6hXQQ0BeN7Ep7suw&oe=6297B2C6" width="100%">

# ### **Introduction**

# Established in 2012, headquartered in Los Angeles with key global operations in Seoul, South Korea, and Beijing, China, Tapas Media is one of the fastest-growing digital publishing platforms of webcomics and novels in North America. Tapas has created a community of more than 9M registered users with stories from 68,000 creators and published over 99,000 stories to date.
# 
# **Disclaimer:** This is a personal project to practice webscraping skills and exploratory data analysis. I do not recommend to use for other purposes. Use it at your own risk.

# ### **Libraries**

# Tapas has a system page that uses JSON files to handle the page items. It's easy to deal and manipulate. We will use only the main tools for the project: 
# 
# * Request for the website requests.
# * Pandas for file handling.
# * bs4 for HTML extraction. 
# 
# If you wanna replicate, maybe you need to install these packages with PIP command.

# In[1]:


import time
from framework import get, get_soup
import pandas as pd

from tqdm.notebook import tqdm, tnrange
from bs4 import BeautifulSoup


# ### **Variables**

# Let's define our URL for scraping.

# In[2]:


url = 'https://tapas.io/comics'


# We have some important parameters to define in our requests.
# 
# * **b**: ALL (List all items).
# * **g**: 0 (Items genre set to All Genres).
# * **f**: PRM (Only premium items).
# * **s**: LIKE (Ordered by likes).
# * **pageNumber**: The dynamic page value.
# * **pageSize**: 20 (Number of items per page).
# 
# Let's focus only on the premium webtoons, because the free content has above 80k items. We will only manipulate the **pageNumber** parameter for the scraper. 

# In[4]:


params = {
    'b': 'ALL',
    'g': 0,
    'f': 'PRM',
    's': 'LIKE',
    'pageNumber': 1,
    'pageSize': 20
}


# For the server not forbbiden our access, we need to pass a user agent and accepts only json files for manipulation.

# In[5]:


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
}

json_headers = headers.copy()
json_headers['accept'] = 'application/json'


# ## **Scraper**

# I will use a for loop to scrape the data from the pages, but I need to know how many pages are available. Usually, we can extract the page number from the HTML, in this case, we can check directly from the JSON file. Let's make the request to check it.

# In[6]:


req = get(url, headers=json_headers, params=params)
req.status_code


# We can check the total page inside the **pager** key in the JSON.

# In[7]:


total_page = req.json()['data']['pager']['total_page']
total_page


# There is a total of 37 pages with 20 items each. This give us a maximum of 740 items. If one error occurs in the process, we will lose all the progress. One of the possibilities is to write directly into a file, but it will be a heavy memory consumer. As we are dealing with a notebook, I will write the data on a dictionary, as the key is the page, and the value it's the manga metadata.

# In[17]:


pages_data = {}


# The most of informations about the webtoons are not available on the search page. In the info page of the webtoon we can access an amount of information. We will make a new request for each item to get these information. Let's encapsulate the scrap process on a function.

# In[16]:


def get_item_information(info):
    soup = get_soup(info, headers=headers)

    creators = [c.text for c in soup.find('ul', attrs={'class': 'creator-section'}).findAll('a', attrs={'class': 'name'})]
    genres = [g.text for g in soup.find('div', attrs={'class': 'info-detail__row'}).findAll('a')]
    stats = soup.find('div', attrs={'class': 'stats'}).findAll('a')
    views = stats[0]['data-title']
    subscribers = stats[1]['data-title']
    likes = stats[2]['data-title']
    banner = soup.find('div', attrs={'class': 'js-top-banner'})['style'].split(';')[1][22:-1]
    details = soup.find('span', attrs={'class': 'description__body'}).text.strip()
    tags = [t.text for t in soup.findAll('a', attrs={'class': 'tags__item'})]
    episodes = soup.find('p', attrs={'class': 'episode-cnt'}).text.strip().split(' ')[0]
    released = soup.find('li', attrs={'class': 'episode-list__item'}).find('p', attrs={'class': 'additional'}).span.text

    return [
        creators, genres, views, subscribers, likes, banner, details, tags, episodes, released
    ]


# And now for the main part, let's scrape!

# In[20]:


for i in tnrange(total_page, desc='Pages'):
    page = i + 1 
    params['pageNumber'] = page

    if pages_data.get(page, []):
        continue

    req = get(url, headers=json_headers, params=params)
    html = req.json()["data"]["body"]
    soup = BeautifulSoup(html, "html.parser")
    data = []
    items = soup.findAll('li')
    for item in tqdm(items, desc=f'Items of Page {page}'):
        title = item.find('img')['alt']
        item_id = item.div.a['data-series-id']
        # genre = item.p.a.text
        # stats = item.find('span', attrs={'class': 'item__stat'}).text
        link = 'https://tapas.io' +  item.div.a['href'] + '/info'
        cover = item.find('img')['src']

        item_data = [title, item_id, link, cover]
        item_data.extend(get_item_information(link))

        data.append(item_data)

        time.sleep(1)

    pages_data[page] = data


# In[26]:


pages_data[1][0]


# Above we can see the information about **My Gentle Giant**. The data are not specified, so let's define a columns variable.

# In[22]:


columns = [
    'title', 'item_id', 'link', 'cover', 'creators', 'genres', 'views', 'subscribers', 'likes', 'banner', 'details', 'tags', 'episodes', 'released'
]


# Each key of the dictionary contains a page data. Let's mount the data on a new list and pass to a dataframe.

# In[27]:


full_data = []
for i in pages_data.values():
    full_data.extend(i)

df = pd.DataFrame(full_data, columns=columns)
df.head()


# Some data need to be processed. Like the **views**, **subscribers** and **likes** columns. Let's save this data on a file!

# In[28]:


df.to_csv('data.csv', index=False)


# ### **Contact**
# 
# If you have any questions or suggestions, send me an email to victor.soeiro.araujo@gmail.com
