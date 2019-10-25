# テキストファイルから単語辞書を作る際に使う

import nltk, os
from nltk.corpus import treebank, wordnet

txt_path = os.path.dirname(os.path.abspath(__file__)) # このファイルのある絶対パス

q_list = []
text = []
file_name = input("ファイル名を入力してください：")
with open(txt_path + '/../dictionary/QandA/' + file_name) as f: # ファイルの入っているディレクトリの絶対パス
    qa_list = f.readlines()
    for qa in qa_list: # 1文ずつ質問文を処理
        qa = qa.split(',')
        q_sentences = qa[0].split(" ")
        # print(q_sentences)
        for w in q_sentences: # 質問文の単語を追加
            q_list.append(w)
    for w in q_list:
        if w in text:
            pass
        else:
            text.append(w)
    # print(text)
    for w in text:
        print(w)