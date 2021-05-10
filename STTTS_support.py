#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.12
# In conjunction with Tcl version 8.6
#    Apr 07, 2020 01:22:24 PM
#    Apr 07, 2020 01:25:58 PM
#    Apr 07, 2020 01:53:27 PM


import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True
    
def set_Tk_var():
    #General
    global lingua
    lingua = StringVar()
    global message
    message = StringVar()
    
    #TTS
    global path
    path = ""
    global sourceText
    sourceText = ""
    global save_folder 
    save_folder = ""
    
    #STT
    global source_file 
    source_file = ""
    global transcript
    transcript = ""



def STT_clearBTN_leftClick(p1):
    print('STTTS_support.STT_clearBTN_leftClick')
    sys.stdout.flush()
    source_file = ""
    lingua.set("en")


def TTS_clearBTN_leftClick(p1):
    print('STTTS_support.TTS_clearBTN_leftClick')
    sys.stdout.flush()
    path=""
    global sourceText
    sourceText=""   
    lingua.set("en")

def Browse(p1):
    print('QTI_support.Browse')
    from tkinter import filedialog
    file = filedialog.askopenfile(mode='rb',
                              filetypes =[('mp3Files', '*.mp3')],
                                          title='Choose a file')
    global source_file
    source_file = file.name
    print(source_file)
    sys.stdout.flush()

def Browse_folder(p1):
    from tkinter import filedialog
    print('QTI_support.Browse_folder')
    folder=filedialog.askdirectory()
    global save_folder
    save_folder = folder
    sys.stdout.flush()

 
def get_TTS(STR,path):
    from gtts import gTTS
    tts = gTTS(STR, lang=lingua.get())
    tts.save(path+"\\"+sourceText+".mp3")
    message.set(message.get()+STR + " converted to audio and saved to "+path+"\\"+sourceText+".mp3"+"\n")
    
def transcribe_mp3(file):
    
    def convert_audio(file):
        '''
        takes filename as string
        saves ouput file
        returns name of output file as string
        '''
        infile=file
        outfile=tempdir+"tempaudio.wav"
        
        import subprocess
        import time
        p=subprocess.Popen(['ffmpeg', '-i', infile, outfile], shell=False)
        time.sleep(10)
        p.terminate
        print(file + " has been converted to wav format")
        return(outfile)
    
    def chunk_audio(file):
        '''
        produces 50 sec chunks of an audio file, with 2 sec overlaps
        '''
        print("Enter chunk audio funtion")
        from pydub import AudioSegment
        sound = AudioSegment.from_wav(file)    
        
        import audioread
        with audioread.audio_open(file) as f:
            seconds = f.duration     #get duration of file in seconds
        length=int(seconds*1000)    #convert to miliseconds
        intervals= zip(range(50000,length+50000,50000), range(100000, length+100000, 50000))
        
        new_file = sound[0 : 50000]       
        new_file.export(tempdir+"\\{:04d}-{:04d}.wav".format(0,50), format="wav")
        print("Created file "+tempdir+"\\{:04d}-{:04d}.wav".format(0,50))
        for x,y in intervals:
            new_file = sound[x-2000 : y]
            new_file.export(tempdir+"\\{:04d}-{:04d}.wav".format(x//1000,y//1000), format="wav")
            print("Created file "+tempdir+"\\{:04d}-{:04d}.wav".format(x//1000,y//1000))
                  
    def create_transcriber(lang):
        def transcribe(file):
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.AudioFile(tempdir+"\\"+file) as source:
                print("{} loaded".format(file) +"\n")
                audio = r.record(source)
                print("{} recorded".format(file) +"\n")
            with open("api-key.json") as f:
                API_KEY=f.read()
                print("API credentials loaded")
                #TODO Currently reaches here and stalls. No error, but never produces text
                text = r.recognize_google_cloud(audio, credentials_json=API_KEY, language=lang)
                print(text)
            print("{}transcribed".format(file) +"\n")
            return text
        return transcribe
    
    
    def transcribe_multiples():
        from multiprocessing.dummy import Pool
        import multiprocessing
        import os
        pool = Pool(len(os.listdir(tempdir+"\\"))) # Number of concurrent threads
        files=os.listdir(tempdir+"\\")
        filtered=[]
        for x in files:
            if os.stat(tempdir+'\\'+x).st_size>50:
                filtered.append(x)
        transcriber=create_transcriber(lingua.get())
        all_text = pool.map(transcriber, filtered)
        pool.close()
        pool.join()
        transcript = ""
        for text in all_text:
            transcript+=text
        return(transcript)
    
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as tempdir:
        print(tempdir)
        wav=convert_audio(file)
        chunk_audio(wav)
        transcript=transcribe_multiples()
        return transcript
    

def Exit_LeftClick(p1):
    print('STTTS_support.Exit_LeftClick')
    sys.stdout.flush()
    destroy_window()

def STT_Submit_leftClick(p1):
    print('STTTS_support.STT_Submit_leftClick')
    sys.stdout.flush()
    source=source_file
    text=transcribe_mp3(source)
    global transcript
    transcript = text
    output=source+"Transcript.txt"
    outfile=open(output, "w")
    outfile.write(text)
    message.set(message.get()+ source + " transcribed and saved to " + output + "\n")


def TTS_Submit_leftClick(p1):
    print('STTTS_support.TTS_Submit_leftClick')
    sys.stdout.flush()
    path=save_folder
    global sourceText
    sourceText = w.TextEntry.get()
    get_TTS(sourceText, path)

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
    lingua.set("en")    

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None
   

if __name__ == '__main__':
    import STTTS
    STTTS.vp_start_gui()










