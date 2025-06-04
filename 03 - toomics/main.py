#!/usr/bin/env python
# coding: utf-8

# # **Toomics - WebScraping**

# <img src="https://scontent-gig2-1.xx.fbcdn.net/v/t39.30808-6/260982248_693542505343662_2286003224233358833_n.jpg?_nc_cat=100&ccb=1-5&_nc_sid=e3f864&_nc_eui2=AeHAsLFxSlI7447Vvz1-jLO37QxwPctQ33XtDHA9y1DfdVLoKWRM3bAcXLxAc78bwduwyL9btX8CLgh_I0m_EmLS&_nc_ohc=1nByVYgUztYAX87gLaG&_nc_ht=scontent-gig2-1.xx&oh=00_AT9kz4M9UAPpCZUpwMf10asF_HTS1vot3Clge1bHJ0EnoA&oe=627811D3" width="100%">

# ## **Introduction**

# Toomics is a premium subscription webtoon service with exclusive titles from professional artists. Following the other webscraping projects, as Tapas and Anime-Planet, this projects aims to scrape the webtoons available on [Toomics](https://toomics.com/). The data will be stored on a CSV file, and available on GitHub and Kaggle for research purposes.
# 
# **Disclaimer:** This is a personal project to practice webscraping skills and exploratory data analysis. I do not recommend to use for other purposes. Use it at your own risk.

# ## **Let's Start**

# ### **Libraries**

# This is a simple project, all the toons and comics are presented in a single page. We will make only one request and extract all the information with **bs4**. The file handling we will use Pandas! So, let's import those libraries! If you wanna replicate this notebook, maybe you need to install the packages with PIP command.

# In[26]:


import requests
from framework import get, get_soup
import pandas as pd
from bs4 import BeautifulSoup


# ### **Unlimited Power**

# Toomics has a **family safe** mode that not shows all their works. Analyzing the requests from the page, we need to desactivate the mode and save the cookies. In requests package we can create a session that persists the cookies. It will be very helpfull on the project. 

# In[3]:


session = requests.session()


# When we click to desactivate the family safe mode we are redirected to another page to confirm our identity. After clicking the button, they will return a cookie to we visualize all the webtoons available on the main url. Let's make the requests from our session to persists all the cookies. 

# In[4]:


session.get('https://toomics.com/en/index/set_family_mode/?family_mode=N&return=/en/webtoon/ranking')
session.get('https://toomics.com/en/age_verification?cancel_return=L2VuL3dlYnRvb24vcmFua2luZw~~&return_url=L2VuL3dlYnRvb24vcmFua2luZw~~')


# Now, we can define the main url that will return all the webtoons.

# In[2]:


url = 'https://toomics.com/en/index/set_display/?display=A&return=/en/webtoon/ranking'


# ### **Scraper**

# We have everything in hand to start the scraping process. Let's make the request to retrieve the HTML and start the extraction.

# In[5]:



soup = get_soup(url)
# Great! The connection worked. Let's parse the HTML to a BeautifulSoup object.

# In[6]:




# We will create a function to retrieve all items of the page. It's very directly and intuitive. 

# In[20]:


def get_webtoons():
    items = soup.find('ul', attrs={'class': 'best'}).findAll('li')
    items.extend(soup.find('ul', attrs={'class': 'lists lists-rank'}).findAll('li'))

    data = []
    for i in items:
        title = i.find('h4').text.strip()
        episodes = i.find('span', attrs={'class': 'section_remai'}).text.strip()
        writers = i.find('p', attrs={'class': 'writer'}).text.split(' | ')
        genres = [g.text for g in i.find('p', attrs={'class': 'etc'}).findAll('span')]
        badges = [b.text for b in i.find('div', attrs={'class': 'ico_box'}).findAll('p')]
        link = 'https://toomics.com' + i.div.a['href']
        cover_img = i.find('img')
        cover = cover_img['data-original'] if cover_img.has_attr('data-original') else cover_img['src']

        data.append([title, episodes, writers, genres, badges, link, cover])

    return data


# Defining the columns names for the data table.

# In[8]:


columns = ['title', 'episodes', 'writers', 'genres', 'badges', 'link', 'cover']


# And for the main part of the project, let's start the engine!

# In[23]:


data = get_webtoons()
data_df = pd.DataFrame(data, columns=columns)
data_df.head()


# Great! Our data was collected perfectly. Let's check the shape of data.

# In[24]:


data_df.shape


# We have a total of 639 webtoons. If family safe was activated it would be around 250. Let's save and end the webscraping project.

# In[25]:


data_df.to_csv('data.csv', index=False)


# ### **Contact**
# 
# If you have any questions or suggestions, send me an email to victor.soeiro.araujo@gmail.com
# 
