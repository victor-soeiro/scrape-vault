#!/usr/bin/env python
# coding: utf-8

# <div style="color: white;
#             display: fill;
#             background-color: #4A4F55;
#             border-radius: 5px;
#             font-family: Verdana;
#             letter-spacing: .5px;
#             display: flex;
#             justify-content: center;">
#     <h1 style="padding: 1.5rem;
#                color: white;
#                text-align: center;
#                margin: 0 auto;
#                font-size: 25px;"> 
#         A24 Films - A IMDB Web Scraping Project 
#     </h1>
# </div>

# <p style="text-align: center; font-family: sans-serif; font-weight: bold; font-size: 15px; margin-bottom: 20px">
#     If you find this notebook useful, support starring this repository.
# </p>

# <div style="color: white;
#             display: fill;
#             background-color: #4A8573;
#             border-radius: 5px;
#             font-family: Verdana;
#             letter-spacing: .5px;
#             display: flex;;">
#     <h1 style="padding: 1rem;
#                color: white;
#                text-align: center;
#                margin: 0 auto;
#                font-size: 20px;"> 
#         Libraries 
#     </h1>
# </div>

# IMDB has its own API for consumption of its data, but we only have 100 API calls for day. A24 contains more movies than that, so let's practice our skills by scraping the data from an HTML.
# 
# We will use the Requests and BS4 package for this project.

# In[3]:


import json
import requests
from framework import get, get_soup, post

from bs4 import BeautifulSoup
from math import ceil


# <div style="color: white;
#             display: fill;
#             background-color: #4A8573;
#             border-radius: 5px;
#             font-family: Verdana;
#             letter-spacing: .5px;
#             display: flex;
#             margin-top: 20px;">
#     <h1 style="padding: 1rem;
#                color: white;
#                text-align: center;
#                margin: 0 auto;
#                font-size: 20px;"> 
#         Defining Variables 
#     </h1>
# </div>

# Searching on the IMDB site I found the company ID of A24.

# In[4]:


COMPANY_ID = 'co0390816'


# The site uses a page system, but based on the number of results. Each page contains only 50 movies, so the second page starts with reference 51.

# In[5]:


URL = 'https://www.imdb.com/search/title/?companies={}&start={}&ref=adv_nxt&view=simple'


# We need to get the total number of titles to get the number of pages.

# In[6]:


soup = get_soup(URL.format(COMPANY_ID, 1))


# In[7]:


titles = int(soup.find('div', class_='desc').span.text.split(' ')[-2])
pages = ceil(titles / 50)

print('Number of Titles:', titles)
print('Number of Pages:', pages)


# 

# In[8]:


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32",
    'accept-language': 'en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}


# <div style="color: white;
#             display: fill;
#             background-color: #4A8573;
#             border-radius: 5px;
#             font-family: Verdana;
#             letter-spacing: .5px;
#             display: flex;
#             margin-top: 20px;">
#     <h1 style="padding: 1rem;
#                color: white;
#                text-align: center;
#                margin: 0 auto;
#                font-size: 20px;"> 
#         Collecting Data 
#     </h1>
# </div>

# In[47]:


def get_title_information(url: str):
    soup = get_soup(url, headers=headers)

    data = dict()
    meta = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).text)['props']['pageProps']['aboveTheFoldData']
    if meta['productionStatus']['currentProductionStage']['id'] == 'in_development':
        return

    from pprint import pprint
    #pprint(meta)

    # data['type'] = meta['@type']

    data['certificate'] = meta['certificate']['rating']
    data['credits'] = meta['credits']['total']
    data['release_date'] = f'{meta["releaseDate"]["month"]}/{meta["releaseDate"]["day"]}/{meta["releaseDate"]["year"]}'
    data['countries_of_origin'] = [i['id'] for i in meta['countriesOfOrigin']['countries']]
    data['genres'] = [i['id'] for i in meta['genres']['genres']]
    data['imdb'] = meta['id']
    data['keywords'] = [i['node']['text'] for i in meta['keywords']['edges']]
    data['status'] = meta['meta']['publicationStatus']
    data['metacritic'] = meta['metacritic']['metascore']['score']
    data['title'] = meta['originalTitleText']['text']
    data['plot'] = meta['plot']['plotText']['plainText']
    data['rating'] = meta['ratingsSummary']['aggregateRating']
    data['vote_count'] = meta['ratingsSummary']['voteCount']
    data['reviews'] = meta['reviews']['total']
    data['runtime'] = meta['runtime']['seconds']

    return data


# In[48]:


get_title_information('https://www.imdb.com/title/tt6710474')


# In[10]:


def get_page_titles(reference: str, company: str = COMPANY_ID):
    """ Collect all titles from a IMDb page. """

    soup = get_soup(URL.format(company, reference), headers=headers)

    data = []
    lister_list = soup.findAll('span', {'class': 'lister-item-header'})
    for title in lister_list:
        if title.find('small'):
            continue

        title_link = 'https://www.imdb.com' + title.find('a')['href']
        print(title_link)
        title_info = get_title_information(title_link)
        data.append(title_info)

    return data


# In[11]:


def get_all_titles_from_company():
    """ """
    pass


# Needs to delete:
# 
# * production_companies
# * filming_locations
# * also_known_as
# * released_year
# * opening_weekend_us_&_canada
# * official_sites
# * writers
# * stars

# In[ ]:




