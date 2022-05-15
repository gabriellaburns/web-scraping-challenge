#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import re
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## News

# In[3]:


url = "https://mars.nasa.gov/news/"
response = requests.get(url)


# In[4]:


soup = BeautifulSoup(response.text, 'html.parser')

print(soup.prettify())


# In[5]:


results=soup.find('div', class_="slide")
results


# In[6]:


news_title =results.find('div', class_="content_title").text
print(f"News Title :\
      {news_title}")


# In[7]:


#just trying to get the /n out of the soup
news_title_cleaner = news_title.strip('\n')
news_title_cleaner


# In[8]:


news_p = soup.find('div', class_="rollover_description_inner").text
print(f"News Blurb :\
      {news_p}")


# In[10]:


news_p_cleaner = news_p.strip('\n')
news_p_cleaner


# ## JPL Mars Space Images - Featured Image

# In[11]:


#Visit the url for the Featured Space Image site 
space_url = 'https://spaceimages-mars.com'
browser.visit(space_url)


# In[12]:


browser.links.find_by_partial_text('FULL IMAGE').click()


# In[13]:


soup = BeautifulSoup(browser.html, 'html.parser')
print(soup.prettify())


# In[14]:


img_url = soup.find("img", class_ = "headerimage fade-in")["src"]
img_url


# In[15]:


featured_image_url = f'{space_url}/{img_url}'
featured_image_url


# ## Mars Facts

# In[16]:


galaxy_url = 'https://galaxyfacts-mars.com'
browser.visit(galaxy_url)


# In[17]:


soup = BeautifulSoup(browser.html, 'html.parser')
print(soup.prettify())


# In[18]:


#mars facts
table = pd.read_html(galaxy_url, match="Equatorial Diameter")
table


# In[19]:


df = table[0]
df.columns=['Statistic', 'Mars Data']
df


# In[20]:


#mars to earth comparison
table2 = pd.read_html(galaxy_url, match="Mars - Earth Comparison")
table2


# In[21]:


df2 = table2[0]
df2.columns = ['Statistic', 'Mars Data', 'Earth']
df2


# In[22]:


#I wasn't sure if we needed all the data in tables, or just the first tabl
#to be safe, I loaded both in seperately and then concatonated with an
#inner join
df_all_data = pd.concat([df, df2], join="inner")
df_all_data


# In[29]:


mars_dict=df_all_data.to_dict("records")
print(mars_dict)


# ## Mars Hemispheres

# In[23]:


hemi_url = 'https://marshemispheres.com/'


# In[24]:


browser.visit(hemi_url)


# In[25]:


response = requests.get(hemi_url)
soup = BeautifulSoup(response.text, "html.parser")


# In[26]:


response = soup.find_all('div', class_='item')
print(response)


# In[27]:


hemisphere_image_urls = []

for x in response:

    title = x.h3.text
    browser.find_by_tag('h3').click()

    img_url = (browser.links.find_by_text("Sample"))["href"]
    hemisphere_image_urls.append({'title': title, 'img_url': img_url})
    browser.back()


# In[28]:


hemisphere_image_urls


# In[ ]:





# In[ ]:




