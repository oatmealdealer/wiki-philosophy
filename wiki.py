'''Object class for Wikipedia articles and their associated links.
Includes functions for getting various information out of articles.
'''

import requests
from bs4 import BeautifulSoup

class Article:
    '''
    Object class for a Wikipedia article.
    If no URL is supplied, pick a page at random.
    '''
    WIKIRAND = 'https://en.wikipedia.org/wiki/Special:Random'
    WIKIBASE = 'https://en.wikipedia.org'

    def __init__(self, url=WIKIRAND):
        # To make this easier, we'll check if the URL passed in is a body link.
        # If it is, we can fix it by prepending the base URL.
        if url[0:6] == '/wiki/':
            self.url = self.WIKIBASE + url
        else:
            self.url = url

        # For the time being, we will manually invoke the getter on all our properties
        # by setting them to None and then trying to access them.
        # This isn't really necessary, though.
        # We could just set them all to None and let nature run its course.
        self._page = None
        self._page = self.page

        self._title = None
        self._title = self.title

        self._body = None
        self._body = self.body


    @property
    def page(self):
        '''
        Return the BeautifulSoup object for the page if defined.
        If not defined, request the page and instantiate the soup object.
        '''
        if not self._page is None:
            return self._page

        request = requests.get(self.url)

        soup = BeautifulSoup(request.text, 'lxml')
        self._page = soup
        return self._page


    @property
    def title(self):
        '''
        Return the title of the page if defined.
        If not defined, find the title in the page.
        '''
        if not self._title is None:
            return self._title

        self._title = self.page.find('h1', class_='firstHeading').text
        return self._title


    @property
    def body(self):
        '''
        Return the portion of the BeautifulSoup object that constitutes the article's body.
        If not defined, find it within the page.
        '''
        if not self._body is None:
            return self._body

        self._body = self.page.find('div', class_='mw-parser-output')
        return self._body


if __name__ == '__main__':
    article = Article()
    print(article.url)
    print(article.title)
