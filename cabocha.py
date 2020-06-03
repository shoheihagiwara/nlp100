import xml.etree.ElementTree as ET
import pprint
import os
import csv


if __name__ == "__main__":

    def from_cabocha_xml_to_complete_xml(path):
        with open(path, encoding='utf-8') as f:
            file_content = f.read()
            complete_xml_string = '<?xml version="1.0" encoding="UTF-8" ?>' + \
                os.linesep + '<neko>' + os.linesep + file_content + '</neko>' + os.linesep
            return complete_xml_string

    # 40. 係り受け解析結果の読み込み（形態素）
    # 形態素を表すクラスMorphを実装せよ．
    # このクラスは表層形（surface），基本形（base），
    # 品詞（pos），品詞細分類1（pos1）を
    # メンバ変数に持つこととする．
    # さらに，CaboChaの解析結果（neko.txt.cabocha）を読み込み，
    # 各文をMorphオブジェクトのリストとして表現し，3文目の形態素列を表示せよ．

    class Morph:

        def __repr__(self):
            return str(vars(self))

        @classmethod
        def load_from_xml(cls, path):
            """read XML file and return list of list of Morphs.

            return:
                list        # this is document
                of list     # this is sentence
                of Morph.
            """

            root = ET.fromstring(from_cabocha_xml_to_complete_xml(path))

            list_of_list_of_morph = []
            for sentence in root:
                list_for_sentence = []
                for chunk in sentence:
                    for tok in chunk:
                        list_for_sentence.append(cls.from_xml_tok_elemet(tok))
                list_of_list_of_morph.append(list_for_sentence)
            return list_of_list_of_morph

        @classmethod
        def from_xml_tok_elemet(cls, xml_tok_element):
            morph = Morph()
            tok_attr_list = list(csv.reader([xml_tok_element.attrib["feature"]]))[0]
            size = len(tok_attr_list)
            morph.surface = xml_tok_element.text
            morph.base = tok_attr_list[6] if size > 6 else ""
            morph.pos = tok_attr_list[0] if size > 0 else ""
            morph.pos1 = tok_attr_list[1] if size > 1 else ""
            return morph
    xml_path = "neko.txt.cabocha"
    llm = Morph.load_from_xml(xml_path)

    pprint.pprint([vars(m) for m in llm[2]])

    # 41. 係り受け解析結果の読み込み（文節・係り受け）
    # 40に加えて，文節を表すクラスChunkを実装せよ．
    # このクラスは形態素（Morphオブジェクト）のリスト（morphs），
    # 係り先文節インデックス番号（dst），
    # 係り元文節インデックス番号のリスト（srcs）をメンバ変数に持つこととする．
    # さらに，入力テキストのCaboChaの解析結果を読み込み，
    # １文をChunkオブジェクトのリストとして表現し，
    # 8文目の文節の文字列と係り先を表示せよ．
    # 第5章の残りの問題では，ここで作ったプログラムを活用せよ．
    class Chunk:

        def __init__(self):
            self.__morph_list = []
            self.__link = None
            self.__srcs = []

        
        @classmethod
        def load_from_xml(cls, path):

            sentence_list = []
            
            # cabochaで出したXML形式はXML宣言とルートノードが存在せず不正なのでそのままでは読み込めない。
            # 足りない情報を追加してから読み込む。
            complete_xml_string = from_cabocha_xml_to_complete_xml(path)
            root = ET.fromstring(complete_xml_string)

            for sentence in list(root):
                sentence_chunk_list = []
                for chunk_elemet in sentence:

                    chunk = Chunk()

                    # リストにMorphを追加
                    for tok in chunk_elemet:
                        chunk.add_morph(Morph.from_xml_tok_elemet(tok))

                    # linkを追加
                    chunk.set_link(int(chunk_elemet.attrib['link']))

                    sentence_chunk_list.append(chunk)
                
                # srcsを追加
                for i, chunk in enumerate(sentence_chunk_list):
                    link = chunk.get_link()
                    if link != -1:
                        sentence_chunk_list[link].add_src(i)

                sentence_list.append(sentence_chunk_list)
            
            return sentence_list


        def add_morph(self, morph):
            self.__morph_list.append(morph)

        def set_link(self, link):
            self.__link = link

        def add_src(self, src):
            self.__srcs.append(src)

        def get_link(self):
            return self.__link

        def __repr__(self):
            return str(vars(self))

    llchunk = Chunk.load_from_xml(xml_path)
    pprint.pprint(llchunk[7])


