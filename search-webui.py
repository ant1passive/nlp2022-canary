
from se_boolean import searchEngineBoolean
from se_tfidf import searchEngineTFIDF
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
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

    # initialize the search engine (currently the web ui only uses tfidf

    foo = searchEngineTFIDF()
    foo.index_documents(articles, titles)
    query = request.args.get('query')
    matches = []
    if query:
        matches = foo.test_query(query)
    return render_template('searchpage.html', matches=matches)


