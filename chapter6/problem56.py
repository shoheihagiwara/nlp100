#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pandas as pd
import pickle
from sklearn.metrics import classification_report as cr

if __name__ == "__main__":

    # 56. 適合率，再現率，F1スコアの計測

    # train testの読み込み
    df_train = pd.read_csv('train.txt', index_col=0)
    df_test  = pd.read_csv('test.txt', index_col=0)

    # modelの読み込み
    with open('./chapter6/model.pickled', 'rb') as f:
        model = pickle.load(f)

    y_label = 'y_label_category'
    train_pred_y = model.predict(df_train.drop(y_label, axis=1))
    test_pred_y  = model.predict(df_test.drop(y_label, axis=1))
    print(cr(df_train[y_label], train_pred_y))
    print(cr(df_test[y_label], test_pred_y))


