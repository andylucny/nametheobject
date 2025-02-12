import pyttsx3
import os
from agentspace import space
import time

space['language'] = 'sk'
    
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    if len(voices) == 0:
        import platform 
        if platform.system() == "Windows":
            print("run Registy Editor (regedit) and")
            print("export content of Computer\\HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech_OneCore\\Voices\\Tokens into my.reg file" )
            print("rewrite paths in file to Computer\\HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens")
            print("import the my.reg file")
        else:
            print("install:")
            print("$ sudo apt-get install espeak -y")
        os._exit(0)
        
    voice_names = [ voice.name for voice in voices ] 
    #print(voice_names)
    
    if space(default='en')['language'] == 'sk':
        try:
            speaker = voice_names.index('Microsoft Filip - Slovak (Slovakia)')
        except ValueError:
            try:
                speaker = voice_names.index('Vocalizer Expressive Laura Harpo 22kHz')
            except ValueError:
                speaker = 0
    
    else:
        try:
            speaker = voice_names.index('Microsoft Zira Desktop - English (United States)')
        except ValueError:
            try:
                speaker = voice_names.index('Microsoft David Desktop - English (United States)')
            except ValueError:
                try:
                    speaker = voice_names.index('english-us')
                except ValueError:
                    speaker = 0
    
    #print('speaker:',speaker, voices[speaker].name)
    engine.setProperty('voice', voices[speaker].id)
    space['speaking'] = True
    engine.say(text)
    print('speaking on <'+text+'>')
    engine.runAndWait()
    print('speaking off')
    time.sleep(0.5)
    space['speaking'] = False

if __name__ == "__main__":
    speak('Na holi sa pasie ovca.')
    print('done')
