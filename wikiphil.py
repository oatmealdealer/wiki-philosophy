'''Start from either a random or a predetermined wikipedia article.
Find Philosophy by following the first link on each page
that is *not* in parentheses.
It needs work, but it does it most of the time.
'''
import requests
from bs4 import BeautifulSoup

WIKI = 'https://en.wikipedia.org/wiki/Main_Page'
WIKIRAND = 'https://en.wikipedia.org/wiki/Special:Random'
WIKITEST = ''
WIKIBASE = 'https://en.wikipedia.org'
PRINTURLS = False
PRINTTAGS = False
MAXPAGES = 40
MAXLINKS = 5


def get_page(url, printurl=False):
    '''Get a soup object from the page at a given url.'''
    request = requests.get(url)  # Get the page via requests

    if printurl:  # We may potentially want to print the url to console
        print('Getting page from %s' % url)

    soup = BeautifulSoup(request.text, 'lxml')  # Parse the text with BS4
    return soup  # Return the soup object


def wiki_title(soup):
    '''Find the title of the article.'''
    return soup.find('h1', class_='firstHeading').text


def wiki_body(soup):
    '''Isolate the actual content of the article.'''
    return soup.find('div', class_='mw-parser-output')


def is_body_link(tag):
    '''Check if a given tag is an article body link.

    It needs to be valid for the purpose of the game -
    meaning not in parentheses or italics.'''
    test_args = []

    is_a = tag.name == 'a'  # Make sure it's an <a> tag
    test_args.append(is_a)

    has_href = tag.has_attr('href')  # Make sure the HREF attr is present
    test_args.append(has_href)

    in_p = tag.parent.name == 'p'  # Make sure it's in a paragraph
    test_args.append(in_p)

    if has_href:  # Check for /wiki/ at the beginning of the URL
        in_wiki = tag['href'][0:6] == '/wiki/'
        test_args.append(in_wiki)

    in_par = not inParen(tag)
    test_args.append(in_par)

    in_i = not is_in_italics(tag)
    test_args.append(in_i)

    if PRINTTAGS:
        print(tag)
        # print(test_args)

    return all(test_args)


def is_header_link(tag):
    '''Check if tag is a header link.'''
    return tag.has_attr('href') and tag.name == 'link'


def get_page_url(soup):
    '''Get the URL of the page.'''
    return soup.find(is_header_link).text


def is_in_italics(tag):
    '''Check if a tag is enclosed by <i> tags, or if it is the parent of one'''
    return tag.parent.name == 'i' or tag.i == 'i'


def inParen(tag):
    '''This function is a huge pain.
    It checks if a tag is enclosed by parentheses.
    You wouldn't believe how annoying that is.
    '''

    if PRINTTAGS:
        print('Tag says: %s' % tag.text)
    p = False
    n = False

    pe = tag.previous_elements
    ne = tag.next_elements

    pi = 0
    ni = 0

    for e in pe:
        pi += 1
        if e.name == None and e.parent.name == 'p':
            lpos = e[::-1].find("(")
            rpos = e[::-1].find(")")
            if lpos > rpos:
                p = True
                # print('DINGO BABIES')
                # print(p)
            else:
                p = False
            if lpos != -1 or rpos != -1:
                # print('Previous lpos is %s and rpos is %s' % (lpos, rpos))
                if lpos > -1:
                    # print('Left parentheses found to the left at position %s of previous element #%i' % (lpos, pi))
                    pass
                if rpos > -1:
                    pass
                    # print('Right parentheses found to the left at position %s of previous element #%i' % (rpos, pi))
                # print("Parentheses found to the left! Somewhere!")
                # print('Found in the following element: %s' % e)
                # print('The parent type of which is: %s' % e.parent.name)
                break

    for e in ne:
        if e.name == None and e.parent.name == 'p':
            lpos = e.find("(")
            rpos = e.find(")")
            if lpos < rpos:
                n = True
                # print('DINGER WINGER')
                # print(n)
            else:
                n = False
            if lpos != -1 or rpos != -1:
                # print('Next lpos is %s and rpos is %s' % (lpos, rpos))
                if lpos > -1:
                    pass
                    # print('Left parentheses found to the right at position %s of next element #%i' % (lpos, ni))
                if rpos > -1:
                    pass
                    # print('Right parentheses found to the right at position %s of next element #%i' % (rpos, ni))
                # print("Parentheses found to the right! Somewhere!")
                # rint('Found in the following element: %s' % e)
                # print('The parent type of which is: %s' % e.parent.name)
                break



    #print(pe)
    #print(ne)
    # if PRINTTAGS == True:
    #     print('Previous element is %s' % pe)
    #     print('Next element is %s' % ne)

    if p == True and n == True:
        #print("DINGO BINGO!!!!!!")
        return True
    else:
        return False



def getLinks(soup):
    #links = soup.find_all('a')
    links = []
    #links = soup.find_all(is_body_link)
    i = 0
    #while i < MAXLINKS:
    #print(soup)
    n = 0
    for child in soup.descendants:
        n += 1
        if child.name != None:
            pass
        else:
            pass#(child)
    #print('This soup has %i descendants.' % n)
    for link in soup.find_all('a'):
        if i < MAXLINKS:
            #print(link)
            if is_body_link(link) == True:
                    links.append(link)
                    i += 1
                    #print(i)
        else:
            break



    return links

def isItalic(tag):
    #if tag.parent.name == 'i' or tag
    pass

def findPhilosophy():
    i = 0                 # Counter for while loop
    success = False        # Boolean of whether or not we've found Philosophy
    visitedpages = []    # To store all the urls we've visited, in case we hit an infinite loop of pages.

    if WIKITEST == '':                # Check our override variable - in case we want to start from a specific page
        page = get_page(WIKIRAND)    # If it's empty, get a random page. Otherwise, use the specified page
    else:
        page = get_page(WIKITEST)


    while i < MAXPAGES:  # Until we can check for infinite loops in the page history, let's just set a limit of pages to visit.
        title = wiki_title(page)  # Call our function to find the article title
        content = wiki_body(page)        # Call our function to get the body content
        links = getLinks(content)        # From that content, call the function to get our viable links
        #url = get_page_url(page)                # This function currently isn't working, but - it would be nice to have the URL of the page we're on


        print('Page title is: %s' % title)
        #print('Page content is: %s' % content)

        if title == 'Philosophy':
            success = True
            break
        else:
            pass

        if PRINTURLS == True:


            for link in links:
                if is_body_link(link):
                    isbody = 'is'
                else:
                    isbody = 'is not'

                print('Link title is "%s" and it %s a body link.\nLink URL is %s' % (link.text, isbody, link['href']))
                
                # if inParen(link) == True:
                #     print('Link is in parentheses')
                # else:
                #     print('Link is not in parentheses')
                #print(is_body_link(link))
        else:
            pass
        if len(links) > 0:
            firstLink = links[0]['href']
        else:
            print("Didn't get any links - exiting loop")
            break

        page = get_page(WIKIBASE + firstLink)

        if firstLink in visitedpages:
            print('Hit an infinite loop on page "%s" - exiting loop' % wiki_title(page))
            break

        visitedpages.append(firstLink)

        i += 1

    if success == False:
        print('Failed to find Philosophy after %i pages' % i)
    else:
        print('Found Philosophy in %i pages' % i)
    return [success, i]


def main():
    # Step 1: Pick a random wikipedia article.
    # Step 2: Check if article name is Philosophy. If so, end loop.
    # Step 3: Determine the first link in the article body that is *not* in parentheses OR ITALICS.
    # Step 4: Open that link.
    # Step 5: Goto step 2.
    # Also, detect if a page is visited that has been visited before.
    record = []
    i = 0
    while i < 10:
        record.append(findPhilosophy())
        i += 1



    print(record)

if __name__ == "__main__":
    main()