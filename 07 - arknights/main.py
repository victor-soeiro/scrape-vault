#!/usr/bin/env python
# coding: utf-8

# ## Arknights - Webscraping Project

# <img src="https://gamepress.gg/arknights/sites/arknights/files/2021-01/WhoIsRealBanner_0.jpeg" width="100%">

# 

# 

# In[1]:


from framework import get_soup
import pandas as pd

from tqdm.notebook import tqdm


# 

# In[2]:


URL = 'https://arknights.fandom.com/wiki/Operator/{}-star'


# 

# In[3]:


STARS = range(1, 7)


# 

# In[4]:


operators_urls = []


# 

# In[5]:


for star in STARS:
    url = URL.format(star)


    soup = get_soup(url)

    table = soup.find('table', attrs={'class': 'mrfz-btable'}).tbody
    for row in table.findAll('tr'):
        columns = row.findAll('td')
        if not columns:
            continue

        operators_urls.append('https://arknights.fandom.com' + columns[1].a['href'])


# 

# In[6]:


operators_urls[:5]


# 

# In[7]:


len(operators_urls)


# 

# In[8]:


operators = []


# 

# In[9]:


for url in tqdm(operators_urls):


    soup = get_soup(url)

    operator = {}

    op_info = soup.find('div', attrs={'class': 'op-info'}).table.tbody
    op_info_rows = op_info.findAll('tr')
    img_info = op_info_rows[0].td.findAll('span', recursive=False)

    operator['name'] = op_info_rows[0].find('br').nextSibling.text.strip()
    operator['class'] = img_info[0].a['title']
    operator['branch'] = img_info[1].a['title']
    operator['faction'] = img_info[2].a['title']
    operator['stars'] = op_info_rows[0].find('a', attrs={'class': 'mw-redirect'})['title']
    operator['position'] = op_info_rows[1].findAll('td')[-1].text.strip()
    operator['tags'] = [t.text.strip() for t in op_info_rows[2].findAll('td')[-1].findAll('div')]
    operator['trait'] = op_info_rows[3].findAll('td')[-1].text.strip()
    operator['availability'] = op_info_rows[4].findAll('td')[-1].text.strip()
    operator['icon'] = op_info.find('div', attrs={'class': 'floatnone'}).img['data-src']
    operator['description'] = op_info_rows[0].findAll('td')[-1].findAll('div', recursive=False)[-1].div.text.strip()
    operator['phrase'] = op_info_rows[0].findAll('td')[-1].find('i').text.strip()

    for info in soup.findAll('div', attrs={'class': 'pi-item'}):
        operator[info.h3.text.strip().replace(' ', '_').lower()] = info.div.text.strip()

    attrs = ['base', 'elite_1', 'elite_2', 'max', 'trust']
    attrs_table = soup.findAll('table', attrs={'class': 'mrfz-btable'})[1].tbody
    for attr in attrs_table.findAll('tr')[1:]:
        attr_text = attr.th.text.strip().replace(' ', '_').lower()
        columns = attr.findAll('td')
        for i, col in enumerate(columns):
            operator[attrs[i] + '_' + attr_text] = col.text.strip()

    image_collection = soup.find('div', attrs={'class': 'pi-image-collection'})
    if image_collection:
        images = [img.a['href'] for img in image_collection.findAll('figure')]
        captions = [c.text.strip() for c in image_collection.findAll('li')]
        operator['images'] = {c: i for c, i in zip(captions, images)}
    else:
        operator['images'] = {operator['name']: soup.find('figure', attrs={'class': 'pi-item pi-image'}).a['href']}

    operators.append(operator)


# 

# In[10]:


df = pd.DataFrame(operators)
df.head()


# 

# In[12]:


df.to_csv('src/data.csv', index=False)


# 
