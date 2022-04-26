
## -- Dependencies --

# splinter and beautiful soup 

from splinter import Browser

from bs4 import BeautifulSoup as soup

from webdriver_manager.chrome import ChromeDriverManager

# pandas for table scraping

import pandas as pd

# date time for recurring scrape
import datetime as dt 

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=True)


def scrape_all():
    browser = init_browser()

# ----- News -----

    #assign url 

    news_url = 'https://redplanetscience.com'
    browser.visit(news_url)

    # delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #html parser
    html = browser.html
    news_soup = soup(html, "html.parser")

    #try/except for err handle

    try: 
        slide_elem = news_soup.select_one("div.list_text")

        #parent telement to find first 'a' anchor tag and save as newstitle
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # parent element to find para text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None 
    

# ----- Featured Images -----

    # Visit URL
    spaceimg_url = 'https://spaceimages-mars.com'
    browser.visit(spaceimg_url)


    # find and click the full image button
        #use 1 to find second button tag - there are 3 on the page
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse image w soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #relative image url
    try:
        #relative img url 
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None 

    #add base to relative url 
    img_url = f"https://spaceimages-mars.com/{img_url_rel}"


# ----- Facts -----

#scrape table with pandas 
    #index 0 is first table it encounters on page 
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    #formatting for columns, index
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    #df to html, bootstrap
    mars_facts = df.to_html(classes="talbe table-striped")

# ----- Hemispheres -----    
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = "https://astrogeology.usgs.gov/"

    browser.visit(url)

    hemisphere_html = browser.html

    hemisphere_soup = soup(hemisphere_html, "html.parser")

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    all_mars_hemispheres = hemisphere_soup.find("div", class_="collapsible results")
    sub_hemispheres = all_mars_hemispheres.find_all("div", class_ = "item")

    #iterate thru each sub hemisphere div 
    for i in sub_hemispheres:

        #title
        hemisphere = i.find("div", class_ = "description")
        title = hemisphere.h3.text

        #image link from img page 
        hemisphere_img_page = hemisphere.a["href"]
        browser.visit(base_url + hemisphere_img_page)

        img_html = browser.html
        img_soup = soup(img_html, "html.parser")

        img_link = img_soup.find("div", class_= "downloads")
        img_url = img_link.find("li").a["href"]

        #dict
        img_dict = {}
        img_dict["title"] = title
        img_dict["img_url"] = img_url

        hemisphere_image_urls.append(img_dict)

    #store in dict
    data = {
      "news_title": news_title,
      "news_paragraph": news_p,
      "featured_image": img_url,
      "facts": mars_facts,
      "last_modified": dt.datetime.now(),
      "hemisphere_images": hemisphere_image_urls
    }

    return data

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


