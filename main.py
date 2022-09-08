from email.policy import strict
from io import BytesIO
from multiprocessing.connection import wait
from typing import List
import PyPDF2 #for pdf reading
from googletrans import Translator # for translating 
import codecs # for utf-8 encoding, otherwise can't read swedish letters
from gtts import gTTS # for making text-to-speech mp3 file
from playsound import playsound # for playing saved mp3
import pygame # to build a player and play the sound
import re # to separate sentences from the text

# read pdf in english
pdfFile = open("LittlePrince.pdf","rb")
pdfReader = PyPDF2.PdfFileReader(pdfFile)

# get num of pages
numOfPages = pdfReader.numPages

# get particular page and extract text
page = pdfReader.getPage(13)
EngText = page.extractText()

# using timer to understand how long would the translation take
# import time
# start_time = time.time()


# regex patterns for separating sentences from the text on the page
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

# split each sentence
def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    
    pygame.init()
    pygame.mixer.init()
    # print eng text and voice it
    for eng_sentence in sentences:
        text_to_speach_translate(eng_sentence)
        # print(b)
        # mp3_fo = BytesIO()
        # ENG_mp3_object = gTTS(b, lang="en")
        # ENG_mp3_object.write_to_fp(mp3_fo)
        # pygame.mixer.music.load(mp3_fo, "mp3")
        # pygame.mixer.music.play()
        # while pygame.mixer.music.get_busy() == True: # to wait until player stops playing
        #     wait
        # translate sentence from eng to swedish
        # translator = Translator()
        # translated_text = translator.translate(sentence, dest='sv',).text
        # print(translated_text)
        # # print eng and swe sentences one after another
        # mp3_fo = BytesIO()
        # SWE_mp3_object = gTTS(translated_text, lang="sv")
        # SWE_mp3_object.write_to_fp(mp3_fo)
        # pygame.mixer.music.load(mp3_fo, "mp3")
        # pygame.mixer.music.play()
        # while pygame.mixer.music.get_busy() == True:
        #     wait
        # playsound(SWE_mp3)

# print("My program took", time.time() - start_time, "to run")
def text_to_speach_translate(eng_sentence):
    print(eng_sentence)
    mp3_bytes_object = BytesIO() #manipulates bytes data in memory
    text_to_speech_mp3_object = gTTS(eng_sentence, lang="en")
    text_to_speech_mp3_object.write_to_fp(mp3_bytes_object)
    pygame.mixer.music.load(mp3_bytes_object, "mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True: # to wait until player stops playing
        wait

    translator = Translator()
    translated_to_swe_sentence = translator.translate(eng_sentence, dest='sv',).text
    print(translated_to_swe_sentence)
    # print eng and swe sentences one after another
    mp3_bytes_object = BytesIO()
    text_to_speech_mp3_object = gTTS(translated_to_swe_sentence, lang="sv")
    text_to_speech_mp3_object.write_to_fp(mp3_bytes_object)
    pygame.mixer.music.load(mp3_bytes_object, "mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        wait
split_into_sentences(EngText)



# # store translated text in a txt file
# codecs.open('SWE.txt', encoding='utf-8', mode='w+').write(translated_text)
# print(translated_text)

# # transform swe text into speech and save as mp3
# SWE_mp3 = gTTS(translated_text, lang="sv")
# SWE_mp3.save("SWE_LittlePrince.mp3")

# # play mp3
# playsound("C:\\Users\potek\PythonAfter6months\FINAL_PROJECT\hej.mp3")




# # MAKING A PLAYER 
# from tkinter import *
# import pygame

# root = Tk()
# root.title("Little Prince Swedish lang player")
# root.iconbitmap("player.ico")
# root.geometry("500x300")

# # initialize pygame mixer
# pygame.mixer.init()

# # create playlist box
# song_box = Listbox(root, bg="black", fg="green", width=600)
# song_box.pack(pady=20)

# # define player control buttons
# play_button_img = PhotoImage(file="images/button_play_48px.png")
# pause_button_img = PhotoImage(file="images/button_pause_48px.png")
# stop_button_img = PhotoImage(file="images/button_stop_48px.png")

# # create player control frame
# controls_frame = Frame(root)
# controls_frame.pack()

# # play swemp3 file 
# def play():
#     audio = ("C:\\Users\potek\PythonAfter6months\FINAL_PROJECT\hej.mp3")
#     pygame.mixer.music.load(audio)
#     pygame.mixer.music.play(loops=0)
# # stop playing audio
# def stop():
#     pygame.mixer.music.stop()
#     song_box.select_clear(ACTIVE)

# # create global pause variable
# global paused 
# paused = False

# # pause and unpause audio
# def pause(is_paused):
#     global paused
#     paused = is_paused

#     if paused:
#         # unpause
#         pygame.mixer.music.unpause()
#         paused = False
#     else:
#         # pause
#         pygame.mixer.music.pause()
#         paused = True


# # create player control buttons
# play_button = Button(controls_frame,image=play_button_img, borderwidth=0, command=play)
# pause_button = Button(controls_frame,image=pause_button_img, borderwidth=0, command=lambda: pause(paused))
# stop_button = Button(controls_frame,image=stop_button_img, borderwidth=0, command=stop)

# play_button.grid(row=0, column=0, padx=10)
# pause_button.grid(row=0, column=2, padx=10)
# stop_button.grid(row=0, column=1, padx=10)


# root.mainloop()
