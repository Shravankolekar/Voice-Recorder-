import sounddevice as sd

from tkinter import *

import queue

import soundfile as sf

import threading

from tkinter import messagebox

import datetime 

from tkinter import filedialog as fd

from playsound import playsound

# Create a queue to store audio data

q = queue.Queue()

# Declare control flags

recording = False

# Callback to collect audio data

def callback(indata, frames, time, status):
    q.put(indata.copy())

# Record audio function

def record_audio():

    global recording

    recording = True

    messagebox.showinfo(message="Recording... Speak into the microphone.")
    
    dt = datetime.datetime.now().strftime('%d_%m_%y_%H_%M_%S')

    filename = f"{dt}.wav"

    with sf.SoundFile(filename, mode='w', samplerate=44100, channels=2) as file:

        with sd.InputStream(samplerate=44100, channels=2, callback=callback):

            while recording:

                file.write(q.get())

    messagebox.showinfo(message=f"Recording saved as {filename}")


# Threaded control for recording/stop

def threading_rec(x):

    if x == 1:

        t1 = threading.Thread(target=record_audio)

        t1.start()

    elif x == 2:

        global recording

        recording = False

# File open and playback

def select_file():
    
    filetypes = (

        ('Audio files', '*.wav'),

        ('All files', '*.*')
    )
    
    filename = fd.askopenfilename(

        title='Open a file',

        initialdir='/',

        filetypes=filetypes
    )
    
    if filename:

        try:

            playsound(filename)

        except Exception as e:

            messagebox.showerror("Error", f"Could not play file:\n{e}")

# GUI setup

voice_rec = Tk()

voice_rec.geometry("360x200")

voice_rec.title("Voice Recorder")

voice_rec.config(bg="#800080")

# Title

Label(voice_rec, text=" Voice Recorder", bg="#107dc2", fg="white", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10)

# Buttons

Button(voice_rec, text="Record Audio", bg='#FF7F7F', command=lambda: threading_rec(1)).grid(row=1, column=0, padx=10, pady=10)

Button(voice_rec, text="Stop Recording", bg='#FFB6C1', command=lambda: threading_rec(2)).grid(row=1, column=1, padx=10, pady=10)

Button(voice_rec, text="Play (Open File)", bg='#90EE90', command=select_file).grid(row=1, column=2, padx=10, pady=10)

voice_rec.mainloop()

