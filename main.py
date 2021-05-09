import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
from constants import *
import pyjokes
import requests
import webbrowser
import os
from GoogleNews import GoogleNews

listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('voice', 'english-us')

def query(query_str):
    response = requests.get(query_str)

    if response.status_code == 200:
        return response.json()
    else:
        return ''

def talk(text):
    engine.say(text)
    engine.runAndWait()

def is_alexa(command):
    command = command.lower()
    if 'alexa' in command:
        command = command.replace('alexa', '')
    else:
        command = ""

def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print('listening')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            if is_alexa(command) != "":
                command = is_alexa(command)
                print(command)
    except:
        print("Do not recognize your mic connaction !!")
        pass
    return command


def run_alexa():
    command = take_command()

    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'wikipedia' in command:
        search = command.replace('wikipedia', '')
        info = wikipedia.summary(search, 1)
        print(info)
        talk(info)
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'weather' in command:
        api_key = weather_apikey
        city_name = ''
        if 'on' in command:
            city_index = command.split().index('on')
            city_name = command.split()[city_index +1]
        elif 'in' in command:
            city_index = command.split().index('in')
            city_name = command.split()[city_index + 1]
        query_string = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        response = query(query_string)

        descrition = response['weather'][0]['description']
        temp = ('%.0f' % (response['main']['temp'] -273))
        feels_like = ('%.0f' % (response['main']['feels_like'] -273))
        response_text = f'Air tempreture is {temp} feels like {feels_like} by {descrition} in {city_name}'
        print(response_text)
        talk(response_text)
    elif 'search' in command:
        command = command.replace('search', '')
        if 'youtube' in command:
            search_key = command.split('on')[0]
            search_on = command.split('on')[1]
            query_string = f'https://www.youtube.com/results?search_query={search_key}'
            talk(f'searching {search_key} on {search_on}')
            webbrowser.open(query_string)
        elif 'google' in command:
            search_key = command.split('on')[0]
            search_on = command.split('on')[1]
            query_string = f'https://www.google.com/search?q={search_key}'
            talk(f'searching {search_key} on {search_on}')
            webbrowser.open(query_string)
    elif 'open' in command:
        command = command.replace('open', '')
        if 'chrome' in command:
            talk(f'{command} opening')
            os.system('google-chrome')
        elif 'terminal' in command:
            talk(f'{command} opening')
            os.system('gnome-terminal')
    elif 'news' in command:
        google_news = GoogleNews(period='5d')
        google_news.search('TR')
        news = google_news.result()

        for new in news:
            title = new['title']
            date = new['date']
            desc = new['desc']
            link = new['link']
            new_text = f'{title} \n {date} \n {desc} \n'
            print('-' *150)
            print(new_text + '\n' + link )
            talk(new_text)
    else:
        talk("Please repeat again!")
        pass


while True:
    run_alexa()