import time
import module_pico

# countdown
def count():
    ###############
    #
    # use this module to countdown
    #
    # param >> None
    #
    # return >> None
    #
    ###############

    sentence = "I will start riddle game"
    module_pico.speak(sentence)
    time_start = time.perf_counter()
    for i in range(1,11):
        while 1:
            time_end = time.perf_counter()
            time_temp = time_end - time_start
            if int(time_temp) == i:
                #print(time_temp)
                module_pico.speak(str(i))
                break
    print("経過時間："+str(time_temp))
    return 1

if __name__ == '__main__':
    count()
