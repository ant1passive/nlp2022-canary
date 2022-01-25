import nltk, re, pprint
from nltk import word_tokenize

from urllib import request
url = "https://yle.fi/uutiset"
html = request.urlopen(url).read().decode('utf8')

from bs4 import BeautifulSoup
raw = BeautifulSoup(html, 'html.parser').get_text()
tokens = word_tokenize(raw)
print(tokens)