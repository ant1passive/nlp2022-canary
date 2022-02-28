
import nltk, re, pprint
from nltk import word_tokenize
import urllib
from urllib import request
from bs4 import BeautifulSoup


class wp_article:

    
    def __init__(self, wp_article_url):
        self.url = ''
        self.info_url = ''
        self.title = ''
        self.wp_prefix = ''
        self.lang_name_en = ''
        self.resolved_length = 0
        wp_url_pieces = re.match('(.*\.org).*/(.*$)', wp_article_url )
        self.url = wp_article_url
        self.wp_prefix = wp_url_pieces[1]
        self.title = urllib.parse.unquote(wp_url_pieces[2])   #.decode('utf8')        
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
            #print("Resolved \'" + l['title'] + '\' at ' + l['href'] ) 
            print("Resolved \'" + l['title'] + '\'')
            links_out.append(wp_article(l['href']))
        return links_out


    def __str__(self):
        return self.title + "\t\n"


def main():

    # create an initial article object
    url = "https://en.wikipedia.org/wiki/Tornio"
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
        print('Article ' + a.title + ' has length ' + str(a.resolve_length()))


main()


