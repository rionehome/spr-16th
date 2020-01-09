from . import infer

def recognizer():
    i = 0
    man = 0
    woman = 0
    inf = infer.CNN()

    while i<3:
        pwd = './' + str(i) + '.jpg'
        pred = inf.predict(pwd) 
        print('man：%5.3f  woman：%5.3f' % (pred[0], pred[1]))
        if pred[0] > 0.5:
            man += 1
        else:
            woman += 1
        i += 1
    counter = str(woman) + '|' + str(man)
    print("woman | man " + counter)

    return str(counter)

if __name__=='__main__':
    recognizer()
