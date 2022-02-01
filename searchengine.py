
# Week 2: First search engine.
# Contains code from boolean-search-tutorial at
# https://notebooks.csc.fi/notebooks/19db991cc4924741a6d4637de9b5cdb8/tree/nlp-tutorials/tutorials

from sklearn.feature_extraction.text import CountVectorizer

class searchEngine:

    def __init__(self):

        self.max_shown_documents = 10
        self.max_shown_characters = 72
        self.documents = ["This is a silly example",
                          "A better example",
                          "Nothing to see here",
                          "This is a great and long example"]

        self.cv = CountVectorizer(lowercase=True, binary=True)
        self.sparse_matrix = self.cv.fit_transform(self.documents)

        #print("Term-document matrix: (?)\n")
        #print(self.sparse_matrix)

        self.sparse_td_matrix = self.sparse_matrix.T.tocsr()
        self.t2i = self.cv.vocabulary_  # shorter notation: t2i = term-to-index

        # Operators and/AND, or/OR, not/NOT become &, |, 1 -
        # Parentheses are left untouched
        # Everything else interpreted as a term and fed through td_matrix[t2i["..."]]
        self.d = {"and": "&", "AND": "&",
                  "or": "|", "OR": "|",
                  "not": "1 -", "NOT": "1 -",
                  "(": "(", ")": ")"}          # operator replacements

    def rewrite_token(self, t):
        return self.d.get(t, 'self.sparse_td_matrix[self.t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense

    def rewrite_query(self, query): # rewrite every token in the query
        return " ".join(self.rewrite_token(t) for t in query.split())

    def test_query(self, query):
        print("Query: '" + query + "'")
        print("Rewritten:", self.rewrite_query(query))
        print("Matching documents: \n")
        total_matches = 0
        results = eval(self.rewrite_query(query)).getA()[0] #Convert the numpy matrix into a numpy array so it may be iterated
        for i, match in enumerate(results):                 #Iterate through the array and print the corresponding documents if true 
            if match == 1:
                total_matches += 1
                if total_matches <= self.max_shown_documents:
                    print(str(self.documents[i][:self.max_shown_characters]))
                    
        print()
        print("Total matches:", total_matches)
        print()    

