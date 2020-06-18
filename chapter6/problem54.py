#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pickle
import pandas as pd
from sklearn.metrics import classification_report

if __name__ == "__main__":
    # 54. 正解率の計測
    # 52で学習したロジスティック回帰モデルの正解率を，学習データおよび評価データ上で計測せよ．

    # モデルをロード
    with open('chapter6/model.pickled', mode="rb") as f:
        model = pickle.load(f)

    def print_classification_report(csv_name):
        df = pd.read_csv(csv_name, index_col=0)
        y_pred = model.predict(df.drop('y_label_category', axis=1))
        y_true = df.y_label_category
        print(csv_name)
        print(classification_report(y_pred=y_pred, y_true=y_true))

    # trainデータで正答率を計測
    print_classification_report('train.txt')

    # validateデータで正答率を計測
    print_classification_report('validate.txt')

    # 55. 混同行列の作成
    # 52で学習したロジスティック回帰モデルの混同行列（confusion matrix）を，学習データおよび評価データ上で作成せよ．
    def print_confusion_matrix(csv_name):
        from sklearn.metrics import confusion_matrix
        df = pd.read_csv(csv_name, index_col=0)
        y_pred = model.predict(df.drop('y_label_category', axis=1))
        y_true = df.y_label_category
        print(csv_name)
        print(confusion_matrix(y_true, y_pred))

    # 学習データと評価データでやる
    print_confusion_matrix('train.txt')
    print_confusion_matrix('validate.txt')
