from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests

##############################################
# Initialize Browser
##############################################
def initBrowser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

##############################################
# Function to scrape Mars News
##############################################
def scrapeMarsNews(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    newsTitleList = soup.find_all('div', {'class': 'content_title'})
    newsTextList = soup.find_all('div', {'class': 'article_teaser_body'})

    # Indexed at one because the first item in the list isn't the correct title.
    newsTitle = newsTitleList[1].text
    newsText = newsTextList[0].text

    marsNews = {'Title': newTitle, 'Text': newText}

    print(newsTitle)
    print('--------------------------')
    print(newsText)

    return marsNews

##############################################
# Function to scrape Mars Space Images
##############################################
def scrapeSpaceImages(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    relative_image_path = soup.find('a', {'class':'fancybox'})["data-fancybox-href"]
    images_url = 'https://www.jpl.nasa.gov'
    featured_img = images_url + relative_image_path
    print(featured_img)

    return featured_img

##############################################
# Function to scrape Mars Facts
##############################################
def scrapeMarsFacts(browser):
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    time.sleep(1)

    table = pd.read_html(url)
    #print(table)

    marsFacts_df = table[0]
    marsFacts_df.columns = ['Description', 'Value']
    htmlString = marsFacts_df.to_html()

    return htmlString

##############################################
# Function to scrape Mars Hemispheres
##############################################
def scrapeMarsHemispheres(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    imageDivs = soup.find_all('div', {'class': 'description'})

    images = []

    baseURL = 'https://astrogeology.usgs.gov'

    for div in imageDivs:
        title = div.find('h3').text
    
        imagePath = div.find('a')['href']
        imageURL = baseURL + imagePath
    
        browser.visit(imageURL)
        imageHTML = browser.html
        imageSoup = bs(imageHTML, "html.parser")
    
        imageLink = baseURL + imageSoup.find('img', {'class': 'wide-image'})['src']
    
        images.append({'title': title, 'img_url': imageLink})
    
    return images

##############################################
#      Main
##############################################

browser = initBrowser()

# Dictionary of Title, Text 
newFromMars = scrapeMarsNews(browser)
# Image URL
spaceImage = scrapeSpaceImages(browser)
# HTML String of table
marsFacts = scrapeMarsFacts(browser)
# List of dictionaries of Title, Image URL
hemispheres = scrapeMarsHemispheres(browser)
