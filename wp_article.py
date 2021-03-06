
import re
import urllib
from urllib import request
from bs4 import BeautifulSoup
from iso639 import languages

# Wikipedia.org uses some non-standard language codes in its subdomain URLs
# Source: https://en.wikipedia.org/wiki/List_of_Wikipedias
# The following dictionary maps these quirks to language names.
# Some of these originate from ISO 639 but are deprecated (eg. 'sh')
wikipedia_quirks = {
    'sq' : 'Albanian',
    'als' : 'Alemannic',
    'roa-rup' : 'Aromanian',
    'map-bms' : 'Banyumasan',
    'nds-nl' : 'Dutch Low Saxon',
    'bh' : 'Bihari',
    'zh-yue' : 'Cantonese',
    'zh-classical' : 'Classical Chinese',
    'ms' : 'Malay',
    'zh-min-nan' : 'Southern Min / Min Nan',
    'no' : 'Norwegian (Bokmål)',
    'ksh' : 'Ripuarian',
    'bat-smg' : 'Samogitian',
    'simple' : 'Simple English',
    'roa-tara' : 'Tarantino',
    'fiu-vro' : 'Võro',
    'cbk-zam' : 'Zamboanga Chavacano',
    'arz' : 'Arabic (Egyptian)',
    'mrj' : 'Western Mari',
    'sh' : 'Serbo-Croatian',
    'nah' : 'Nāhuatl',
    'be-tarask' : 'Belarusian (Taraškievica)'
    }


class wp_article:

    
    def __init__(self, wp_article_url):
        self.url = ''
        self.info_url = ''
        self.title = ''
        self.wp_prefix = ''
        self.lang_name_en = ''
        self.resolved_length = 0
        wp_url_pieces = re.match('(.*//(\S+)\.wikipedia.org).*/(.*$)', wp_article_url )
        # pieces[0] is all of URL
        self.url = wp_article_url
        # pieces[1] is a prefix like 'https://en.wikipedia.org'
        self.wp_prefix = wp_url_pieces[1]
        # pieces[2] is the language code, eg. 'en', 'sv'
        # Unfortunately, Wikipedia uses several nonstandard language codes.
        # TODO: Is it OK to assume that at most one of the following
        # try statements finds a match?
        wp_language_code = wp_url_pieces[2]
        try:
            self.lang_name_en = wikipedia_quirks[wp_language_code]
        except KeyError:
            pass
        try:
            self.lang_name_en = languages.get(part1 = wp_language_code).name
        except KeyError:
            pass
        try:
            self.lang_name_en = languages.get(part3 = wp_language_code).name
        except KeyError:
            pass
        if not self.lang_name_en:
            print('Warning: could not resolve English name for language code \'' + wp_language_code + '\'')
        # pieces[3] is the name of the article (percentage encoded)
        self.title = urllib.parse.unquote(wp_url_pieces[3])   #.decode('utf8')        
        self.info_url = self.wp_prefix + '/w/index.php?title=' + urllib.parse.quote(self.title) + '&action=info'


    # figure out the length of an article by parsing its info page
    def resolve_length(self):
        html = request.urlopen(self.info_url).read().decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        length_string = soup.find('tr', {'id' : 'mw-pageinfo-length'}).find_all('td')[1].text
        length_string = re.sub("[^0-9]", '', length_string)
        try:
            length = int(length_string)
        except ValueError:
            # Some info pages fail to declare article length; deal with it here
            length = 0
        self.resolved_length = length
        return self.resolved_length


    # extract URLs that point to the same article in other languages
    def resolve_interlang_links(self):
        html = request.urlopen(self.url).read().decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        il_links = soup.find_all('a', {'class' : 'interlanguage-link-target'})
        links_out = list()
        for l in il_links:
            #print("Resolving \'" + l['title'] + '\' at ' + l['href'] ) 
            links_out.append(wp_article(l['href']))
        return links_out


    def __str__(self):
        return self.title + "\t\n"


# an example use case
def main():

    # create an initial article object
    #url = "https://en.wikipedia.org/wiki/Tornio"
    url = "https://simple.wikipedia.org/wiki/Alabama"
    my_article = wp_article(url)

    # create an empty list to hold Wikipedia article objects
    my_article_list = list()

    # append our initial article object to the empty list
    my_article_list.append(my_article)

    # create an additional article object for every other language that
    # the initial article is available in; append also these to list
    my_article_list += my_article.resolve_interlang_links()

    # go through all article objects and query the length of each
    # corresponding article from Wikipedia
    for a in my_article_list:
        print('Article ' + a.title + ' in ' + a.lang_name_en + ' has length ' + str(a.resolve_length()))


# execute main() only if this is being run as a script
if __name__ == "__main__":
    main()


