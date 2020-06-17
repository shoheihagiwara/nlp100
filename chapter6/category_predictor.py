#!/usr/bin/env python
# -*- encoding: utf-8
import os
import sys
import pickle
import pandas as pd
sys.path.append(os.getcwd())

with open('chapter6/model.pickled', mode='rb') as f:
    model = pickle.load(f)

with open('chapter6/feature_names') as f:
    feature_names = eval(f.read())

if __name__ == "__main__":

    from lib.utilities import make_bag_of_words

    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} [TITLE]')
        exit(1)

    title = sys.argv[1]

    s = pd.Series(title)
    df_X, _ = make_bag_of_words(s, vocabulary=feature_names)

    category = model.predict(df_X)[0]
    prob_list = model.predict_proba(df_X)[0]

    if category == 'b':
        category = 'business'
    elif category == 'e':
        category = 'entertainment'
    elif category == 'm':
        category = 'medical'
    elif category == 't':
        category = 'technology'
    else:
        category = 'Category Undefined'

    print(category, list(zip(model.classes_, prob_list)))
