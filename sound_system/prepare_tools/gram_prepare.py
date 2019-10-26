# テキストファイルから文法辞書を作る際に使う

import os

txt_path = os.path.dirname(os.path.abspath(__file__)) # このファイルのある絶対パス
q_list = []

file_name = input("ファイル名を入力してください：")
with open(txt_path + '/../dictionary/QandA/' + file_name) as f: # ファイルの入っているディレクトリの相対パス
    qa_list = f.readlines()
    for qa in qa_list:
        qa = qa.split(",")
        q_list.append(qa[0])
    for w in q_list:
        print(w + " | ", end="")

