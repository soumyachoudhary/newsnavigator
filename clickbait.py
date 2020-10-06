import numpy as np 
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string as s
import re

from sklearn.model_selection import cross_val_score

import pickle
lemmatizer=nltk.stem.WordNetLemmatizer()
tfidf=pickle.load(open("vectorizer1.pickle", "rb"))
NB_MN=pickle.load(open("model1.pickle", "rb"))

def tokenization(text):
    lst=text.split()
    return lst


def lowercasing(lst):
    new_lst=[]
    for i in lst:
        i=i.lower()
        new_lst.append(i)
    return new_lst


def remove_punctuations(lst):
    new_lst=[]
    for i in lst:
        for j in s.punctuation:
            i=i.replace(j,'')
        new_lst.append(i)
    return new_lst

def remove_numbers(lst):
    nodig_lst=[]
    new_lst=[]
    for i in lst:
        for j in s.digits:    
            i=i.replace(j,'')
        nodig_lst.append(i)
    for i in nodig_lst:
        if i!='':
            new_lst.append(i)
    return new_lst

def remove_stopwords(lst):
    stop=stopwords.words('english')
    new_lst=[]
    for i in lst:
        if i not in stop:
            new_lst.append(i)
    return new_lst

def remove_spaces(lst):
    new_lst=[]
    for i in lst:
        i=i.strip()
        new_lst.append(i)
    return new_lst


def lemmatzation(lst):
    new_lst=[]
    for i in lst:
        i=lemmatizer.lemmatize(i)
        new_lst.append(i)
    return new_lst

def is_clickbait(k):
	test_x = pd.DataFrame(data = [k])[0]
	test_x=test_x.apply(tokenization)
	test_x=test_x.apply(lowercasing)  
	test_x=test_x.apply(remove_punctuations)  
	test_x=test_x.apply(remove_numbers)
	test_x=test_x.apply(remove_stopwords)  
	test_x=test_x.apply(remove_spaces)
	test_x=test_x.apply(lemmatzation)
	test_x=test_x.apply(lambda x: ''.join(i+' ' for i in x))
	test_1=tfidf.transform(test_x)
	test_arr=test_1.toarray()
	pred=NB_MN.predict(test_arr)
	return(pred[0])

