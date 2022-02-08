
from se_boolean import searchEngineBoolean
from se_tfidf import searchEngineTFIDF
from bs4 import BeautifulSoup
import numpy

numpy.set_printoptions(threshold = numpy.inf) #For testing purposes, allows long matrices to be printed in full.


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
    foo = searchEngineBoolean()

    # 5. opens text file and splits text to articles
    path = r"write your path"
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

    #print(titles)
    #print(text)

    while not done:

        user_input = input("Select action:\n1. Set Boolean search\n2. Set tf-idf search\n3. Enter query prompt\nEnter choice or type 'quit' to exit: ")
        if user_input == "1":
            foo = searchEngineBoolean()
            foo.index_documents(articles, titles)
        elif user_input == "2":
            foo = searchEngineTFIDF()
            foo.index_documents(articles, titles)
        elif user_input == "3":
            queryPrompt(foo)
        elif user_input.lower() == 'quit':
            done = True


# -   -   -   run this thing   -   -   - #
main()


"""

foo.test_query("example AND NOT nothing")
foo.test_query("NOT example OR great")
foo.test_query("( NOT example OR great ) AND nothing") # AND, OR, NOT can be written either in ALLCAPS
foo.test_query("( not example or great ) and nothing") # ... or all small letters
foo.test_query("not example and not nothing")

"""

