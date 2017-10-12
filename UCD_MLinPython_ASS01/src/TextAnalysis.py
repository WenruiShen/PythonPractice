#********************************************************************************
#                                                                               #
#            UCD-COMP41680 Machine Learning                                     #
#    Assignment 2:      Text Scraping & Clustering                              #
#    Author:            Wenrui.Shen                                             #
#    Student Number:    15210671                                                #
#    E-mail:            wenrui.shen@ucdconnect.ie                               #
#    Date:              2017-05-03                                              #
#    Description:       Text Analysis for part-2                                #
#                                                                               #
#********************************************************************************

import io
import os
import sys
import codecs
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
#from matplotlib.patches import Ellipse


#*****************************************************************************************
# Step-0: System initialization.                                                         *
#*****************************************************************************************
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
news_content_subdir = "news/"

#--------------------------------------------------------
#             Format of list: news_documents            |
#-------------------------------------------------------|
#         term_1    term_2    term_3    ...    term_n   |
# news_1:     0        1        0                1      |
# news_2:     1        0        0                0      |
# ...                                                   |
# news_n:     0        0        1                1      |
#--------------------------------------------------------
news_documents = []


#*****************************************************************************************
# Step-1: Get all news files under this directory.                                       *
#*****************************************************************************************
print("Step-1: Now Start part-2 news analysis.")
for news_filename in os.listdir(news_content_subdir):
    if news_filename.endswith(".txt"):
        #print (news_filename)
        news_f = codecs.open(news_content_subdir + news_filename, 'r', "utf-8")
        news_lines = news_f.readlines() 
        news_content = ""
        for news_line in news_lines:
            news_content += news_line.lower()
        news_documents.append(news_content)
        news_f.close()
print("\t# Totally %d news file." % len(news_documents))



#*****************************************************************************************
# Step-2: Create whole terms matrix for all news.                                        *
#*****************************************************************************************
print("Step-2: Process the news.")

# Define the function.
def lemma_tokenizer(text):
    # use the standard scikit-learn tokenizer first
    standard_tokenizer = CountVectorizer().build_tokenizer()
    tokens = standard_tokenizer(text)
    # then use NLTK to perform lemmatisation on each token
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemma_tokens = []
    for token in tokens:
        lemma_tokens.append( lemmatizer.lemmatize(token) )
    return lemma_tokens

#news_vectorizer = CountVectorizer(stop_words="english", min_df = 5, tokenizer=lemma_tokenizer)
# Term Weighting.
news_vectorizer = TfidfVectorizer(stop_words="english", min_df = 5, tokenizer=lemma_tokenizer)
news_terms_vector = news_vectorizer.fit_transform(news_documents)
print("\t# The matrix's shape: " + str(news_terms_vector.shape))
news_terms = news_vectorizer.get_feature_names()
print("\t# Vocabulary has %d distinct terms" % len(news_terms))



#*****************************************************************************************
# Step-3: Summarize the top most characteristic terms for overall news.                  *
#*****************************************************************************************
print("Step-3: Summarization.")

#    Function Input:          unsorted unmpy.array of  terms' weights.
#    Function Output:         numpy.array of indexes about top greatest terms' weights.
#    Function description:    Return an array of index with top max weight.
def f_get_sorted_index_array(terms_weight_sum_array, select_num):
    return np.argsort(terms_weight_sum_array)[::-1][:select_num]

# Get an flat 1-D numpy.array of different terms' weights' summarization from sparse matrix.
terms_weight_sum_array = (news_terms_vector.sum(axis=0).getA())[0]
# Get terms' words according their indexes.
sorted_index_array = f_get_sorted_index_array(terms_weight_sum_array, 20)

print("\tThe top 20 most characteristic terms are:")
print("\tTerms\tIndex\tWeight")
for sorted_index in sorted_index_array:
    print("\t" + str(news_terms[sorted_index]) \
          + "\t:" + str(sorted_index)          \
          + "\t:" + str(terms_weight_sum_array[sorted_index]))



#*****************************************************************************************
# Step-4: Clustering algorithm - A: k-Means Clustering.                                                      #
#*****************************************************************************************
print("Step-4: Clustering algorithm - A: k-Means Clustering.")

# Note: the 's' parameter controls the size of the points
print(type(news_terms_vector))
print(type(news_terms_vector.toarray()))
print(news_terms_vector.toarray().shape)
plt.scatter((news_terms_vector.toarray())[:, 0], (news_terms_vector.toarray())[:, 1])

'''
ellipse = Ellipse(xy=(157.18, 68.4705), width=0.036, height=0.012, 
                        edgecolor='r', fc='None', lw=2)
ax.add_patch(ellipse)
'''
















