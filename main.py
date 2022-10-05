from cgitb import text
import PyPDF2 #for pdf reading
from googletrans import Translator # for translating 
from gtts import gTTS # for making text-to-speech mp3 file
import pygame # to play the sound
import re # to separate sentences from the text
# for creating a player:
from tkinter import * # standard GUI lib
from tkinter import filedialog
from tkinter import simpledialog
import os
from moviepy.editor import concatenate_audioclips, AudioFileClip

def extract_text(pdf_file, page_num):
    # read pdf in english
    pdfFile = open(pdf_file,"rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    # get num of pages
    numOfPages = pdfReader.numPages
    # get particular page and extract text
    page = pdfReader.getPage(page_num) # starts with 0!
    EngText = page.extractText()
    return EngText


# split each sentence
def split_into_sentences(text):
    # regex patterns for separating sentences from the text on the page
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    digits = "([0-9])"
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
    
# # Translate eng page to swedish
def translate_into_swedish(english_sentences):
    translator = Translator() # initiate translator
    translated_to_swe_sentences = []
    for eng_sentence in english_sentences:
        translated_to_swe_sentence = translator.translate(eng_sentence,src='en', dest='sv').text
        translated_to_swe_sentences.append(translated_to_swe_sentence)
    return translated_to_swe_sentences


# create text-to-speech audiofiles, save them in sounds directory
def text_to_speech(english_text, swedish_text):
    for i in range(len(english_text)):
        tts_eng_sent = gTTS(english_text[i], lang="en")
        tts_swe_sent = gTTS(swedish_text[i], lang="sv")
        tts_eng_sent.save(savefile=f"C:/Users/potek/PythonAfter6months/FINAL_PROJECT/sounds/sentence{i}.mp3")
        tts_swe_sent.save(savefile=f"C:/Users/potek/PythonAfter6months/FINAL_PROJECT/sounds/sentence{i}_2.mp3")


# store all sounds objects in one list and merge
def merge_eng_swe_sounds():
    clips =[]
    for sounds in os.listdir("C://Users/potek/PythonAfter6months/FINAL_PROJECT/sounds"):
        clips.append(AudioFileClip("./sounds/" + sounds))

    # merge all sounds together
    c = concatenate_audioclips(clips)
    c.write_audiofile("merged.mp3")

# merge two texts together
def merge_eng_swe_sentences(splitted_eng_sentences, splitted_swe_sentences):
    merged_text = [x for y in zip(splitted_eng_sentences, splitted_swe_sentences) for x in y]
    return merged_text

# MAKING A PLAYER 
root = Tk() # constructor
root.title("Little Prince Swedish lang player")
root.iconbitmap("images/player.ico")
root.geometry("900x600")
root.option_add('*Font', 'Times 15')

# initialize pygame mixer to play the sound
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


# add pdf function
def add_pdf():

    # user choise of PDF
    eng_pdf = filedialog.askopenfilename(initialdir="C:/Users/potek/PythonAfter6months/FINAL_PROJECT/", title="Choose PDF", filetypes=(("pdf files", "*.pdf"), ))
   
    pdfFile = open(eng_pdf,"rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    # get num of pages
    numOfPages = pdfReader.numPages

    # change the state of the disabled choose pagenum menu
    choose_pagenum_menu.entryconfig("Choose pagenum or start from the beginning", state="normal")
    root.update()
    
    # open pagenum input window
    page_num = take_user_input_for_pagenum(numOfPages)
    
    # message for the user
    song_box.insert(END, "Extracting text...")
    root.update()

    # extract text from English PDF
    extracted_eng_text = extract_text(eng_pdf, page_num)

    # message for the user
    song_box.insert(END, "Splitting into sentences...")
    root.update()

    # split it into separate sentences
    splitted_eng_sentences = split_into_sentences(extracted_eng_text)

    # message for the user
    song_box.insert(END, "Translating to Swedish...")
    root.update()

    # translate them to swedish
    translated_to_swe_sentences = translate_into_swedish(splitted_eng_sentences)

    # message for the user
    song_box.insert(END, "Creating text-to-speech sounds for english and swedish text...")
    root.update()

    # create text-to-speech audios, save them in /sounds
    text_to_speech(splitted_eng_sentences, translated_to_swe_sentences)

    # message for the user
    song_box.insert(END, "Merging sounds...Almost done...")
    root.update()

    # store all sounds objects in one list and merge
    merge_eng_swe_sounds()
    
    # delete all messages
    song_box.delete(0,END)

    # merge eng and swe sentences elementwise for printing
    merged_text_eng_swe = merge_eng_swe_sentences(splitted_eng_sentences, translated_to_swe_sentences)
    for sentence in merged_text_eng_swe:
        song_box.insert(END, sentence)

    # delete all sounds files in sound folder, since we merged them, we don't need them anymore
    path = "C://Users/potek/PythonAfter6months/FINAL_PROJECT/sounds/"
    for file_name in os.listdir(path):
    # construct full file path
        file = path + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)

# choose pagenumber function
def choose_pagenumber():
    pass
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

# create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add Add PDF and choose page number Menu
add_pdf_menu = Menu(my_menu)
choose_pagenum_menu = Menu(my_menu)
# add cascades and commands
my_menu.add_cascade(label="ADD PDF", menu=add_pdf_menu)
add_pdf_menu.add_command(label="Add PDF in English", command=add_pdf)
my_menu.add_cascade(label="PAGE NUMBER",menu=choose_pagenum_menu)



def take_user_input_for_pagenum(last_page):
    user_input = simpledialog.askstring("Page number", f" Type page number(0-{last_page})")
    return int(user_input)
    # if user_input != "":
    #     print(user_input)

choose_pagenum_menu.add_command(label="Choose pagenum or start from the beginning", command=take_user_input_for_pagenum)
choose_pagenum_menu.entryconfig("Choose pagenum or start from the beginning", state="disabled")


root.mainloop()