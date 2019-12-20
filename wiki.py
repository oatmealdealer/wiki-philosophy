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

        self._page = None

        self._title = None

        self._body = None

    @property
    def page(self):
        '''
        Return the BeautifulSoup object for the page if defined.
        If not defined, request the page and instantiate the soup object.
        '''
        if self._page is not None:
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
        if self._title is not None:
            return self._title

        self._title = self.page.find('h1', class_='firstHeading').text
        return self._title

    @property
    def body(self):
        '''
        Extract the article body from the BS object.
        If not defined, find it within the page.
        '''
        if self._body is not None:
            return self._body

        self._body = self.page.find('div', class_='mw-parser-output')
        return self._body


if __name__ == '__main__':
    article = Article()
    print(article.url)
    print(article.title)
