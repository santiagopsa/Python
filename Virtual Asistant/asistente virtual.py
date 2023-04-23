import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# Listen mic and return audio

def transform_audio_to_text():

    # Save recognizer in a variable
    r = sr.Recognizer()

    # Microphone config
    with sr.Microphone() as origin:

        # time waiting
        r.pause_threshold = 0.2

        # report you can start recording
        print('You can talk now')

        # record audio
        audio = r.listen(origin)

        try:
            #buscar en google
            request= r.recognize_google(audio, language='es-ar')
            # make sure it worked

            print('You said: '+request)

            return request

        except sr.UnknownValueError:
            print('Ups, I didnt get it')

            return 'Still waiting'

        except sr.RequestError:
            print('Ups no service')
            return 'Still waiting'

        except:
            print('Something happened')
            return 'Still waiting'

# function so the assitant can be heard
def speak(message):
    # turn on pyttsx3
    engine = pyttsx3.init()

    #speak message
    engine.say(message)
    engine.runAndWait()


speak(transform_audio_to_text())

