'''Using the Article class defined in wiki.py, find Philosophy.'''

import sys
import wiki


class Philosophy:
    '''
    Object class for our game - finding Philosophy.
    I get it - this doesnt need to be its own object.
    I'm just practicing. Relax.'''

    # These constants are already in wiki.py
    # but we may as well duplicate them here
    WIKIRAND = 'https://en.wikipedia.org/wiki/Special:Random'
    WIKIBASE = 'https://en.wikipedia.org'
    pages = []

    _result = None

    def __init__(self, url=WIKIRAND, maxpages=40):
        self.maxpages = maxpages

        if url[0:6] == '/wiki/':
            self.url = self.WIKIBASE + url
        else:
            self.url = url

        self.article = wiki.Article(self.url)

        self._result = None
        self._result = self.result

    @property
    def result(self):
        '''Either return our result or find out what it is.'''
        if self._result is not None:
            return self._result

        # Another list
        urls = []
        success = False

        # First, record our starting position
        article = self.article

        urls.append(article.url)
        self.pages.append(article.title)

        print('Page 1: %s' % article.title)

        i = 1
        # Keep going as long as we aren't hitting the max
        while i < self.maxpages:
            i += 1
            # Get the article from the first body link
            # then, add it to our visited pages
            first_link = first_body_link(article.body)

            if first_link is None:
                print("Couldn't find any links - exiting")
                success = False
                break

            article = wiki.Article(first_link)

            if article.url in urls:
                print('Hit an infinite loop on "%s" - exiting' % article.title)
                break

            urls.append(article.url)
            self.pages.append(article.title)

            print('Page %s: %s' % (i, article.title))

            if article.title == 'Philosophy':
                success = True
                break

        success_fail_msg = 'Success' if success else 'Failure'
        message = '%s: %s after %s pages' % (self.article.title, success_fail_msg, i)
        print(message)
        return message


def first_body_link(body):
    '''
    1. Pass in a beautifulsoup object
    2. Find the first link that matches the criteria.
    The function assumes it's the .body property of the Article class.
    '''

    def is_body_link(tag):
        '''
        Check if a link meets the criteria for the Philosophy game.
        1. It's an <a> tag, obviously
        2. It has an href attribute
        3. It's a descendant of a <p> tag,
        meaning it's actually within some body text
        4. It's a link to another Wikipedia page
        (The first 6 chars of the href are '/wiki/')
        5. It's not in italics.
        6. It's NOT enclosed within parentheses. This function is the WORST.
        '''

        def is_in_parentheses(tag):
            '''
            Figure out if a tag is enclosed within parentheses.
            Since the parentheses themselves won't be within an <a> tag,
            we just check if the text surrounding the tag contains parentheses.
            '''
            # Our booleans to show if we've found a left and right parenthesis
            # on the left and right of our tag, respectively
            prev_paren = False
            next_paren = False

            # Our elements to iterate through.
            # Including non-elements,
            # i.e. text that is a sibling of our tag within a parent
            prev_elements = tag.previous_elements
            next_elements = tag.next_elements

            # We only want to read text within a paragraph.
            # Parentheses on wikipedia will not be *part* of a link,
            # only surrounding them
            # Note the [::-1] in the first loop -
            # We want our find() to iterate *backwards*
            # through the text to the left of our link, not forwards
            for element in prev_elements:
                if element.name is None and element.parent.name == 'p':
                    left_paren_pos = element[::-1].find("(")
                    right_paren_pos = element[::-1].find(")")

                    # If the find() method fails, it returns -1.
                    # Therefore, a match for either means that
                    # their sum will add up to at least -1 (-1 + 0)
                    if left_paren_pos + right_paren_pos >= -1:
                        if left_paren_pos > right_paren_pos:
                            prev_paren = True
                            del left_paren_pos, right_paren_pos
                            break
                        else:
                            # prev_paren = False
                            return False

            # Same as before, but looping forwards this time
            for element in next_elements:
                if element.name is None and element.parent.name == 'p':
                    left_paren_pos = element.find("(")
                    right_paren_pos = element.find(")")

                    if left_paren_pos + right_paren_pos >= -1:
                        if right_paren_pos > left_paren_pos:
                            next_paren = True
                            del left_paren_pos, right_paren_pos
                            break
                        else:
                            return False

            return prev_paren and next_paren

        # 1. Check if it's an <a> tag
        is_a = tag.name == 'a'

        # For each criteria, we should immediately return False if it's not met
        # Essentially, this function is a big AND() statement
        # and we want to short-circuit it
        if not is_a:
            return False

        # 2. Check if it has an href
        has_href = tag.has_attr('href')
        if not has_href:
            return False

        # 3. Descendant of a <p> tag
        in_p = tag.parent.name == 'p'
        if not in_p:
            return False

        # 4. Links to a wikipedia page
        in_wiki = tag['href'][0:6] == '/wiki/'
        if not in_wiki:
            return False

        # 5. Not in italics
        in_italics = tag.parent.name == 'i' or tag.i == 'i'
        if in_italics:
            return False

        in_paren = is_in_parentheses(tag)
        if in_paren:
            return False

        return True

    # Grab every <a> tag from the article content
    links = body.find_all('a')

    for link in links:
        if is_body_link(link):
            # As soon as we find a link that meets our criteria, get the URL
            return link['href']

    # If we weren't able to find one for whatever reason,
    # we should return None regardless.
    return None


def main(num=10):
    '''
    If the script is run on its own,
    just run the game 10 times for fun and exit.
    '''
    records = []

    i = 0

    while i < num:
        i += 1
        records.append(Philosophy().result)

    for record in records:
        print(record)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main()
