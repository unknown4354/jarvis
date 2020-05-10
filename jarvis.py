import re
from urllib import urlopen
import urllib2
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
from bs4 import BeautifulSoup as soup
import subprocess
from pyowm import OWM
import vlc
import youtube_dl
import json
import requests
from urllib2 import urlopen


engine = pyttsx3.init()
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice', voices[0].id)


def takecommand() :
    r = sr.Recognizer()
    with sr.Microphone() as source :
        print ("listening...")
        r.pause_threshold = 1
        r.energy_threshold = 350
        audio = r.listen(source)

    try :
        print ("Recognizing...")
        query = r.recognize_google(audio)
        print ("user said", query)

    except Exception as e :
        # print (e)
        print ("say that again please...")
        return "none"
    return query


def speak(audio) :
    engine.say(audio)
    engine.runAndWait()


def WishMe() :
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12 :
        speak("Good morning!")
    elif hour >= 12 and hour < 18 :
        speak("Good afternoon!")
    else :
        speak("Good evening!")

    speak("Hello sir I am Jarvis. Your personal assistant. How may I help you")


def sendEmail(to, content) :
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('strss.busters@gmail.com', 'swagismystyle4354000')
    server.sendmail('singhaals@gmail.com', to, content)
    server.close()


if __name__ == '__main__' :
    WishMe()
    while True :
        query = takecommand().lower()

        if 'search about' in query :
            speak("searching...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("Got it")
            print (results)
            speak(results)

        elif 'play music' in query :
            music_dir = 'New folder'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[9]))

        elif 'the time' in query :
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(strTime)
            speak("Sir, The time is" + strTime)

        elif 'email to me' in query :
            try :
                speak("What should I say?")
                content = takecommand()
                to = "singhaals@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e :
                print(e)
                speak("Sorry sir, could not send the email")

        elif 'open' in query :
            reg_ex = re.search('open (.+)', query)
            if reg_ex :
                domain = reg_ex.group(1)
                print(domain)
                url = 'https://www.' + domain + '.com'
                webbrowser.open(url)
                speak("The website you have requested has been opened for you Sir.")
            else :
                pass

        elif 'current weather' in query :
            reg_ex = re.search('current weather in (.*)', query)
            if reg_ex :
                city = reg_ex.group(1)
                owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
                obs = owm.weather_at_place(city)
                w = obs.get_weather()
                k = w.get_status()
                x = w.get_temperature(unit='celsius')
                speak(
                    'Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (
                        city, k, x['temp_max'], x['temp_min']))


        elif 'bye' in query:
            speak("Goodbye Sir. Have a great day")
            exit()

