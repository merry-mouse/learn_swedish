import PyPDF2 #for pdf reading
from googletrans import Translator # for translating 
from gtts import gTTS # for making text-to-speech mp3 file
import pygame # to build a player and play the sound
import re # to separate sentences from the text
# for creating a player:
from tkinter import * # standard GUI lib
import os
from moviepy.editor import concatenate_audioclips, AudioFileClip

# read pdf in english
pdfFile = open("LittlePrince.pdf","rb")
pdfReader = PyPDF2.PdfFileReader(pdfFile)

# get num of pages
numOfPages = pdfReader.numPages

# get particular page and extract text
page = pdfReader.getPage(1) # starts with 0!
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
    sentences = [s.replace("\t", " ") for s in sentences] # get rid of tabs
    return sentences
    
# call function to split sentences and store it 
eng_page = split_into_sentences(EngText)
swe_page = []

# Translate eng page to swedish
translator = Translator() # initiate translator
for eng_sentence in eng_page:
    translated_to_swe_sentence = translator.translate(eng_sentence,src='en', dest='sv').text
    swe_page.append(translated_to_swe_sentence)


# create text-to-speech audiofiles, save them in sounds directory
def text_to_speech(english_text, swedish_text):
    for i in range(len(english_text)):
        tts_eng_sent = gTTS(english_text[i], lang="en")
        tts_swe_sent = gTTS(swedish_text[i], lang="sv")
        tts_eng_sent.save(savefile=f"C:/Users/potek/PythonAfter6months/FINAL_PROJECT/sounds/sentence{i}.mp3")
        tts_swe_sent.save(savefile=f"C:/Users/potek/PythonAfter6months/FINAL_PROJECT/sounds/sentence{i}_2.mp3")

# call text-to-speech function, create sounds from each sentence, store them in sounds
text_to_speech(eng_page, swe_page)
# clips = [AudioFileClip(c) for c in os.listdir("C://Users/potek/PythonAfter6months/FINAL_PROJECT/sounds")]

# store all sounds objects in one list
clips =[]
for a in os.listdir("C://Users/potek/PythonAfter6months/FINAL_PROJECT/sounds"):
    clips.append(AudioFileClip("./sounds/" + a))

# merge all sounds together
c = concatenate_audioclips(clips)
c.write_audiofile("merged.mp3")

# merge two texts together
merged_text = [i +" " + j for i, j in zip(eng_page, swe_page)]

# MAKING A PLAYER 
root = Tk() # constructor
root.title("Little Prince Swedish lang player")
root.iconbitmap("images/player.ico")
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
    pygame.mixer.music.load("merged.mp3", "mp3")
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