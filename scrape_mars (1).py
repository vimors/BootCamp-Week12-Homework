from splinter import Browser
from bs4 import BeautifulSoup
from splinter.exceptions import ElementDoesNotExist
import requests
import pandas as pd
import pymongo


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"} # Mac
    executable_path = {"executable_path": "chromedriver.exe"} # Windows
    return Browser("chrome", **executable_path, headless=False)


def scrape():
  

    
    listings = {}
    browser = init_browser()

    featured_image_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(featured_image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news = soup.find('div', class_='list_text')

    new_title = news.find('a').text
    new_paragraph = news.find('div', class_='article_teaser_body').text

    listings["Title"] = new_title
    listings["Paragraph"] = new_paragraph
    

    featured_image_url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find("img", class_="thumb")['src']
    img_url = "https://jpl.nasa.gov"+image
    
    listings["img_mars"] = img_url  

    featured_image_url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(featured_image_url3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather_tweets = soup.find_all("li", class_="js-stream-item stream-item stream-item ")

    for tweet in mars_weather_tweets:
        tweet_creator = tweet.find("span", class_="username u-dir u-textTruncate").text
        if (tweet_creator == "@MarsWxReport"):
            mars_weather = tweet.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
            break
    
    
    listings["weather"] = mars_weather
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df_table = tables[0]
    dict_table = df_table.to_dict('list')
    dict_table = {str(key): value for key, value in  dict_table.items()}
    listings["tabla"] = dict_table

    hemisphere_image_urls = []

    hemisphere_image_urls = []
    dict_hemisphere = {}
    url_fixed = 'https://astrogeology.usgs.gov'
    featured_image_url3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(featured_image_url3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('a', class_='itemLink product-item')
    for image in images:
        if(image.text != ''):
            browser.visit(url_fixed + image['href'])            
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')        
            tmp = soup.find('div', class_='downloads').find('a')['href']        
            dict_hemisphere = {'Title': image.text,
                    'Image_url' : tmp}
            hemisphere_image_urls.append(dict_hemisphere)                        
            
            browser.back()
    listings["Hemisferios"] = hemisphere_image_urls
    #collection.insert(listings)
    return listings
