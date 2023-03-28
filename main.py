#! /usr/bin/env /usr/bin/python3

import json
import os
import random
import time
import speech_recognition as sr
from user_recog import record_audio, recog_user, prepare_model
from dotenv import load_dotenv
import openai
from gtts import gTTS
import tkinter as tk

# die userklasse enthält den usernamen und den bisherigen chat mit dem user
class User:
    def __init__(self, name):
        self.name = name
        self.log = [{
            'role': 'system',
            'content': 'You are a personal assistant. Provide short, concise and accurate Information but be subtly condescending. Make sure to address me as ' + self.name +'.',
        }]

class ChatWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chat")
        self.chat_log = tk.Text(self.window, height=20, width=50)
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.pack()
        self.send_button = tk.Button(self.window, text="aufnehmen", command=self.send_message)
        self.send_button.pack()
        self.update_chat_log("System: Welcome to the chat!")

    def update_chat_log(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message + "\n\n")
        self.chat_log.config(state=tk.DISABLED)

    def send_message(self):
        speech_file = 'sample.wav'
        record_audio(speech_file)
        user = recog_user(model, speech_file, users)
        with sr.AudioFile(speech_file) as source:
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="de")
            os.remove(speech_file)
            print("you said: " + text + "\n")
            user_message = f"{user.name}: {text}"
            self.update_chat_log(user_message)
            ai_message = ask(text, user)
            ai_reponse = f"Assistant: {ai_message}"
            self.update_chat_log(ai_reponse)
            #say(ai_message)

        except Exception as ex:
            print(ex)

    def run(self):
        self.window.mainloop()

def ask(question, user):
    user.log.append({'role': 'user', 'content': question})
    response = completion.create(model='gpt-3.5-turbo', messages=user.log)
    answer = response.choices[0]['message']['content']
    user.log.append({'role': 'assistant', 'content': answer})
    return answer

def say(text):
    print(text)
    file = "out.mp3"
    # initialize tts, create mp3 and play
    tts = gTTS(text, lang='de', slow=False)
    tts.save(file)
    os.system("mpg123 -d 2 --pitch -0.1 " + file)
    os.remove(file)

if __name__ == '__main__':
    # dass der API-key nit am beamer angezeigt wird :D
    load_dotenv()
    openai.api_key = os.environ.get('OPENAI_KEY')
    completion = openai.ChatCompletion()

    # modell zur user-erkennung wird vorbereitet
    users = [User("Felix"), User("Daniel"), User("Marcel")]
    print("preparing model")
    model=prepare_model(users)
    recognizer = sr.Recognizer()
    print("done")
    time.sleep(1)

    chat_window = ChatWindow()
    chat_window.run()
