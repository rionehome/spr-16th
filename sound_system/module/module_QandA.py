import os
import datetime
import math
import csv
import numpy as np
from pocketsphinx import LiveSpeech, get_model_path

import module_pico
import module_beep


print("最初開始")
file_path = os.path.abspath(__file__)
question_dictionary = {}
noise_words = {}
counter = 0

#Difine path
spr_dict_path = file_path.replace(
    'module/module_QandA.py', 'dictionary/robocup_2019_sphinx.dict')
spr_gram_path = file_path.replace(
    'module/module_QandA.py', 'dictionary/robocup_2019_sphinx.gram')
csv_path = file_path.replace(
    'module/module_QandA.py', 'dictionary/QandA/robocup_2019.csv')
log_path = file_path.replace('module/module_QandA.py', 'speak_log/{}.txt').format(str(datetime.datetime.now()))
model_path = get_model_path()

#Male a dictionary from txt file
with open(csv_path, 'r') as f:
    for line in csv.reader(f):
        question_dictionary.setdefault(str(line[0]), str(line[1]))

def QandA(number):

    ###############
    #
    # use this module at spr section >> | Q&A
    #
    # param >> number: | how many times do you want to do Q&A
    #
    # return >> 1
    #
    ###############

    global counter
    global question_dictionary
    global noise_words
    global live_speech

    #Noise list
    #noise_words = read_noise_word(spr_gram_path)

    #If I have a question which I can answer, count 1
    while counter < number:
        print("- "+str(counter+1)+" cycle!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", flush=True)
        print("\n[*] LISTENING ...", flush=True)
        #Setup live_speech
        setup_live_speech(False, spr_dict_path, spr_gram_path)
        module_beep.beep("start")
        for question in live_speech:
            print(question)
            if str(question) not in noise_words:
                max = 0
                correct_question = ""
                for question_key in question_dictionary.keys():
                    cos = calc_cos(str(question), question_key)
                    if cos > max:
                        max = cos
                        correct_question = question_key
                        #print(max)
                question = correct_question
                if max > 0.8:
                    if str(question) == "I want you to answer with turning":
                        pause()
                        module_beep.beep("stop")
                        print("\n----------------------------\n", str(question), "\n----------------------------\n")
                        module_pico.speak(question_dictionary[str(question)])


                    #Detect yes or no 

                    else:
                        pause()
                        module_beep.beep("stop")
                        print("\n-------your question--------\n",str(question),"\n----------------------------\n")
                        print("\n-----------answer-----------\n",question_dictionary[str(question)],"\n----------------------------\n")
                        module_pico.speak(question_dictionary[str(question)])

                        # logの作成
                        log = open(log_path, 'a')
                        log.write(str(datetime.datetime.now()) + " [question]:  " + str(question) + "\n")
                        log.write(str(datetime.datetime.now()) + " [answer]:  " + question_dictionary[str(question)] + "\n")

                        print("\n\n!!!!!!!!!!", flush=True)
                        counter += 1
                        break
                elif 0 < max <= 0.8:
                    pause()
                    module_beep.beep("stop")
                    answer = "Sorry I don't have answer." 
                    print("\n-----------answer-----------\n",answer,"\n----------------------------\n")
                    module_pico.speak(answer)
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    counter += 1
                    break

            #noise
            else:
                print(".*._noise_.*.")
                print("\n[*] LISTENING ...")
                pass
    counter = 0
    return 1

def pause():

    ###############
    #
    # use this module to stop lecognition
    #
    # param >> None
    #
    # return >> None
    #
    ###############

    global live_speech
    live_speech = LiveSpeech(no_search = True)

'''def read_noise_word(gram):

    ###############
    #
    # use this module to put noise to list
    #
    # param >> None
    #
    # return >> words: list in noises
    #
    ###############

    words = []
    with open(gram) as f:
        for line in f.readlines():
            if "<noise>" not in line:
                continue
            if "<rule>" in line:
                continue
            line = line.replace("<noise>", "").replace(" = ", "").replace("\n", "").replace(";", "")
            words = line.split(" | ")
    
    return words'''

def setup_live_speech(lm, dict_path, jsgf_path):

    ###############
    #
    # use this module to set live speech parameter
    #
    # param >> lm: False >> means useing own dict and gram
    # param >> dict_path: ~.dict file's path
    # param >> jsgf_path: ~.gram file's path
    # param >> kws_threshold: mean's confidence (1e-○)
    #
    # return >> None
    #
    ###############

    global live_speech
    live_speech = LiveSpeech(lm = lm,
                             hmm=os.path.join(model_path, 'en-us'),
                             dic = dict_path,
                             jsgf = jsgf_path)

def calc_cos(A, B):

    ###############
    #
    # use this module to define degree of similarity
    #
    # param >> A: first sentence
    # param >> B: second sentence
    #
    # return >> cos: degree of similarity
    #
    ###############

    list_A = []
    list_B = []
    list_A = A.split(" ")
    list_B = B.split(" ")

    lengthA = np.sqrt(len(list_A))
    lengthB = np.sqrt(len(list_B))
    math = 0
    for a in list_A:
        if a in list_B:
            math += 1

    if (lengthA != 0 and lengthB != 0):
        cos = math / (lengthA * lengthB)
    else:
        cos = math / 100

    return cos

if __name__ == '__main__':
    QandA(5)
