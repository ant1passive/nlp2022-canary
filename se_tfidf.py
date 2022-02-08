
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

        # Operators and/AND, or/OR, not/NOT become &, |, 1 -
        # Parentheses are left untouched
        # Everything else interpreted as a term and fed through td_matrix[t2i["..."]]
        self.d = {}          # operator replacements

        # initialize this instance with silly examples by default
        #self.index_documents(example_documents)


    def index_documents(self, documents):
        self.documents = documents
        self.tf = TfidfVectorizer(lowercase=True, sublinear_tf = True, use_idf = True, norm = "l2")
        self.sparse_matrix = self.tf.fit_transform(self.documents).T.todense()
        #print("Term-document matrix: (?)\n")
        #print(self.sparse_matrix)
        #self.sparse_td_matrix = self.sparse_matrix.T.tocsr()
        self.t2i = self.tf.vocabulary_  # shorter notation: t2i = term-to-index
        self.all_words = []
        for key in self.t2i.keys():
            self.all_words.append(key)
        print(self.all_words[:10])
     



    def test_query(self, query):
        print("Query: '" + query + "'")
        
        self.scores = []
        if '*' in query:
            queries_to_make = []
            if query[0] == '*':
                for word in self.all_words:
                    if query[1:] in word[-len(query[1:]):]:
                        queries_to_make.append(word)

            elif query[-1] == '*':
                for word in self.all_words:
                    if query[:-1] in word[:(len(query)-1)]:
                        queries_to_make.append(word)   
            
            else:
                pass
            print(queries_to_make)
            for word in queries_to_make:
                query_vector = self.tf.transform([word]).todense() #Calculate a vector for the query
                for i in range(0, len(self.documents)-1):        #Assign similarity scores to all documents, and store them in a list
                    document_vector = self.sparse_matrix[:, i]
                    score = np.array(np.dot(query_vector, document_vector))[0][0]

                    self.scores.append((score, i))

                
                
        else:
            query_vector = self.tf.transform([query]).todense() #Calculate a vector for the query
            for i in range(0, len(self.documents)-1):        #Assign similarity scores to all documents, and store them in a list
                document_vector = self.sparse_matrix[:, i]
                score = np.array(np.dot(query_vector, document_vector))[0][0]

                self.scores.append((score, i))

        self.scores.sort(reverse = True) 

        print("Most similar documents: \n")
            
        for i in range(0, self.max_shown_documents):       #Print the documents with the highest scores 
            document_index = self.scores[i][1]
            if self.scores[i][0] > 0:
                print(str(self.documents[document_index][:self.max_shown_characters]), "\n")
                print("Similarity to query:", self.scores[i][0], "\n")
