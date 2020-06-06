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

        def get_pos(self):
            return self.__pos
        
        def get_surface(self):
            return self.__surface

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
            morph.__surface = xml_tok_element.text
            morph.__base = tok_attr_list[6] if size > 6 else ""
            morph.__pos = tok_attr_list[0] if size > 0 else ""
            morph.__pos1 = tok_attr_list[1] if size > 1 else ""
            return morph
    xml_path = "neko.txt.cabocha"
    llm = Morph.load_from_xml(xml_path)

    #pprint.pprint([vars(m) for m in llm[2]])

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
        
        def get_text(self):
            return "".join([ m.get_surface() for m in self.get_morphs()])

        def get_morphs(self):
            import copy
            return copy.deepcopy(self.__morph_list)

        def __repr__(self):
            return str(vars(self))
        

    llchunk = Chunk.load_from_xml(xml_path)
    #pprint.pprint(llchunk[7])

    # 42. 係り元と係り先の文節の表示
    def print_chunk_depencency(sentence_chunks):
        """print dependency between chunks in a sentence.

        premise: parameter chunks consist of one sentence.

        parameter:
            sentence_chunks: list of chunk
        """

        for chunk in sentence_chunks:
            if chunk.get_link() == -1:
                continue
            src = chunk
            dst = sentence_chunks[chunk.get_link()]

            # src、dstどちらかが記号のみで構成されていたら表示しない。
            has_only_signs = lambda chunk: len(chunk.get_morphs()) == len([morph for morph in chunk.get_morphs() if morph.get_pos() == "記号"])
            if has_only_signs(src) or has_only_signs(dst):
                continue

            get_text = lambda chunk: "".join([morph.get_surface() for morph in chunk.get_morphs()])
            src_text = get_text(src)
            dst_text = get_text(dst)

            print(src_text + "\t" + dst_text)

    #for sentence in llchunk:
    #    print_chunk_depencency(sentence)


    # 43. 名詞を含む文節が動詞を含む文節に係るものを抽出
    def print_noun2verb_dependency(sentence_chunks):
        for chunk in sentence_chunks:
            if chunk.get_link() == -1:
                continue
            src = chunk
            dst = sentence_chunks[chunk.get_link()]

            # srcに動詞があって、dstに名詞があるときのみ表示する
            has_at_least_one = lambda chunk, pos: any([morph.get_pos() == pos for morph in chunk.get_morphs()])
            if not has_at_least_one(src, "名詞") or not has_at_least_one(dst, "動詞"):
                continue

            get_text = lambda chunk: "".join([morph.get_surface() for morph in chunk.get_morphs() if morph.get_pos() != "記号"])
            src_text = get_text(src)
            dst_text = get_text(dst)

            print(src_text + "\t" + dst_text)

    #for sentence in llchunk:
        #print_noun2verb_dependency(sentence)

    # 44. 係り受け木の可視化
    import pydot
    #from IPython.display import Image, display

    graph = pydot.Dot(graph_type='digraph')
    sentence = llchunk[3]
    for chunk in sentence:
        dst = chunk.get_link()
        if dst == -1:
            continue
        dst_chunk_text = sentence[dst].get_text()
        src_chunk_text = chunk.get_text()
        e = pydot.Edge( src_chunk_text, dst_chunk_text )
        graph.add_edge(e)
    # jupyter notebook 上であれば以下の2行でファイル保存なしに画像を表示できるらしい。今回はやらないが。
    # plt = Image(graph.create_png())
    # display(plt)

    # なぜか知らんがencodingをしていしないとだめだ
    graph.write_svg("nlp100_problem44.svg", encoding='utf-8')
