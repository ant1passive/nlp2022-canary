
# Week 2: First search engine.
# Contains code from boolean-search-tutorial at
# https://notebooks.csc.fi/notebooks/19db991cc4924741a6d4637de9b5cdb8/tree/nlp-tutorials/tutorials

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


example_documents = ["This is a silly example",
                     "A better example",
                     "Nothing to see here",
                     "This is a great and long example"]


class searchEngineTFIDF:

    def __init__(self):
        self.max_shown_documents = 10
        self.max_shown_characters = 72  # one row of usual console window
        self.wildcard_max_queries = 20  #Prevents the program from searching with every possible query if user searches '*'

        # Operators and/AND, or/OR, not/NOT become &, |, 1 -
        # Parentheses are left untouched
        # Everything else interpreted as a term and fed through td_matrix[t2i["..."]]
        self.d = {}          # operator replacements

        # initialize this instance with silly examples by default
        #self.index_documents(example_documents)


    def index_documents(self, documents, titles):
        self.documents = documents
        self.titles = titles
        self.tf = TfidfVectorizer(lowercase=True, sublinear_tf = True, use_idf = True, norm = "l2")
        self.sparse_matrix = self.tf.fit_transform(self.documents).T.todense()
        #print("Term-document matrix: (?)\n")
        #print(self.sparse_matrix)
        #self.sparse_td_matrix = self.sparse_matrix.T.tocsr()
        self.t2i = self.tf.vocabulary_  # shorter notation: t2i = term-to-index
        self.all_words = []
        for key in self.t2i.keys():
            self.all_words.append(key)
        #print(self.all_words[:10])


    def test_query(self, query):
        self.scores = []

        # If the query has an *, do a wildcard search. Currently only
        # works if in the beginning or end of query
        queries_to_make = []

        query = query.lower()

        if query[0] == '*':
            for word in self.all_words:
                if query[1:].lower() in word[-len(query[1:]):]:
                    if len(queries_to_make) < self.wildcard_max_queries:
                        queries_to_make.append(word)

        elif query[-1] == '*':
            for word in self.all_words:
                if query[:-1].lower() in word[:(len(query)-1)]:
                    if len(queries_to_make) < self.wildcard_max_queries:
                        queries_to_make.append(word)

        elif '*' in query:
            asterisk_index = query.index('*')
            word_left = query[:asterisk_index]
            word_right = query[asterisk_index + 1:]
            for word in self.all_words:
                if len(word) > asterisk_index:
                    if word_left == word[:asterisk_index]:
                        if word_right == word[-len(word_right):]:
                            print(word)
                            print(word_right, word[-len(word_right):])
                            queries_to_make.append(word)


        else:   # There was no '*' in query, use the query as-is
            queries_to_make.append(query)
        #print("Queries made:", queries_to_make)
#lol
        #print(queries_to_make)


        for word in queries_to_make:
            query_vector = self.tf.transform([word]).todense() #Calculate a vector for the query
            for i in range(0, len(self.documents)-1):          #Assign similarity scores to all documents, and store them in a list
                document_vector = self.sparse_matrix[:, i]
                score = np.array(np.dot(query_vector, document_vector))[0][0]
                self.scores.append((score, i))

        self.scores.sort(reverse = True) 

        #print("Most similar documents: \n")
        self.final_list = []

        for i in range(0, self.max_shown_documents):            #create a list that can be returned
            if self.scores == []:
                # no matches, return the empty list
                return self.final_list
            else:
                document_index = self.scores[i][1]
                if self.scores[i][0] > 0:
                    title = self.titles[document_index]
                    contents = str(self.documents[document_index][:self.max_shown_characters])
                    similarity = self.scores[i][0]
                    self.final_list.append((title, contents, similarity))

        return self.final_list

