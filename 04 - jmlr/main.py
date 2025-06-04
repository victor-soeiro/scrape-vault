#!/usr/bin/env python
# coding: utf-8

# ## **Journal of Machine Learning Research (JMLR) - WebScraping Project**

# > **Disclaimer:** This is a personal project to practice webscraping skills and exploratory data analysis. I do not recommend to use for other purposes. Use it at your own risk.

# ### **Libraries**

# All volumes and papers of JMLR are on only one page. The scraping process will use only the main tools. 
# 
# > **If you wanna replicate, maybe you need to install some of the packages with PIP command.**

# In[1]:


import re
import pandas as pd
from framework import get_soup

from tqdm.notebook import tqdm


# ### **Variables**

# Let's define the URL to request the volumes HTML page.

# In[2]:


url = 'https://www.jmlr.org/papers/'


# ### **Volumes**

# Let's start the extracting process of the volumes.

# In[3]:




# Parsing the HTML to a BeautifulSoup object.



vols_soup = get_soup(url)


# The volumes will be on a list to loop and scrape the papers.

# In[5]:


vols = []


# The information it's stored on a *font* tag with a *volume* class. It's easy to scrape the data.

# In[7]:


content = vols_soup.findAll('font', {'class': 'volume'})
for i in content:
    container = i.parent 
    href = container['href']
    if 'papers' in href:
        href = 'https://www.jmlr.org' + href
    else:
        href = url + href

    volume = i.text.strip()   
    vols.append(dict(href=href, volume=volume))


# Let's check the last released volume!

# In[8]:


vols[0]


# ### **Papers**

# If one error occurs in the scraping process, we will lose all the progress. One of the possibilities is to write directly into a file, but it will be a heavy memory consumer. As we are dealing with a notebook, I will write the data in a dictionary, as the key is the volume, and the value it's the paper.
# 
# Maybe it's not the best idea, but it will be enough for this project.

# In[12]:


papers_per_volume = {}


# Unfortunately, over the papers, the data are not distributed uniformly. We will need more steps to scrape all the data correctly. For each volume, it has a set of papers. Let's scrape each one of them and store them in the dictionary.

# In[13]:


for v in tqdm(vols):
    url = v['href']
    volume = v['volume']

    if papers_per_volume.get(volume, []):
        continue 


    soup = get_soup(url)

    papers = []
    papers_container = soup.findAll('dl')
    for p in papers_container:        
        dt = p.find('dt')
        dd = p.find('dd')

        if dt.find('dd'):
            title = list(dt.children)[0].text.strip()
        else:
            title = dt.text.strip()

        authors = dd.b.text.strip().split(', ')

        desc = dd.b.nextSibling.text.strip()        
        year = desc.split(' ')[-1].replace('.', '')  
        pages_string = desc[desc.find(":")+1:desc.rfind(",")]
        pages_values = re.findall(r'[0-9]+', pages_string)
        pages = int(pages_values[1]) - int(pages_values[0]) + 1

        code_string = dd.find(string='code')
        if code_string:
            code = code_string.parent['href']
        else:
            code = ''

        pdf = dd.find(string='pdf')
        if pdf:
            link = pdf.parent['href']
        else:
            link = dd.find(string='[pdf]').parent['href']

        if 'www' not in link:
            link = 'https://www.jmlr.org' + link

        papers.append(dict(title=title, volume=volume, authors=authors, year=year, pages=pages, link=link, code=code))

    papers_per_volume[volume] = papers


# Let's see the first two papers of the first volume!

# In[14]:


papers_per_volume['Volume 1'][:2]


# ### **Save data**

# As the papers are per volume, let's group them all on a list!

# In[16]:


full_data = []
for p in papers_per_volume.values():
    full_data.extend(p)


# Now, we can pass to a DataFrame and check the table.

# In[17]:


df = pd.DataFrame(full_data)
df.head()


# And finally, let's save the data.

# In[18]:


df.to_csv('data.csv', index=False)

