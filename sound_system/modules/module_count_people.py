from . import module_pico.py
from . import module_pico.py
def count_people(a | b):
    number = number.split('|')
    person_number = 'There are {} people, the number of woman is {}, the number of men is {}.'.format(int(number[0])+int(number[1]), number[0], number[1])
    module_beep.beep('stop')
    print(person_number)
    module_pico.speak(person_number)
    return 1

if __name__ == '__main__':
    w = int(input("number of woman :"))
    m = int(input("number of man :"))
    count_people(w, m)    
