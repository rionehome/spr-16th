from . import module_beep
from . import module_tuning
from . import module_pico

import usb.core
import usb.util
import time
import os
import csv
import math
from pocketsphinx import LiveSpeech, get_model_path


return_list=[]
question_dictionary = {}
model_path = get_model_path()
live_speech=None
dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)




file_path = os.path.abspath(__file__)
csv_path =  file_path.replace('module/module_QandAandA.py', 'dictionary/QandA/robocup_2019.csv')
dict_path = file_path.replace('module/module_QandAandA.py','dictionary/robocup_2019_sphinx.dict')
gram_path = file_path.replace('module/module_QandAandA.py','dictionary/robocup_2019_sphinx.gram')


with open(csv_path, 'r') as f:
    for line in csv.reader(f):
        question_dictionary.setdefault(str(line[0]), str(line[1]))


def angular():

    global question_dictionary
    global return_list
    global dev
    
    angular=0
    answer=0


    setup_live_speech(False,dict_path,gram_path,1e-10)
    Mic_tuning = module_tuning.Tuning(dev)


    while True:
        # if dev:
        for phrase in live_speech:
            cos=0
            for question_key in question_dictionary.keys():
                cos = calc_cos(str(phrase),question_key)
                if cos>0.8:
                    module_beep.beep("stop")
                    print("\n-------your question--------\n",str(phrase),"\n----------------------------\n", flush=True)
                    print("\n-----------answer-----------\n",question_dictionary[str(phrase)],"\n----------------------------\n", flush=True)
                    angular=Mic_tuning.direction
                    answer=question_dictionary[str(phrase)]
                    return_list = [angular, answer]
                    print("角度は {0} \n 答えは {1}".format(return_list[0], return_list[1], flush=True))
                    return return_list
                else:
                    continue



def setup_live_speech(lm, dict_path, jsgf_path, kws_threshold):
    

    global live_speech
    live_speech = LiveSpeech(lm=lm,
                             hmm=os.path.join(model_path, 'en-us'),
                             dic=dict_path,
                             jsgf=jsgf_path,
                             kws_threshold=kws_threshold)


def calc_cos(A,B):

    list_A = []
    list_B = []
    list_A = A.split(" ")
    list_B = B.split(" ")

    lengthA = math.sqrt(len(list_A))
    lengthB = math.sqrt(len(list_B))
    match = 0
    for a in list_A:
        if a in list_B:
            match += 1

    if (lengthA != 0 and lengthB != 0):
        cos = match/(lengthB*lengthA)
    else:cos = match/100

    return cos


if __name__ == "__main__":
    angular()
