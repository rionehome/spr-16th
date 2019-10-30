from module import module_count
from module import module_count_people
from module import module_angular
# from module import module_QandA
from module import module_pico
from module import module_beep


# モジュール実行部分
command = []

message = input('Please input message : ')
command.append("Command:" + str(message))

while(True):
    # 10秒カウント
    if 'count' == command[0].replace('Command:', ''):
        if module_count.count() == 1:
            break
    # 人数発話
    if 'count_people' == command[0].replace('Command:', ''):
        if module_count_people.count_people(str(message)) == 1: # ここの引数に人数を入れる
            break
        
    # QandA開始
    if 'QandA' == command[0].replace('Command:', ''):
        if module_QandA.QandA(5) == 1:
            break

    # 音限定位
    if 'augular' == command[0].replace('Command:', ''):
        if module_angular.augular() == 1:
            break