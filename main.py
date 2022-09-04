"""Plan:
- Write code that imports an pdf
- make this pdf => .txt
- then translates it into Swedish, so we have Swedish txt file.
- Write code that reads a sentence of Swedish book, then English.
"""

# from typing import List
# import PyPDF2 #for pdf reading
# from googletrans import Translator # for translating 
# import codecs # for utf-8 encoding 
# from gtts import gTTS # for making text-to-speech mp3 file
# from playsound import playsound # for playing saved mp3

# # read pdf in english
# pdfFile = open("LittlePrince.pdf","rb")
# pdfReader = PyPDF2.PdfFileReader(pdfFile)

# # get num of pages
# numOfPages = pdfReader.numPages

# # get particular page and extract text
# page = pdfReader.getPage(14)
# text = page.extractText()

# # transkate eng text into swedish
# translator = Translator()
# translated_text = translator.translate(text, dest='sv').text

# # store translated text in a txt file
# codecs.open('SWE.txt', encoding='utf-8', mode='w+').write(translated_text)
# print(translated_text)

# # transform swe text into speech and save as mp3
# SWE_mp3 = gTTS(translated_text, lang="sv")
# SWE_mp3.save("SWE_LittlePrince.mp3")

# # play mp3
# playsound("C:\\Users\potek\PythonAfter6months\FINAL_PROJECT\hej.mp3")


# MAKING A PLAYER 
from tkinter import *
import pygame

root = Tk()
root.title("Little Prince Swedish lang player")
root.iconbitmap("player.ico")
root.geometry("500x300")

# initialize pygame mixer
pygame.mixer.init()

# create playlist box
song_box = Listbox(root, bg="black", fg="green", width=600)
song_box.pack(pady=20)

# define player control buttons
play_button_img = PhotoImage(file="images/button_play_48px.png")
pause_button_img = PhotoImage(file="images/button_pause_48px.png")
stop_button_img = PhotoImage(file="images/button_stop_48px.png")

# create player control frame
controls_frame = Frame(root)
controls_frame.pack()

# play swemp3 file 
def play():
    audio = ("C:\\Users\potek\PythonAfter6months\FINAL_PROJECT\hej.mp3")
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play(loops=0)
# stop playing audio
def stop():
    pygame.mixer.music.stop()
    song_box.select_clear(ACTIVE)

# create global pause variable
global paused 
paused = False

# pause and unpause audio
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # pause
        pygame.mixer.music.pause()
        paused = True




# create player control buttons
play_button = Button(controls_frame,image=play_button_img, borderwidth=0, command=play)
pause_button = Button(controls_frame,image=pause_button_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame,image=stop_button_img, borderwidth=0, command=stop)

play_button.grid(row=0, column=0, padx=10)
pause_button.grid(row=0, column=2, padx=10)
stop_button.grid(row=0, column=1, padx=10)


root.mainloop()
