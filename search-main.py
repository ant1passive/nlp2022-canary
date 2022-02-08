
from se_boolean import searchEngineBoolean
from se_tfidf import searchEngineTFIDF
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
    # path = input("Give filepath")
    path = r"write your path"
    #path = r"./input-texts/enwiki-20181001-corpus.100-articles.txt"
    file = open(path, encoding="utf8")
    document = file.read()
    articles = document.split("</article>")
    # print(len(articles))
    # print(articles[100])
    # print(articles[0])

    while not done:

        user_input = input("Select action:\n1. Set Boolean search\n2. Set tf-idf search\n3. Enter query prompt\nEnter choice or type 'quit' to exit: ")
        if user_input == "1":
            foo = searchEngineBoolean()
            foo.index_documents(articles)
        elif user_input == "2":
            foo = searchEngineTFIDF()
            foo.index_documents(articles)
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

