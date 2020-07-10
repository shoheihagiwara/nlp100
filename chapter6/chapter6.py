#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer

sys.path.append(os.getcwd())

if __name__ == "__main__":

    from lib.utilities import make_bag_of_words

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
    df_X, feature_names = make_bag_of_words(news_corpora['title'])
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
    model = LogisticRegression(random_state=821, max_iter=200)
    model.fit(train.drop('y_label_category', axis=1),
              train['y_label_category'])

    # pickle the model so that I can use it in my app later
    import pickle
    with open('./chapter6/model.pickled', mode='wb') as f:
        pickle.dump(model, f)

    # and column names too
    with open('./chapter6/feature_names', mode='w', encoding='utf-8') as f:
        f.write(str(feature_names))

    # 53. 予測
    # TODO あとでやる。

    # 54. 正解率の計測   56. 適合率，再現率，F1スコアの計測
    y_test = test['y_label_category']
    y_pred = model.predict(test.drop('y_label_category', axis=1))
    print(classification_report(y_pred=y_pred, y_true=y_test))
