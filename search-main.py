
from se_boolean import searchEngineBoolean
from se_tfidf import searchEngineTFIDF

foo = searchEngineBoolean()

"""

foo.test_query("example AND NOT nothing")
foo.test_query("NOT example OR great")
foo.test_query("( NOT example OR great ) AND nothing") # AND, OR, NOT can be written either in ALLCAPS
foo.test_query("( not example or great ) and nothing") # ... or all small letters
foo.test_query("not example and not nothing")

"""

# 5. opens text file and splits text to articles
#path = input("Give filepath")
path = r"write your path"
#path = r"./input-texts/enwiki-20181001-corpus.100-articles.txt"
file = open(path, encoding="utf8")
document = file.read()
articles = document.split("</article>")
print(len(articles))
#print(articles[100])
#print(articles[0])

foo.index_documents(articles)

while True:
    try:
        user_query = str(input("Type the query, or enter 'quit': "))
        if user_query != 'quit':
            foo.test_query(user_query)
        else:
            break
    except (TypeError):
        print('Invalid input')
    except (KeyError):
        print('Keyerror')
    except (SyntaxError):
        print('Syntax Error')


