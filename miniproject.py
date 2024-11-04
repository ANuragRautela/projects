import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import time
import subprocess
import cv2 
import wolframalpha
import json
import requests
import pywhatkit

print('Loading your AI personal assistant')

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id',)
engine.setProperty('rate',150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

speak("Loading your AI personal assistant")
wishMe()

def open_file_or_application(application_name):
    try:
        result = subprocess.run(['where', application_name], capture_output=True, text=True)
        executable_path = result.stdout.strip()

        if executable_path:
            os.startfile(executable_path)
            speak(f"Opening {application_name}")
            print(f"Opening {application_name}")
        else:
            speak(f"Sorry, I couldn't find {application_name}.")
            print(f"Could not find {application_name}.")
    except Exception as e:
        speak(f"Error opening {application_name}: {e}")
        print(f"Error opening {application_name}: {e}")

if __name__=='__main__':
    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()
        if statement==0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop"  in statement or "bye" in  statement:
            speak('your personal assistant  is shutting down,Good bye')
            print('your personal assistant  is shutting down,Good bye')
            break

        #if 'open youtube' in statement:
            #webbrowser.open_new_tab("https://www.youtube.com")
            #speak("youtube is open now")
            #time.sleep(5)

        elif 'youtube search' in statement:
            query = statement.lower().replace('open', '').replace('youtube', '').strip()
            webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={query}")
            speak(f"Searching for {query} on YouTube.")
            time.sleep(5)    

        #elif 'open google' in statement:
            #webbrowser.open_new_tab("https://www.google.com")
            #speak("Google chrome is open now")
            #time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            print(f"opening the {statement}\n")
            time.sleep(5)

        elif "weather" in statement:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name=takeCommand()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                speak(" City Not Found ")
                print(" City Not Found ")

        elif 'time' in statement:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am asstiant version 1 point O your persoanl assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome,gmail ,predict time,take a photo,predict weather' 
                  'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!')


        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by Anurag")
            print("I was built by Anurag")
            
        elif 'news' in statement:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            try:
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                cv2.imwrite("img.jpg", frame)
                cap.release()
                speak("Photo captured successfully.")
            except Exception as e:
                print(f"Error capturing image: {e}")

        elif 'search'  in statement or 'Google search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'ask' in statement:
            speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question=takeCommand()
            app_id="R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

        elif "log off" in statement or "sign out" in statement:
            speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])
        
        elif "play" in statement or "play music" in statement or "playmusic" in statement:
            speak("Sure, playing music for you. Please say the name of the song.")
            song_name = takeCommand()
            speak(f"Searching for {song_name} on YouTube.")
            try:
                pywhatkit.playonyt(song_name)
            except Exception as e:
                speak("Sorry, I couldn't find the song. Please try again.")
        
        #elif 'open' in statement:
            #speak("Sure, please provide the path of the file or application.")
            #file_path = takeCommand()
            #open_file_or_application(file_path)
        
        elif 'website' in statement or 'go to website' in statement:
            speak("Sure, please tell me the website URL.")
            website_url = takeCommand()
    
            if 'http' not in website_url:
                website_url = 'http://' + website_url

            webbrowser.open_new_tab(website_url)
            speak(f"Opening website {website_url}")
            print(f"Opening website {website_url}")
        
        elif "record a video" in statement or 'video recording' in statement:
            try:
                cap = cv2.VideoCapture(0)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, 30)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))
                start_time = time.time()
                while time.time() - start_time < 30:
                    ret, frame = cap.read()
                    out.write(frame)          
                cap.release()
                out.release()
                speak("Video recording completed.")
            except Exception as e:
                print(f"Error recording video: {e}")
time.sleep(3)
