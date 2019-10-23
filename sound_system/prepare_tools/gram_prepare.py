q_list = []
file_name = input("ファイル名を入力してください：")
with open('/home/kohei/spr_practice/QA_text/' + file_name) as f: # ファイルの入っているディレクトリの絶対パス
    qa_list = f.readlines()
    for qa in qa_list: # 1文ずつ質問文を処理
        qa = qa.split(",")
        q_list.append(qa[0])
    for w in q_list:
        print(w + " | ", end="")

