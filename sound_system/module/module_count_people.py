from . import module_pico
from . import module_beep


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
    person_string = 'There are {} people, the string of woman is {}, the string of men is {}.'.format(int(string[0])+int(string[1]), string[0], string[1])
    module_beep.beep('stop')
    print(person_string)
    module_pico.speak(person_string)
    return 1
'''

if __name__ == '__main__':
    # 人数のみのカウント
    number = input("number of people :")
    count_people(number)

'''
    # 男女人数のカウント
    number = input("number of people [woman|man]")
    count_people(number)    
'''
