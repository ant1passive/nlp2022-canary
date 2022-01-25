
from nltk import word_tokenize

from urllib import request
url = "https://yle.fi/uutiset"
html = request.urlopen(url).read().decode('utf8')

from bs4 import BeautifulSoup
raw = BeautifulSoup(html, 'html.parser').get_text()
tokens = word_tokenize(raw)
print(tokens)

import requests

url_link = "https://www.foreca.fi/"
request = requests.get(url_link)

Soup = BeautifulSoup(request.text, 'html.parser')

heading_tags = ["h1", "h2", "h3"]
for tags in Soup.find_all(heading_tags):
    print(tags.name + ' -> ' + tags.text.strip())

for link in Soup.find_all("a"):
    print("Text: {}".format(link.text))
    print("href: {}".format(link.get("href")))