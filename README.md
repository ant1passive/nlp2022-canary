# nlp2022-canary

This repository contains two demo programs involving web scraping and natural language processing:
  1. A search engine that retrieves text from an excerpt of 100 Wikipedia articles using both Boolean and TF-IDF search.
  2. A web crawler that, given a URL to a Wikipedia article, looks at interlanguage links on that page and retrieves the article length for each language.

Both programs are used via web browser at `localhost:8000/search`. The programs employ Flask to serve a page to the browser.

### How to try out the demos

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

Install packages required by the demos:

```
pip install Flask scikit-learn beautifulsoup4 iso-639 lxml matplotlib

```

### Search engine demo

Run an initialization script to set environment variables for Flask:

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

### Wikipedia article analyzer demo

Run the initialization script named `init-wpa` instead of `init-search`, then give the command `flask run`. Note that the demos won't run at the same time, because both use port 8000 for communication.

