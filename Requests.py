from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib


def virgin_scrape():
    """
        Scrapes Job Information from Virgin Media
        Returns: a list of dictionaries containing job advert information
    """
    i = 1
    urls = []
    n = True
    while n:
        # The Pages holding the links to the job adverts increase by 1
        url = 'https://careers.virginmedia.com/apply/?location=United+Kingdom&listpage=' + str(i)
        # gets webpage information
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        if 'No Jobs Found' not in str(soup):
        # finds all the titles and splits from the text as required
            postings = soup.find('article', class_='vacancy').findAll('a')
            for s in postings:
                soap = s.get('href')
                st = soap.find('url') + 4
                e = soap.find('auth') - 1
                urls.append([s.text, urllib.parse.unquote(soap[st:e])])
        else:
            n = False
        i += 1
    out = []
    # iterates through the list of lists
    for u in urls:
        # gets and cleans the job description
        req = Request(u[1], headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        out.append({'Title': u[0], 'Company': 'Virgin Media', 'Desc': ' '.join([f.text for f in soup.findAll('p')])})

    return out
