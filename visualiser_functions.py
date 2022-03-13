from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def cat_plot(categories, values):                   #takes two lists as arguments
    plt.figure()                                    #initialize the figure thingamajig
    cats = categories
    vals = values
    if len(cats) > len(vals):
        for i in range(len(cats) - len(vals)):      #if the lists are not of the same length, add stuff to the shorter one until they are
            vals.append(0)
    if len(cats) < len(vals):
        for i in range(len(vals) - len(cats)):      
            cats.append("unknown category")
    bars = plt.barh(cats, vals)                             #create a bar graph and save it as an image
    bars[0].set_color('r')
    plt.savefig("plots\graphimage.png")


def cat_plot_tuple(tuples):                         #takes a tuple
    cats = []
    vals = []

    for tuple in tuples:
        try:
            cats.append(str(tuple[0]))              #some error handling
        except:
            cats.append("unknown category")
        try:    
            vals.append(float(tuple[1]))
        except:
            vals.append(0)
    
    fig_height = max(6, 0.13*len(tuples))               #autoscale figure according to amount of data
    plt.figure(figsize=(8, fig_height))                 #initialize the figure thingamajig
    bars = plt.barh(cats, vals)                         #create a bar graph and save it as an image
    bars[0].set_color('r')

    # Create the directory 'static' if it isn't there yet.
    # It is ignored by version control, and doesn't exist after cloning.
    Path("./static").mkdir(parents=True, exist_ok=True)
    plt.savefig("static/graphimage.png")



#cat_plot(["a", "b", "c"], [1.0, 2.0, 3.0])
#cat_plot_tuple([("a", 1.0), ("b", 2.0), ("c", 3.3), (3, "d"), (True)])
    
    

    
    

