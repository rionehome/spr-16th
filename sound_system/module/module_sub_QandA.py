import os
import csv
from pocketsphinx import LiveSpeech, get_model_path
from time import sleep

from . import module_pico
from . import module_beep

def QandA(number):

    #Difine path
    file_path = os.path.abspath(__file__)
    dic_path = file_path.replace(
        'module/module_sub_QandA.py', 'dictionary/robocup_2019_sphinx.dict')
    gram_path = file_path.replace(
        'module/module_sub_QandA.py', 'dictionary/robocup_2019_sphinx.gram')
    csv_path = file_path.replace(
        'module/module_sub_QandA.py', 'dictionary/QandA/robocup_2019.csv')
    model_path = get_model_path()


    # setting
    qa_dictionary = {}
    counter = 0


    # setting pocketsphinx
    Live_speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=os.path.join(model_path, 'en-us'),
        lm=False,
        dic= dic_path,
        jsgf= gram_path
    )


    #Make qa_dictionary from csv file
    with open(csv_path, 'r') as f:
        for line in csv.reader(f):
            qa_dictionary.setdefault(str(line[0]), str(line[1]))

    
    # start riddle game
    while counter < number:
        print("- "+str(counter+1)+" cycle -")
        print("\n[*] LISTENING ...")
        module_beep.beep("start")  # 音声認識開始の合図
        # sleep(1.0)
        for question in Live_speech:
            print(question)
            if str(question) in qa_dictionary.keys():
                question = str(question)
                # print(question)
                #Live_speech = LiveSpeech(no_search = True)
                module_beep.beep("stop")  # 音声認識終了の合図
                print("\n----------------------------\n", question, "\n----------------------------\n")
                module_pico.speak(qa_dictionary[question])
                break
        counter += 1
    return 1

if __name__ == '__main__':
    QandA(5)