from visualiser_functions import cat_plot_tuple
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

    # 5. opens text file and splits text to articles
    path = r"write path here"
    #path = r"./input-texts/enwiki-20181001-corpus.100-articles.txt"

    markup = ''
    with open(path, encoding="utf8") as f:
        markup = f.read()

    # add a fake top-level tag to markup to ensure that parse tree has a root
    markup = "<top>\n" + markup + "\n</top>\n"
    # parse XML to find paragraph tags
    soup = BeautifulSoup(markup, 'xml')
    articleTags = soup.find_all('article')

    # accumulate body texts and titles
    articles = list()
    titles = list()
    for a in articleTags:
        articles.append(a.text.strip())
        titles.append(a['name'])

    # initialize the search engine (currently the web ui only uses tfidf

    #foo = searchEngineTFIDF()
    #foo.index_documents(articles, titles)

    #foo.test_query("in")
    #print(titles)
    #print(text)

@app.route('/search')
def search():
    
    #path = r"write path here"
    path = r"./input-texts/enwiki-20181001-corpus.100-articles.txt"

    markup = ''
    with open(path, encoding="utf8") as f:
        markup = f.read()

    # add a fake top-level tag to markup to ensure that parse tree has a root
    markup = "<top>\n" + markup + "\n</top>\n"
    # parse XML to find paragraph tags
    soup = BeautifulSoup(markup, 'xml')
    articleTags = soup.find_all('article')

    # accumulate body texts and titles
    articles = list()
    titles = list()
    for a in articleTags:
        articles.append(a.text.strip())
        titles.append(a['name'])

    # initialize the search engines

    se_bool = searchEngineBoolean()
    se_bool.index_documents(articles, titles)

    se_tfidf = searchEngineTFIDF()
    se_tfidf.index_documents(articles, titles)

    query = request.args.get('query')
    bool_matches = []
    tfidf_matches = []

    radio = request.args.get('analyse')
    if radio:
        if ' ' in radio:
            radio = radio.replace(' ', '_')
            
        url = "https://en.wikipedia.org/wiki/" + radio

        
        #url = "https://en.wikipedia.org/wiki/" + user_input

        my_article = wp_article(url)

        # create an empty list to hold Wikipedia article objects
        my_article_list = list()

        # append our initial article object to the empty list
        my_article_list.append(my_article)

        # create an additional article object for every other language that
        # the initial article is available in; append also these to list
        my_article_list += my_article.resolve_interlang_links()

        # Get query from URL variable
        query = True

        matches = []
        to_plot = []        

        # go through all article objects and query the length of each
        # corresponding article from Wikipedia
        for a in my_article_list:
            matches.append([a.lang_name_en, a.title, a.resolve_length()])
            to_plot.append((a.lang_name_en, a.resolved_length))
        matches = sorted(matches, key=itemgetter(2), reverse=True)
        cat_plot_tuple(to_plot)

    
    elif query:
        tfidf_matches = se_tfidf.test_query(query)
        bool_matches = se_bool.test_query(query)

    return render_template('search-results.html', bool_matches = bool_matches, tfidf_matches=tfidf_matches)


