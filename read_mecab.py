import csv
import sys

def make_dict_from_csv(path: str) -> list:
    with open(path, encoding='utf-8') as f:
        mecab_result_list = csv.reader(f)

        result_list = []
        inner_list = []
        for one_keitaiso in mecab_result_list:
            # sentence: 表層形surface,品詞pos,品詞細分類1pos1,品詞細分類2,品詞細分類3,活用型,活用形,原形base,読み,発音
            # index:    0             1      2               3          4          5     6      7       8    9

            if one_keitaiso[0] == 'EOS':
                result_list.append(inner_list)
                inner_list = []
                continue

            tmpDict = {"surface": one_keitaiso[0],
                        "pos"   : one_keitaiso[1],
                        "pos1"  : one_keitaiso[2],
                        "base"  : one_keitaiso[7]}
            inner_list.append(tmpDict)

    return result_list

if __name__ == "__main__":

    path: str = "neko.txt.csv"
    result_list = make_dict_from_csv(path)
    #sys.stdout.buffer.write(str(result_list[:1]).encode('utf-8'))
    #print()
    #sys.stdout.buffer.write(str(result_list[-4:]).encode('utf-8'))

    # result_listには以下のようにデータが入ってる。
    #
    # [
    #   [                             ←ここが1つの文を表す 
    #       {"surface": "XXX",        ←これが1つの形態素を表す
    #        "pos"    : "XXX",
    #        "pos1"   : "XXX",
    #        "base"   : "XXX"}
    #       ...
    #   ],
    #   ...
    # ]

    # 31. 動詞
    # 動詞の表層形をすべて抽出せよ．
    verb_set = set()
    for sentence in result_list:
        for elem in sentence:
            if elem["pos"] == "動詞":
                verb_set.add(elem["surface"])
    with open("verb_surface_set.txt", encoding="utf-8", mode='w') as f:
        print(verb_set, file=f)

    # 32. 動詞の原形Permalink
    # 動詞の原形をすべて抽出せよ．
    def write_verb_base_set():
        verb_base_set = set()
        for sentence in result_list:
            for elem in sentence:
                if elem["pos"] == "動詞":
                    verb_base_set.add(elem["base"])
        with open("verb_base_set.txt", encoding="utf-8", mode='w') as f:
            print(verb_base_set, file=f)
    write_verb_base_set()

    # 33. 「AのB」
    # 2つの名詞が「の」で連結されている名詞句を抽出せよ．
    # https://nlp100.github.io/ja/ch04.html#33-a%E3%81%AEb
    def write_connected_nouns():
        connected_nouns = set()
        for sentence in result_list:
            for i in range(len(sentence) - 2):
                first =  sentence[i]
                second = sentence[i+1]
                third =  sentence[i+2]
                if first["pos"] == "名詞" \
                        and second["pos"] == "助詞" and second["base"] == "の" \
                        and third["pos"] == "名詞": 
                    connected_nouns.add(first["surface"] + second["surface"] + third["surface"])
        with open("connected_nouns.txt", encoding="utf-8", mode="w") as f:
            print(connected_nouns, file=f)
    write_connected_nouns()

    # 34. 名詞の連接
    # 名詞の連接（連続して出現する名詞）を最長一致で抽出せよ．
    # https://nlp100.github.io/ja/ch04.html#34-%E5%90%8D%E8%A9%9E%E3%81%AE%E9%80%A3%E6%8E%A5
    def find_catted_nouns() -> list:
        """すべての名詞の連接を見つけリストで返却する

        最長一致で見つける。

        ステップ説明：
        各文をループして、各文の要素をループする。要素iを見て名詞だったら、記憶して、次の要素がないor次の要素が名詞ではないとき、
        かつ、記憶してきた名詞が2つ以上あったら、それは名詞の連接になるのでリストに入れて記憶をなくす。
        要素iが名詞でなかったら、記憶をなくす。
        
        """
        catted_noun_list  = []
        for sentence in result_list:
            tmp_catted_noun = []
            for i, elem in enumerate(sentence):
                if elem["pos"] == "名詞":
                    tmp_catted_noun.append(elem)
                    if i == (len(sentence) - 1) \
                            or sentence[i+1]["pos"] != "名詞":
                        if len(tmp_catted_noun) > 1:
                            catted_noun_list.append(''.join([elem["surface"] for elem in tmp_catted_noun]))
                            tmp_catted_noun = []
                else:
                    tmp_catted_noun = []
        return catted_noun_list
    #print(find_catted_nouns())

    # 35. 単語の出現頻度
    # 文章中に出現する単語とその出現頻度を求め，出現頻度の高い順に並べよ．
    def get_word_frequency_list(result_list):
        import collections
        c = collections.Counter([elem["base"] for sentence in result_list for elem in sentence])
        return c.most_common()
    word_count_list = get_word_frequency_list(result_list)

    # 36. 頻度上位10語Permalink
    # 出現頻度が高い10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ．
    import matplotlib.pyplot as plt
    import matplotlib
    # 日本語を表示させる。このフォントだとWindowsでしか動かないだろう。
    matplotlib.rc('font', family="Yu Gothic")
    word_list = [item[0] for item in word_count_list[:10]]
    count_list = [item[1] for item in word_count_list[:10]]
    #plt.bar(word_list, count_list)
    #plt.show()

    # 37. 「猫」と共起頻度の高い上位10語
    #「猫」とよく共起する（共起頻度が高い）10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ．
    def count_cooccurence(lld, tw):
        """同じ文内でターゲット単語と共起する単語の頻度をカウントする。

        lld: list of  # <- this represents a collection of sentences.
            list of   # <- this represents a sentence.
            {"surface": "xxx", "pos": "xxx", "pos1": "xxx", "base": "xxx"}
        tw: string
            ターゲットとする単語
        """
        coocurrence_list = []
            
        for ld in lld:
            if any(d["surface"] == tw for d in ld):
                coocurrence_list.extend([d["surface"] for d in ld if d["pos"] not in ["助動詞", "助詞"]])
        
        import collections
        return collections.Counter(coocurrence_list).most_common()

    cooccurrence_list = count_cooccurence(result_list, "猫")
                    
    import matplotlib.pyplot as plt
    import matplotlib
    # 日本語を表示させる。このフォントだとWindowsでしか動かないだろう。
    matplotlib.rc('font', family="Yu Gothic")
    plt.figure(figsize=(3, 1))
    n = 10
    word_list = [item[0] for item in cooccurrence_list[:n]]
    count_list = [item[1] for item in cooccurrence_list[:n]]
    plt.bar(word_list, count_list)
    plt.tight_layout() #これでxticksが見きれないようになるかと思ったけど効果なし
    #plt.show()

    # 38. ヒストグラム
    # 単語の出現頻度のヒストグラム（横軸に出現頻度，縦軸に出現頻度をとる単語の種類数を棒グラフで表したもの）を描け．
    def make_hist(lld, n=10):
        """x軸に出現回数、y軸に出現回数がxの単語の数のヒストグラムを表示する。

        lld: list of list of dict
        n: int
            how many bars to show
        """
        word_freq_list = get_word_frequency_list(lld)
        print(len([x for x in word_freq_list if x[1] == 1]))
        freq_list = [x[1] for x in word_freq_list]

        import numpy as np
        freq_list = np.array(freq_list)

        import plotly.express as px
        fig = px.histogram(x=freq_list, nbins=len(freq_list))
        fig.show()
    #make_hist(result_list)

    # 39. Zipfの法則
    # 単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．
    def make_loglog_graph(lld):
        word_freq_list = get_word_frequency_list(lld)
        import pandas as pd
        df = pd.DataFrame({
                "word": [x+1 for x in range(len(word_freq_list))],
                "freq": [x[1] for x in word_freq_list]
            })
        print(df.head())

        import plotly.express as px
        fig = px.bar(df, x='word', y='freq')
        fig.update_layout(xaxis_type="log", yaxis_type="log")
        fig.show()
    make_loglog_graph(result_list)






