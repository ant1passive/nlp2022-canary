# nlp2022-canary

This repository contains a demo program involving web scraping and natural language processing. The program has the following functions:
  1. A search engine that retrieves text from a local excerpt of 100 Wikipedia articles using both Boolean and TF-IDF search.
  2. A web crawler that looks at interlanguage links of a Wikipedia article and and retrieves the article length for each language.

When user makes a search using function (1), search results (if any) will appear tabulated. One of these results can be chosen for further analysis via a radio button in the rightmost column of the table. Clicking on "Analyse" will then run the web crawler.

Even though the one-hundred-article Wikipedia excerpt for searches is a local file, the crawler accesses actual Wikipedia pages. It just takes the title of a search result as input and starts from the corresponding Wikipedia article on the internet.

The program is used via web browser at `localhost:8000/search`. The programs employ Flask to serve a page to the browser.

### Trying out the program

Clone the git repository and change to `nlp2022-canary` directory:

```
git clone https://github.com/ant1passive/nlp2022-canary
cd nlp2022-canary
```

Create a virtual environment `demoenv` and activate it:

```
python3 -m venv demoenv
. demoenv/bin/activate
```

On Windows:

```
py -3 -m venv demoenv
demoenv/Scripts/activate
```

Install Python packages required by the program:

```
pip install Flask scikit-learn beautifulsoup4 iso-639 lxml matplotlib
```

While `demoenv` is active, run an initialization script to set environment variables for Flask:

```
. init-search.sh
```

On Windows:

```
init-search.bat
```

Start the application:

```
flask run
```

Go to `localhost:8000/search` in your browser to see the user interface.

