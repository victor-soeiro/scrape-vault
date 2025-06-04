#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd


# In[11]:


df = pd.read_csv('not-cleaned/data.csv')
df.head()


# In[12]:


columns_to_drop = [
    'service_time',
    'manufacturer',
    'release_date',
    'weight',
    'inspection_report',
    'top_speed',
    'climb',
    'brake',
    'integrity',
    'also_known_as',
    'paradox_sim.',
    'community_nickname(s)',
    'real_name',
    'operator_rec._1',
    'operator_rec._2',
    'full_name',
    'age',
    'english',
    'model',
    'leitmotif',
    'operator_rec.',
    'korean',
    'chinese',
    'japanese',
    'illustrator',
    'produced_in'
]


# In[13]:


df.drop(columns_to_drop, axis=1, inplace=True)


# In[14]:


df.shape


# In[15]:


percent_missing = df.isnull().sum() * 100 / len(df)
percent_missing.sort_values(ascending=False)


# In[16]:


df.to_csv('data.csv', index=False)


# In[ ]:




