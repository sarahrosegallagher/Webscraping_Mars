
## -- Dependencies --

# splinter and beautiful soup 

from splinter import Browser

from bs4 import BeautifulSoup as soup

from webdriver_manager.chrome import ChromeDriverManager

# pandas for table scraping

import pandas as pd

# date time for recurring scrape
import datetime as dt 



#set up path 
def scrape_all():
    executable_path = {"executable_path": ChromeDriverManager().install()}

    browser = Browser("chrome", **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)

    #store in dict
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now()
    }

    #quit broswer 
    browser.quit()
    
    return data 



# ----- News -----

#refactor fxn 
def mars_news(browser): 

    #assign url 

    url = 'https://redplanetscience.com'
    browser.visit(url)

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
    
    return news_title, news_p 


# ----- Featured Images -----

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


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

    return img_url


# ----- Facts -----

def mars_facts():
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
    return df.to_html(classes="talbe table-striped")

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




