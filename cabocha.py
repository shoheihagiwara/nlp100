if __name__ == "__main__":
    # 40. 係り受け解析結果の読み込み（形態素）
    # 形態素を表すクラスMorphを実装せよ．
    # このクラスは表層形（surface），基本形（base），
    # 品詞（pos），品詞細分類1（pos1）を
    # メンバ変数に持つこととする．
    # さらに，CaboChaの解析結果（neko.txt.cabocha）を読み込み，
    # 各文をMorphオブジェクトのリストとして表現し，3文目の形態素列を表示せよ．
    import xml.etree.ElementTree as ET
    import pprint

    class Morph:

        @classmethod
        def load_from_xml(cls, path):
            """read XML file and return list of list of Morphs.

            return:
                list        # this is document
                of list     # this is sentence
                of Morph.
            """

            tree = ET.parse(path)
            root = tree.getroot()

            list_of_list_of_morph = []
            for sentence in root:
                list_for_sentence = []
                for chunk in sentence:
                    for tok in chunk:
                        morph = Morph()
                        import csv
                        tok_attr_list = list(csv.reader([tok.attrib["feature"]]))[0]
                        size = len(tok_attr_list)
                        morph.surface = tok.text
                        morph.base = tok_attr_list[6] if size > 6 else ""
                        morph.pos = tok_attr_list[0] if size > 0 else ""
                        morph.pos1 = tok_attr_list[1] if size > 1 else ""
                        list_for_sentence.append(morph)
                list_of_list_of_morph.append(list_for_sentence)
            return list_of_list_of_morph
    llm = Morph.load_from_xml("neko.txt.cabocha")

    pprint.pprint([vars(m) for m in llm[2]])

