#!/usr/bin/env python
# coding: utf-8

# ## **Anime-Planet: Web Scraping Notebook**

# <img src="https://steemitimages.com/DQmeRTV7T2QwH73NyV7y8XU96HuBrLXnHHiedMCFw8ZPBnr/FBPcover.png" width="100%">

# ## **Preludes** 
# 
# Comics are popular among people of all ages. It's a form of art, a narrative expressed as draws. Since the late 20th century, the publishers have translated mangas (comics originating from Japan) to the world. The fast growth of the popularity gained a significant worldwide audience. In 2021 in the US, mangas made up [76% of overall comics and graphic novels sales](https://www.animenewsnetwork.com/news/2022-03-01/npd-bookscan-via-the-beat-manga-made-up-76.71-percent-of-adult-fiction-graphic-novel-sales-in-2021/.182296) according to NPD Group. This projects aims to scrape the mangas available on [Anime-Planet](https://www.anime-planet.com/), a great source to search for mangas and animes. This data will be stored on a CSV file, and available on GitHub and Kaggle for study purposes.
# 
# I will consider that mangas includes manhwa (originating from Korea) and manhua (originating  from China).
# 
# **Disclaimer:** This is a personal project to practice webscraping skills and exploratory data analysis. I do not recommend to use for other purposes. Use it at your own risk.

# ## **Yoshi Yoshi**

# To those who didn't understood the term "Yoshi Yoshi", it means to start an activity with entusiasm. Let's start the WebScraping on Anime-Planet!

# ### **Libraries**

# For most web scraping projects, I will use only requests and bs4. In this project, I will use pandas to facilitate the file handling and NumPy to handle the NaN values (rarely it will occur). I'm using an Anaconda environment, so it's easy to import the libraries, but if you want to replicate, maybe you need to install the libraries with the pip command.

# In[1]:


import numpy as np
import pandas as pd
from framework import get_soup
import time

from tqdm.notebook import tnrange
from bs4 import BeautifulSoup


# ### **Variables**

# All mangas are available on a path on Anime-Planet Website. The page system uses an URL parameter to access the content. Let's define the URL and the end page number.

# In[2]:


main_url = 'https://www.anime-planet.com/manga/all'


# In[3]:


end_page = 2028


# ### **Scraping**

# I will encapsulate the repetitive code on a function to modify in case of need. 
# 
# One of the errors of web scraping is to call an object function that is None. It will raise an error that will interrupt the scraping process. I already checked the Anime-Planet website, and we only need to create a function to check if the object is None, if True returns the text on it or if False returns a NaN value.

# In[4]:


def check_text(value):
    if value:
        return value.text

    return np.nan


# It's funny how the data is available on the page. When the mouse it's over the manga, it will display a window containing all the metadata. As we are scraping, all the hover information is contained in the title tag of the item HTML. This string needs to be parsed again on another BeautifulSoup object. 
# 
# Now, it's easy to scrape all the manga metadata. 

# In[5]:


def item_scraper(item):
    info = item.a['title']
    info_bs = BeautifulSoup(info, 'html.parser')

    title = check_text(info_bs.h5)
    description = check_text(info_bs.p)
    rating = check_text(info_bs.find('div', attrs={'class': 'ttRating'}))
    year = check_text(info_bs.find('li', attrs={'class': 'iconYear'}))
    if year:
        year = str(year).split(' - ')[0]

    if info_bs.h4:
        tags = [t.text for t in info_bs.h4.nextSibling.findAll('li')]
    else:
        tags = []

    cover = item.a.div.img['data-src']

    return [title, description, rating, year, tags, cover]


# As we are dealing with over 2 thousand pages, if one error occurs in the process, we will lose all the progress. One of the possibilities is to write directly into a file, but it will be a heavy memory consumer. As we are dealing with a notebook, I will write the data on a dictionary, as the key is the page, and the value it's the manga metadata.
# 
# Maybe it's not the best idea, but it will be enough for this project.

# In[6]:


pages_data = {}


# And for the main part of the project, let's scrape the pages with a recursive function. We can do it in multiple ways. For visualization with tqdm, we will loop a range object containing an array of pages to call the function to obtain the metadata. But first, let's define the function.

# In[7]:


def scraper(page=1):
    bs = get_soup(main_url, params={'page': page})

    container = bs.find('ul', attrs={'class': 'cardDeck'})
    items = container.findAll('li')

    data = [item_scraper(i) for i in items]
    return data


# Now we can loop the pages with the function using tqdm to observe the loop progress.

# In[8]:


for i in tnrange(end_page, desc='Pages'):
    page = i + 1

    if pages_data.get(page, []):
        continue

    data = scraper(page+1)
    pages_data[page] = data
    time.sleep(1)


# The data are partitioned in the dictionary. Let's unite all the data and save it into a CSV file.

# In[10]:


headers = ['title', 'description', 'rating', 'year', 'tags', 'cover']


# In[11]:


full_data = []
for i in pages_data.values():
    full_data.extend(i)

pd.DataFrame(full_data, columns=headers).to_csv('data.csv', index=False)

