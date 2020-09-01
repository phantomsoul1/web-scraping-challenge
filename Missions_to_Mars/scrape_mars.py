from bs4 import BeautifulSoup
from config import chromedriver_path
from pprint import pprint
from splinter import Browser
import pandas as pd
import requests

def scrape():

    # Initialize result dictionary
    result = {}

    # Initialize the browser
    # (be sure to define the chrome driver path in the included config file)
    executable_path = {'executable_path': chromedriver_path}
    browser = Browser('chrome', **executable_path, headless=True)

    # NASA Mars News
    url = 'https://mars.nasa.gov/news'
    print(f'Searching {url}...')
    browser.visit(url)
    
    # Since the page has a redirect to trigger the react.js script, we need to revisit
    # the page with the parameters it redirects to
    url = browser.url
    browser.visit(url)

    # Now we can mine the results with BS4
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Work our way down the hierarchy to the specific elements of interest
    # (we don't want to accidentally pick up some other element elsewhere
    # with the same class)
    item_list = soup.find('ul', class_='item_list')
    slide = item_list.find('li', class_='slide')
    list_text = slide.find(class_='list_text')
    content_title = list_text.find(class_='content_title')
    article_teaser_body = list_text.find(class_='article_teaser_body')

    # Record the results
    result['news_title'] = content_title.text
    result['news_p'] = article_teaser_body.text

    print('Most recent news title found.')
    print('Most recent article teaser found.')

    # JPL Mars Space Images - Featured Image

    # Links are listed as relative links, so we have to segregate
    # out a base URL to append to the beginning of all links
    base_url = 'https://www.jpl.nasa.gov'
    print(f'Searching {base_url}...')

    # Visit the given page
    url = base_url + '/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Upon inspection, this result will work with BS4
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the main feature and anchor to its full image
    main_feature = soup.find('section', class_='main_feature')
    a = main_feature.find('a', id='full_image')

    # Compose the full image's URL and visit that page
    url = base_url + a['data-link']
    browser.visit(url)

    # Upon inspection, this result should contain the full image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the image of class 'main_image' and get its source address
    img = soup.find('img', class_='main_image')
    src = img['src']

    # Record the featured image URL by appending the source address to the base URL
    result['featured_image_url'] = base_url + src
    print('Featured image URL found.')

    # Mars Facts

    url = 'https://space-facts.com/mars/'
    print(f'Searching {url}...')
    
    # Since this is the only table on the page, fetching it via Pandas is easy
    table_dfs = pd.read_html(url)
    table_df = table_dfs[0]

    # Give the dataframe column names
    table_df.columns = ['Term', 'Description']

    # Record the result as an HTML table
    result['facts_table'] = table_df.to_html(header=False, index=False)
    print('Facts table found.')

    # Mars Hemispheres

    # Visit URL provided. Again, we have to segregate the base URL because
    # all links are provided as relative URLs.
    base_url = 'https://astrogeology.usgs.gov'
    print(f'Searching {base_url}...')
    url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Upon inspection, the result gives us tags we need
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the links to the 4 enhanced image pages
    product_section = soup.find(id='product-section')
    items = product_section.find_all(class_='item')
    print(f'{len(items)} items found.')

    # create a list for the hemispheres and iterate through them
    hemisphere_image_urls = []
    for item in items:

        # Compose the link
        a = item.find('a', class_='itemLink product-item')
        link = a['href']
        url = base_url + link
        print(f'Searching {url}...')
            
        # Visit the link    
        browser.visit(url)
        soup = BeautifulSoup(browser.html, 'html.parser')
        
        # Upon inspection, the result has the tags we need
        # Find the link to the full-size image
        wide_image = soup.find(id='wide-image')
        img = wide_image.find('img', class_='wide-image')
        img_src = img['src']
        print('Source image found.')
        
        # Find the title; strip the word 'Enhanced' from the end of it
        title = soup.find('h2', class_='title').text
        title = title.replace(' Enhanced', '')
        print('Title found.')
        
        # Add the result as a dictionary to the list of hemispheres
        hemisphere_image_urls.append({
            'title': title,
            'img_url': base_url + img_src
        })

    # Add the list of hemispheres
    result['hemisphere_image_urls'] = hemisphere_image_urls
    print('Hemisphere image links found.')

    # Return the results
    return result

if __name__ == '__main__':
    pprint(scrape())