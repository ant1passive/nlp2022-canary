
# Week 2: First search engine.
# Contains code from boolean-search-tutorial at
# https://notebooks.csc.fi/notebooks/19db991cc4924741a6d4637de9b5cdb8/tree/nlp-tutorials/tutorials

from sklearn.feature_extraction.text import CountVectorizer

# Operators and/AND, or/OR, not/NOT become &, |, 1 -
# Parentheses are left untouched
# Everything else interpreted as a term and fed through td_matrix[t2i["..."]]

max_documents = 2
max_characters = 10

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements

def rewrite_token(t):
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

"""
def test_query(query):
    print("Query: '" + query + "'")
    print("Rewritten:", rewrite_query(query))
    print("Matching:", eval(rewrite_query(query))) # Eval runs the string as a Python command 
    print()
"""

def test_query(query):
    print("Query: '" + query + "'")
    print("Rewritten:", rewrite_query(query))
    print("Matching documents: \n")
    total_matches = 0
    results = eval(rewrite_query(query)).getA()[0] #Convert the numpy matrix into a numpy array so it may be iterated
    for i, match in enumerate(results):            #Iterate through the array and print the corresponding documents if true 
        if match == 1:
            total_matches += 1
            if total_matches <= max_documents:
                print(str(documents[i][:max_characters]))
                
    print()
    print("Total matches:", total_matches)
    print()


documents = ["This is a silly example",
             "A better example",
             "Nothing to see here",
             "This is a great and long example"]

cv = CountVectorizer(lowercase=True, binary=True)
sparse_matrix = cv.fit_transform(documents)

print("Term-document matrix: (?)\n")
print(sparse_matrix)

sparse_td_matrix = sparse_matrix.T.tocsr()
t2i = cv.vocabulary_  # shorter notation: t2i = term-to-index

test_query("example AND NOT nothing")
test_query("NOT example OR great")
test_query("( NOT example OR great ) AND nothing") # AND, OR, NOT can be written either in ALLCAPS
test_query("( not example or great ) and nothing") # ... or all small letters
test_query("not example and not nothing")

"""
# ask the user to type the query
user_query = ''
# Start a loop that will run until the user enters 'quit'.
while user_query != 'quit':
    # Ask the user for a query
    user_query = input("Type the query, or enter 'quit': ")
    # runs the query
    if user_query != 'quit':
        test_query(user_query)
"""

# same as up but includes errors
while True:
    try:
        user_query = str(input("Type the query, or enter 'quit': "))
        if user_query != 'quit':
            test_query(user_query)
        else:
            break
    except (TypeError):
        print('Invalid input')
    except (KeyError):
        print('Keyerror')
    except (SyntaxError):
        print('Syntax Error')


