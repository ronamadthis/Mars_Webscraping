# Dependencies

from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
	browser = init_browser()
	marsDict = {}


# NASA News Scrape
	nasa_url = "https://mars.nasa.gov/news/"
	browser.visit(nasa_url)
	time.sleep(1)

	html = browser.html
	soup = BeautifulSoup(html, "html.parser")

	nasa_newstitle = soup.find('div', class_='content_title').text
	nasa_newstext = soup.find('div', class_='article_teaser_body').text
	

	marsDict['news_title'] = nasa_newstitle 

	marsDict['news_text'] = nasa_newstext

# NASA Featured Image
	jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(jpl_url)

	browser.click_link_by_partial_text('FULL IMAGE')
	time.sleep(2)

	browser.click_link_by_partial_text('more info')
	time.sleep(2)

	jpl_html = browser.html
	jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

	img_partial = jpl_soup.find('figure', class_='lede').find('img')['src']
	image_path = f'https://www.jpl.nasa.gov{img_partial}'

	marsDict['featured_image_url'] = image_path
	

# Mars Weather Report
	mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(mars_weather_url)
	time.sleep(1)
	mars_weather_html = browser.html
	mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

	mars_weather = mars_weather_soup.find('p', class_="tweet-text").text

	marsDict['Weather'] = mars_weather	
	

# Mars Facts
	mars_facts_url = 'https://space-facts.com/mars/'
	browser.visit(mars_facts_url)
	time.sleep(1)
	mars_facts_html = browser.html
	mars_facts_soup = BeautifulSoup(mars_facts_html, 'html.parser')

	fact_table = mars_facts_soup.find('table', id='tablepress-mars')
	column1 = fact_table.find_all('td', class_='column-1')
	column2 = fact_table.find_all('td', class_='column-2')

	properties = []
	values = []

	for row in column1:
	    property = row.text.strip()
	    properties.append(property)
	    
	for row in column2:
	    value = row.text.strip()
	    values.append(value)
	    
	mars_facts = pd.DataFrame({
	    "Property":properties,
	    "Value":values
	    })

	mars_facts_html = mars_facts.to_html(index=False)
	mars_facts

	marsDict['mars_facts'] = mars_facts_html

# Mars Hemispheres
	usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(usgs_url)
	hemispheres_html = browser.html
	soup = BeautifulSoup(hemispheres_html, 'html.parser')
	items = soup.find_all('div', class_='item')
	base_url = "https://astrogeology.usgs.gov"
	url_list = []
	for item in items:
	    url = item.find("a", class_='itemLink')['href']   
	    url_list.append(base_url + url)
	    
	hemi_dicts = []
	for page in url_list:
	    hemi_dict = {}
	    browser.visit(page)
	    hemispheres_html = browser.html
	    soup = BeautifulSoup(hemispheres_html, 'html.parser')
	    title = soup.find('h2', class_='title').text.strip("Enhanced")
	    image = soup.find('img', class_='wide-image')["src"]
	    
	    hemi_dict['title'] = title.strip()
	    hemi_dict['img_url'] = base_url + image
	    hemi_dicts.append(hemi_dict)

	marsDict['hemi_dicts'] = hemi_dicts
	
	return (marsDict)

	

