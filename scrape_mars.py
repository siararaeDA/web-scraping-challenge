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
def scrapeMarsNews():
    browser = initBrowser()

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

    marsNews = {'Title': newsTitle, 'Text': newsText}

    browser.quit()
    
    return marsNews

##############################################
# Function to scrape Mars Space Images
##############################################
def scrapeSpaceImages():
    browser = initBrowser()

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    relative_image_path = soup.find('a', {'class':'fancybox'})["data-fancybox-href"]
    images_url = 'https://www.jpl.nasa.gov'
    featured_img = images_url + relative_image_path

    browser.quit()

    return featured_img

##############################################
# Function to scrape Mars Facts
##############################################
def scrapeMarsFacts():
    browser = initBrowser()

    url = "https://space-facts.com/mars/"
    browser.visit(url)

    time.sleep(1)

    table = pd.read_html(url)
    #print(table)

    marsFacts_df = table[0]
    marsFacts_df.columns = ['Description', 'Value']
    htmlString = marsFacts_df.to_html()

    browser.quit()

    return htmlString

##############################################
# Function to scrape Mars Hemispheres
##############################################
def scrapeMarsHemispheres():
    browser = initBrowser()

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

    browser.quit()
    
    return images

##############################################
#      Main
##############################################
def scrape():
    # Dictionary of Title, Text 
    newsFromMars = scrapeMarsNews()
    # Image URL
    spaceImage = scrapeSpaceImages()
    # HTML String of table
    marsFacts = scrapeMarsFacts()
    # List of dictionaries of Title, Image URL
    hemispheres = scrapeMarsHemispheres()

    # Store all of the data in one dictionary
    marsInfoDict = {
        'newsTitle': newsFromMars['Title'],
        'newsText': newsFromMars['Text'],
        'featuredImgURL': spaceImage,
        'htmlFactsTable': marsFacts,
        'hemisphereImages': hemispheres
    }

    return marsInfoDict

