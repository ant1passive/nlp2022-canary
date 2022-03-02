
from se_boolean import searchEngineBoolean
from se_tfidf import searchEngineTFIDF
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from wp_article import wp_article
from operator import itemgetter
import numpy

numpy.set_printoptions(threshold = numpy.inf) #For testing purposes, allows long matrices to be printed in full.
app = Flask(__name__)

def queryPrompt(searchEngine):
    while True:
        try:
            user_query = str(input("Type the query (empty quits): "))
            if user_query != '':
                searchEngine.test_query(user_query)
            else:
                break
        except (TypeError):
            print('Invalid input')
        except (KeyError):
            print('Keyerror')
        except (SyntaxError):
            print('Syntax Error')


def main():

    done = False
    
    # Queries are possible right after this constructor call:
    # there is sample data hard-coded in the class definition.
    # foo = searchEngineBoolean()

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
    length = list()
    titles = list()
    for a in my_article_list:
        titles.append(a.title)
        lenght.append(a.resolve_length())

    # initialize the search engine (currently the web ui only uses tfidf

    #foo = searchEngineTFIDF()
    #foo.index_documents(articles, titles)

    #foo.test_query("in")
    #print(titles)
    #print(text)

@app.route('/search')
def search():

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

    # Get query from URL variable
    query = request.args.get('query')

    matches = []

    if query:
        # go through all article objects and query the length of each
        # corresponding article from Wikipedia
        for a in my_article_list:
            matches.append([a.lang_name_en, a.title, a.resolve_length()])
        matches = sorted(matches, key=itemgetter(2), reverse=True)

    return render_template('searchpage.html', matches=matches)


