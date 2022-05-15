from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import pandas as pd

def scrape_info():

    # News
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find('div', class_="slide")
    
    news_title = results.find('div', class_="content_title").text.strip('\n')
    news_p = soup.find('div', class_="rollover_description_inner").text.strip('\n')

    # JPL Mars Space Images - Featured Image    

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Visit the url for the Featured Space Image site 
    space_url = 'https://spaceimages-mars.com'
    browser.visit(space_url)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    soup = BeautifulSoup(browser.html, 'html.parser')

    img_url = soup.find("img", class_ = "headerimage fade-in")["src"]
    featured_image_url = f'{space_url}/{img_url}'

    # ## Mars Facts
    galaxy_url = 'https://galaxyfacts-mars.com'
    table = pd.read_html(galaxy_url, match="Equatorial Diameter")

    df = table[0]
    df.columns=['Statistic', 'Data']
    mars_dict=df.to_dict("records")

    # ## Mars Hemispheres
    hemi_url = 'https://marshemispheres.com/'

    browser.visit(hemi_url)
    
    response = requests.get(hemi_url)
    soup = BeautifulSoup(response.text, "html.parser")

    response = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for x in response:

        title = x.h3.text
        browser.find_by_tag('h3').click()

        img_url = (browser.links.find_by_text("Sample"))["href"]
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        browser.back()

    #dict
    mars_data = {
        "news_title": news_title,
        "news_p": news_p, 
        "featured_image_url": featured_image_url,
        "hemisphere_image_urls": hemisphere_image_urls, 
        "mars_facts": mars_dict
    
    }

    browser.quit()

    # Return results
    return mars_data