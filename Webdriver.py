import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def three_scrape():
    """
           Scrapes Job Information from Three
           Returns: a list of dictionaries containing job advert information
       """
    urls = []
    # Initiates the web driver
    driver = webdriver.Chrome(r"chromedriver.exe")
    # Goes to the first webpage
    driver.get(
        'https://jobs.three.co.uk/search-jobs/United '
        'Kingdom/5965/4/2635167-6269131-2649889-7290691-2654782/51x62127/0x30556/50/2')
    time.sleep(5)
    # Clicks the cookie button
    driver.find_element_by_id('gdpr-button').click()
    k = True
    while k:
        time.sleep(5)
        # iterates through the elements in the page which have class name job-tile and getting the hrefs
        for d in driver.find_elements_by_class_name("job-tile"):
            b = BeautifulSoup(d.get_attribute('innerHTML'), 'html.parser').find('a')
            urls.append('https://jobs.three.co.uk/' + b.get('href'))
        # select body of page and page_down
        body = driver.find_element_by_css_selector('body')
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        # Click Next element if exists
        if "next disabled" not in driver.find_element_by_id('content').get_attribute('innerHTML'):
            driver.find_element_by_class_name("next").click()
        else:
            k = False
    driver.close()

    out = []
    session = HTMLSession()
    # iterates through the href list
    for u in urls:
        # gets and cleans the job description and title
        page = requests.get(u)
        other_pages = BeautifulSoup(page.content, 'html.parser')
        title = other_pages.find('title').text
        s = session.get(u).html.text
        out.append({'Title': title, 'Company': 'Three', 'Desc': s[:s.find('====')]})

        return out
