#!/usr/bin/env python
# coding: utf-8

# In[1]:


from framework import get_soup
import pandas as pd

from tqdm.notebook import tqdm


# In[2]:


url = 'https://afk-arena.fandom.com/wiki/Heroes'


# In[3]:



# In[4]:


soup = get_soup(url)


# In[10]:


items = [i for c in soup.findAll('table', attrs={'class': 'wikitable'})[1:] for i in c.tbody.findAll('tr')][1:]
len(items)


# In[14]:


def get_item_information(url):

    soup = get_soup(url)

    data = {}

    data['name'] = soup.find('h2', attrs={'data-source': 'name'}).text.strip()
    title = soup.find('h2', attrs={'data-source': 'title'})
    if title:
        data['title'] = title.text.strip()

    stats = soup.findAll('div', attrs={'class': 'pi-item'})
    for s in stats:
        key = s.h3.text.strip()
        if s.find('ul'):
            data[key] = [list(u)[0].text.strip() for u in s.findAll('li')]
        elif s.find('img'):
            data[key] = s.div.text.strip()
        else:
            data[key] = list(s.div.children)[0].text.strip()

    data['image'] = soup.find('a', attrs={'class': 'image-thumbnail'})['href']

    return data


# In[15]:


data = []


# In[16]:


for i in tqdm(items):
    if i.find('th'):
        continue

    columns = i.findAll('td')
    link = 'https://afk-arena.fandom.com' + columns[2].a['href']

    item = get_item_information(link)
    item['link'] = link

    data.append(item)


# In[17]:


data[0]


# In[18]:


df = pd.DataFrame(data)
df.head()


# In[19]:


df.shape


# In[21]:


df.to_csv('data.csv', index=False)

