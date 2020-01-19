import os
import datetime
from . import module_pico
from . import module_beep


# logを作るファイルのパスを定義
file_path = os.path.abspath(__file__)
log_path = file_path.replace('module/module_count_people.py', 'speak_log/{}.txt').format(str(datetime.datetime.now()))

'''
# 人数のみのカウント
def count_people(number): 

    ###############
    #
    # use this module to speak number of people
    #
    # param >> number: speak this number
    #
    # return >> 1
    #
    ###############

    person_number = 'There are {} people'.format(int(number))
    module_beep.beep('stop')
    print(person_number)
    module_pico.speak(person_number)

    # logの作成
    log = open(log_path, 'a')
    log.write(str(datetime.datetime.now()) + " [person recognition]:  " + person_number + "\n")
    log.close()

    return 1

'''
# 男女人数のカウント
def count_people(string): 

    ###############
    #
    # use this module to speak number of women and man
    #
    # param >> string: 女4男7の場合 4|7 という文字列
    #
    # return >> 1
    #
    ###############

    string = string.split('|')
    person_string = 'There are {} people, the number of women is {}, the number of men is {}.'.format(int(string[0])+int(string[1]), string[0], string[1])
    module_beep.beep('stop')
    print(person_string)
    module_pico.speak(person_string)

    # logの作成
    log = open(log_path, 'a')
    log.write(str(datetime.datetime.now()) + " [person recognition]:  " + person_string + "\n")
    log.close()

    return 1


if __name__ == '__main__':
    # 男女人数のカウント
    number = input("number of people [woman|man]")
    count_people(number)