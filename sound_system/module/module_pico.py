import os
import subprocess

# Define path
file_path = os.path.abspath(__file__)
speech_wave = file_path.replace(
            'module/module_pico.py', 'beep/speech.wav')

# Speak content
def speak(content):

    ###############
    #
    # use this module to speak param
    #
    # param >> content: speak this content
    #
    # return >> None
    #
    ###############

    print("[*] SPEAK : {0}".format(content),flush=True)
    #subprocess.call('amixer sset Master 90% -q --quiet', shell=True)  # 大声
    subprocess.call(['pico2wave', '-w={}'.format(speech_wave), content])
    subprocess.call('aplay -q --quiet {}'.format(speech_wave), shell=True)
    #subprocess.call('amixer sset Master 75% -q --quiet', shell=True)  # 声の大きさを戻す

if __name__ == '__main__':
    content = input("Please input content : ")
    speak(content)