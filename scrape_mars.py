from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests

def init_browser():
    executable_path = {'executable_path': 'C:/Users/jdelga01/Desktop/Mission_to_Mars/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

mars_data={}

def scrape():
    browser=init_browser()
    url='https://mars.nasa.gov/news/'
    browser.is_element_not_present_by_css('div.content_title', wait_time=None)
    browser.visit(url)
    html_last = browser.html
    soup=bs(html_last,'html.parser')
    articles_titles=soup.find_all('div', class_='content_title')
    for a in articles_titles:
        title=a.find('a').text
    teaser=soup.find('div', class_='article_teaser_body').text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    response=requests.get(url)
    soup=bs(response.text,'html.parser')
    featured_image=str(soup.find('div',class_='carousel_items'))
    ft_url1=featured_image.split('url(\'/')[1]
    ft_url2=ft_url1.split(');">\n<div class')[0][:-1]
    pre_ft_url='https://www.jpl.nasa.gov/'
    ft_url=pre_ft_url+ft_url2

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    response=requests.get(url)
    soup=bs(response.text,'html.parser')
    last_tweet=soup.find_all('div', class_='js-tweet-text-container')
    weather_tweets=[]
    for l in last_tweet:
        if "InSight sol" in l.text:
            weather_tweets.append(l.text.replace('\n',' '))
    mars_weather=weather_tweets[0]

    import pandas as pd
    url='https://space-facts.com/mars/'
    tables = pd.read_html(url)
    fact_table=tables[1]
    fact_table.columns=['Description','Value']
    fact_table=fact_table.set_index('Description')
    html_table=fact_table.to_html()

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]

    mars_data["news_title"]=title
    mars_data["news_p"]=teaser
    mars_data["featured_image_url"]=ft_url
    mars_data["mars_weather"]=mars_weather
    mars_data["mars_facts"]=html_table
    mars_data["hemisphere_image_urls"]=hemisphere_image_urls

    browser.quit()

    return mars_data