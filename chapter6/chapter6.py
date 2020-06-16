#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

if __name__ == "__main__":

    # read csv
    news_corpora = pd.read_csv(
        "./chapter6/newsCorpora.csv", sep="\t", header=None)
    news_corpora.columns = ["id", "title", "url",
                            "publisher", "category", '_', '_', '_']
    print("read csv")

    # filter by publisher
    news_corpora = news_corpora.query(
        'publisher in ["Reuters", "Huffington Post", "Businessweek", "Contactmusic.com", "Daily Mail"]')
    print("filtered by publishers")

    # 51. 特徴量抽出
    # How: create bag of words
    vectorizer = CountVectorizer()
    df_X = pd.DataFrame(vectorizer.fit_transform(
        news_corpora['title']).toarray())
    df_X.columns = vectorizer.get_feature_names()
    df_X = pd.concat(
        [df_X, news_corpora['category'].reset_index(drop=True).rename('y_label_category')], axis=1)

    # train, test, validation split to 8:1:1 ratio
    # first (train, test & validation) to 8:2 ratio,
    # and then split test&validation to 1:1, which results in 8:1:1 ratio.
    from sklearn.model_selection import train_test_split
    train, test_validate = train_test_split(
        df_X, random_state=821, shuffle=True, test_size=.2)
    test, validate = train_test_split(
        test_validate, shuffle=False, test_size=.5)
    print("test, test, validate")

    # save them all
    train.to_csv("train.txt")
    test.to_csv("test.txt")
    validate.to_csv("validate.txt")

    # 52. 学習
    # train the model
    model = LogisticRegression(random_state=821)
    model.fit(train.drop('y_label_category', axis=1),
              train['y_label_category'])

    # pickle the model so that I can use it in my app later
    import pickle
    with open('./chapter6/model.pickled', mode='wb') as f:
        pickle.dump(model, f)

    # and column names too
    with open('./chapter6/feature_names', mode='w') as f:
        f.write(vectorizer.get_feature_names())
