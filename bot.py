
import requests
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse

proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
}

def getHTML(onion):
        onions = []
        print('Attempting to get .onion links from ' + str(onion) + '...')

        try:
                html=requests.get(onion, proxies=proxies, timeout=10).text

                # Looks for all 'href' attributes in html object.
                for link in BeautifulSoup(html, parse_only=SoupStrainer('a'), features='html.parser'):
                        if link.has_attr('href'):
                                # Check if there's any .onion links.
                                if link['href'].find('.onion')>=0:
                                        # If there's a .onion link, parse for domain.
                                        link['href'] = 'http://' + urlparse(str(link['href'])).netloc

                                        # Append this .onion link to the 'onions' array.
                                        onions.append(link['href'])

                                else
                                        continue

                #If there's no "<a href='xxxx.onion'>" then getHTML() will return an empty onions array.
        except:
                pass

        return onions

def alive(onion):
        try:
                print('Pinging ' + onion)
                html = requests.get(onion, proxies=proxies, timeout=10).text

                if html:
                        print('This site is alive.')
                        return 1 # Means site is alive.

        except:
                return 0 # Means site is dead.

# http://wiki5kauuihowqi5.onion/

def init():
        onion = open('fresh_onions.txt','r')
        fresh_onions = onion.readlines()
        onion.close()

        if len(fresh_onions) == 0:
                print('Reached EOF...')
                return

        open('fresh_onions.txt','w').close()

        for link in fresh_onions:
                # Check if site has been scraped already.
                with open('scraped.txt') as s:
                        if link.strip() in s.read():
                                print(link.strip() + ' has already been scraped. Skipping.')
                                continue

                onions = getHTML(link.strip())

                if onions:
                        print('Finished scraping. Adding to scraped.txt')
                        so = open('scraped.txt','a')
                        so.write(link.strip())
                        so.close()

                        # Now it will check all the new links it found to see if they're alive. Alive links will be added to fresh_onions.txt
                        for onion in onions:
                                freshOnion = alive(onion)

                                if freshOnion == 1:
                                        # It should make sure it has not recorded this site already.
                                        with open('onion_garden.txt') as os:
                                                if onion in os.read():
                                                        print('Site has already been recorded.')
                                                        continue

                                        # Add to fresh_onions.txt
                                        print('Adding to fresh_onions.txt')
                                        fo = open('fresh_onions.txt','a')
                                        fo.write(onion + '\n')
                                        fo.close()

                                        print('Adding to onion_garden.txt')
                                        og = open('onion_garden.txt','a')
                                        og.write(onion + '\n')
                                        og.close()
                                else:
                                        print('This site is dead.')
                else:
                        print('This site does not contain any links.')

        init()
init()










