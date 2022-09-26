from io import BytesIO
from typing import List
import PyPDF2 #for pdf reading
from googletrans import Translator # for translating 
import codecs # for utf-8 encoding, otherwise can't read swedish letters
from gtts import gTTS # for making text-to-speech mp3 file
import pygame # to build a player and play the sound
import re # to separate sentences from the text
# for creating a player:
from tkinter import * # standard GUI lib
import pygame
import time
import os

# read pdf in english
pdfFile = open("LittlePrince.pdf","rb")
pdfReader = PyPDF2.PdfFileReader(pdfFile)

# get num of pages
numOfPages = pdfReader.numPages

# get particular page and extract text
page = pdfReader.getPage(9) # starts with 0!
EngText = page.extractText()


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
    return sentences
    


# print, and play text-to-speach splitted sentences
def text_to_speech(sentence, language):
    
    # initialize BytesIO
    mp3_bytes_object = BytesIO() # manipulates bytes data into memory
    # text-to-speech given sentence
    text_to_speech_mp3_object = gTTS(sentence, lang=language)
    # store it in mp3_bytes_object
    text_to_speech_mp3_object.write_to_fp(mp3_bytes_object)
    return mp3_bytes_object

# call function to split sentences and store it 
eng_page = split_into_sentences(EngText)


# MAKING A PLAYER 
root = Tk() # constructor
root.title("Little Prince Swedish lang player")
root.iconbitmap("player.ico")
root.geometry("900x600")
root.option_add('*Font', 'Times 15')

# initialize pygame mixer
pygame.mixer.init()

# create playlist box
song_box = Listbox(root, bg="black", fg="yellow", width=800, height=20)
song_box.pack(pady=20)

# define player control buttons
play_button_img = PhotoImage(file="images/button_play_48px.png")
pause_button_img = PhotoImage(file="images/button_pause_48px.png")
stop_button_img = PhotoImage(file="images/button_stop_48px.png")

# create player control frame
controls_frame = Frame(root)
controls_frame.pack()

# play eng and swe mp3 files
def play():
    for eng_sentence in eng_page:
        eng_sentence = eng_sentence.replace("\t", " ")
        # insert english text
        song_box.insert(END, eng_sentence) # Use END as the first argument if you want to add new lines to the end of the listbox
        root.update()
        # create mp3object eng sentence
        eng_audio = text_to_speech(eng_sentence, "en")
        # translate eng sentence to swe 
        translator = Translator() # initiate translator
        translated_to_swe_sentence = translator.translate(eng_sentence, dest='sv',).text
        # create mpr object swe sentence
        swe_audio = text_to_speech(translated_to_swe_sentence, "sv")
        pygame.mixer.music.load(eng_audio , "mp3")
        
        pygame.mixer.music.play(loops=0)
        # needs to wait until sentence stop playing 
        while pygame.mixer.music.get_busy() == True:
            time.sleep(0.5)
        pygame.mixer.music.load(swe_audio, "mp3")
        song_box.insert(END, str(translated_to_swe_sentence)) # Use END as the first argument if you want to add new lines to the end of the listbox
        root.update()
        pygame.mixer.music.play(loops=0)
        # needs to wait until sentence stop playing 
        while pygame.mixer.music.get_busy() == True:
            time.sleep(0.5)

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
        os.system("pause")

# create player control buttons
play_button = Button(controls_frame,image=play_button_img, borderwidth=0, command=play)
pause_button = Button(controls_frame,image=pause_button_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame,image=stop_button_img, borderwidth=0, command=stop)

play_button.grid(row=0, column=0, padx=10)
pause_button.grid(row=0, column=2, padx=10)
stop_button.grid(row=0, column=1, padx=10)

root.mainloop()