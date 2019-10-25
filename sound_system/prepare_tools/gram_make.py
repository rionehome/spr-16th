#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 標準入力からPocket sphinxの文法辞書と単語辞書を作成するプログラム
import os

dictionary_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dictionary')
name = input("作成する辞書の名前を入力してください:")

PATH1 = os.path.join(dictionary_directory_path, 'cmudict-en-us.dict')  # 全単語が入っている単語辞書の絶対パス
PATH2 = os.path.join(dictionary_directory_path, '{}_sphinx.dict').format(name)  # 作りたい単語辞書の絶対パス
PATH3 = os.path.join(dictionary_directory_path, '{}_sphinx.gram').format(name)  # 作りたい文法辞書の絶対パス

if os.path.exists(PATH2) or os.path.exists(PATH3):
    print("同じファイル名の辞書が存在します。")
    print("終了")
    print("========================================")
else:
    print('文章を入力してください + Enter')
    print('(終了する場合はCtrl-C)')
    print("========================================")
    sentence_list = []  # 標準入力した文を格納するリスト
    try:
        while 1:
            sentence = input()  # ファイルに追加する文章を標準入力
            sentence = sentence.rstrip()  # 改行コード削除
            sentence_list.append(sentence)

    except KeyboardInterrupt:
        word_list = []  # 文の単語を格納するリスト
        for s in sentence_list:
            words_list = s.split(' ')
            for w in words_list:
                word_list.append(w)

        word_list = list(set(word_list))  # 重複している単語を削除

        # 単語が入っている単語辞書の単語をall_words_listに格納
        with open(PATH1) as f1:
            lines1 = f1.readlines()
            all_words_list = []
            for l1 in lines1:
                all_words_list.append(l1.split(' ')[0])

        no_words_list = []  # 辞書になかった単語を格納する
        for w in word_list:
            if w not in all_words_list:
                no_words_list.append(w)

        no_sentence_list = []
        # 辞書になかった単語が含まれている文をno_sentence_listに格納、それ以外をwrite_sentence_listに格納
        if no_words_list:
            write_sentence_list = []
            for s in sentence_list:
                no_sentence_flag = False
                for n in no_words_list:
                    if n in s:
                        no_sentence_flag = True
                if no_sentence_flag:
                    no_sentence_list.append(s)
                else:
                    write_sentence_list.append(s)
        else:
            write_sentence_list = sentence_list

        if write_sentence_list:
            # 文法辞書に書き込み
            with open(PATH3, "a") as f3:
                f3.write("#JSGF V1.0;\n")
                f3.write("grammar {}_sphinx;\n".format(name))
                f3.write("public <rule> = <command>;\n")
                f3.write("<command> = ")
                write_sentence_list = sorted(write_sentence_list)  # ソート
                for a in range(len(write_sentence_list) - 1):
                    f3.write(write_sentence_list[a] + " | ")
                f3.write(write_sentence_list[len(write_sentence_list) - 1])
                f3.write(";")

            # 単語辞書に書き込み
            with open(PATH2, "a") as f2:
                write_word_list = []
                for ws in write_sentence_list:
                    w_list = ws.split(' ')
                    for word in w_list:
                        write_word_list.append(word)
                write_word_list = list(set(write_word_list))
                write_word_list = sorted(write_word_list)  # ソート

                for ww in write_word_list:
                    ww_index = all_words_list.index(ww)
                    f2.write(lines1[ww_index])  # 単語と音素記号のセットの一行を書き込む
                    # 音素が複数ある場合
                    if ww + '(2)' in all_words_list:
                        ww_index = all_words_list.index(ww + '(2)')
                        f2.write(lines1[ww_index])
                    elif ww + '(3)' in all_words_list:
                        ww_index = all_words_list.index(ww + '(3)')
                        f2.write(lines1[ww_index])

        if no_sentence_list:
            print("追加できなかった文章は")
            for ns in no_sentence_list:
                print(ns)

        if no_words_list:
            print("見つからなかった単語は")
            for nw in no_words_list:
                print(nw)