#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd


def make_bag_of_words(s: pd.Series, vocabulary=None):
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    df_X = pd.DataFrame(vectorizer.fit_transform(s).toarray())
    df_X.columns = vectorizer.get_feature_names()
    return (df_X, vectorizer.get_feature_names())
