#!/bin/env python
# -*- coding: utf-8 -*-

import pickle
import pprint
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":

    # 57. 特徴量の重みの確認

    # first read the model.
    with open('./chapter6/model.pickled', 'rb') as f:
        model = pickle.load(f)

    with open('./chapter6/feature_names') as f:
        f_names = eval(f.read())
        print(f_names)



    # 最終的にはクラスごとに特徴量が重みが高い順に出したいので、
    # まずはクラスごとのdictをつくる
    # dictで、中身が、キーがクラス、値にdict、そのdictの中身が、
    # キーに特徴量名、値にその特徴量の重み
    class_coef_dict = {}
    for cls, features in zip(model.classes_, model.coef_):
        tmp_dict = {}
        for name, feature in zip(f_names, features):
            tmp_dict[name] = feature
        class_coef_dict[cls] = tmp_dict

    # 特徴量の重い順に並べる
    # 結果、class_coef_dictの中身は
    # {class: [('1番小さい特徴量名', 重み),('2番目に小さい特徴量名', 重み),...]}
    # となる。
    for cls, f_dict in class_coef_dict.items():
        class_coef_dict[cls] = sorted(f_dict.items(), key=lambda x: x[1])

    for i, cls in enumerate(class_coef_dict.keys()):
        # 各クラスの棒グラフを作る
        top_and_last = [*class_coef_dict[cls][:10], *class_coef_dict[cls][-10:]]
        x = [x[0] for x in top_and_last]
        y = [x[1] for x in top_and_last]
        plt.subplot(2,2,i+1)
        plt.barh(x, y)
        plt.title('class: ' + cls)
    plt.show()





    ### print(model.coef_)
    ### print(model.coef_)
    ### df = pd.DataFrame(data=[[1,2,3],[4,5,6],[7,8,9]], columns=['a','b','c'])
    ### print(df)
    ### plt.bar(data=df)
    ### plt.show()

