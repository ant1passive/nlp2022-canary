
import nltk, re, pprint
from nltk import word_tokenize
from urllib import request
from bs4 import BeautifulSoup

url = "https://yle.fi/uutiset"
html = request.urlopen(url).read().decode('utf8')

# parse HTML to find paragraph tags
soup = BeautifulSoup(html, 'html.parser')
paragraphs = soup.find_all(['p', 'h2', 'h3', 'h6'])

# accumulate text content of paragraphs to a list
text = list()
for p in paragraphs:
    text.append(p.text)

# concatenate all strings that we found
text = " ".join(text)

# throw away soft hyphens that YLE uses in their text
text = text.replace('\u00ad', '')

tokens = word_tokenize(text)
print('\n === Tokenized text from yle.fi/uutiset ===\n')
print(*tokens, sep=' ')
print('')

import requests

url_link = "https://www.foreca.fi/"
request = requests.get(url_link)

Soup = BeautifulSoup(request.text, 'html.parser')

print('\n === Text from heading tags at foreca.fi ===\n')

heading_tags = ["h1", "h2", "h3"]
for tags in Soup.find_all(heading_tags):
    print(tags.name + ' -> ' + tags.text.strip())

print('\n === Text from link tags at foreca.fi ===\n')

for link in Soup.find_all("a"):
    print("Text: {}".format(link.text))
    print("href: {}".format(link.get("href")))

