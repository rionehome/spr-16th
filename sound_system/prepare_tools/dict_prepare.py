import nltk
from nltk.corpus import treebank, wordnet

q_list = []
text = []
file_name = input("ファイル名を入力してください：")
with open('/home/kohei/spr_practice/QA_text/' + file_name) as f: # ファイルの入っているディレクトリの絶対パス
    qa_list = f.readlines()
    for qa in qa_list: # 1文ずつ質問文を処理
        qa = qa.split(',')
        """q_sentences = nltk.word_tokenize(qa[0]) # 質問文のみを分かち書き"""
        q_sentences = qa[0].split(" ")
        print(q_sentences)
        for w in q_sentences: # 質問文の単語を追加
            q_list.append(w)
    for w in q_list:
        if w in text:
            pass
        else:
            text.append(w)
    print(text)
    for w in text:
        print(w)