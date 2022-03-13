from visualiser_functions import cat_plot_tuple
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from wp_article import wp_article
from operator import itemgetter
import numpy

numpy.set_printoptions(threshold = numpy.inf) #For testing purposes, allows long matrices to be printed in full.
app = Flask(__name__)

@app.route('/search')
def search():

    # create an initial article object
    print(request.args.get('query'))
    url = request.args.get('query')
    if not url:
        return render_template('wp-analysis-results.html', matches = [])

    #user_input = request.args.get('query')
    #if not user_input:
    #    return render_template('searchpage.html', matches = [])

    else:
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

        return render_template('wp-analysis-results.html', matches=matches)


