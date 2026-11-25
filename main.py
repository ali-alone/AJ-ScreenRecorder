import customtkinter as ctk
import pyautogui
import numpy as np
import pyaudio
import wave
import threading
import time
import cv2
from moviepy import *
from tkinter import messagebox

#main ctk settings

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ScreenRecorder:
    def __init__(self,root):
        self.root = root
        self.root.title("AJ ScrennRecorder")
        self.root.geometry("400x300")
        
        self.recording = False
        self.video_writer = None
        self.audio_frames = []
        self.start_time = None
        
        #user interface
        
        self.title_label = ctk.CTkLabel(root,text="screen recorder", font=("Lalezar,20"))
        self.title_label.pack(pady = 10)
        
        self.start_button = ctk.CTkButton(root, text= "start recording",font=("Lalezar,14"), command=self.start_recording)
        self.start_button.pack(pady = 10)
        
        self.stop_button = ctk.CTkButton(root, text= "stop recording",font=("Lalezar,14"), command=self.stop_recording, state=ctk.DISABLED)
        self.stop_button.pack(pady = 10)
        
        self.status_label = ctk.CTkLabel(root,  text= "Status idle",font=("Lalezar,15"))
        self.status_label.pack(pady =10)

    def start_recording(self):
        self.recording = True
        self.start_button.configure(state = ctk.DISABLED)
        self.stop_button.configure(state = ctk.NORMAL)
        self.status_label.configure(text = "Status: Recording...")
        
        # record video settings
        
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWritter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWritter("output_video.mp4", fourcc ,20.0,screen_size)
        
        #mic settings
        
        self.audio_frames = []
        self.audio = pyaudio.PyAudio()
        self.audio_stream = self.audio.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
        
        # thread recording
        
        self.start_time = time.time()
        threading.Thread(target=self.record_screen).start()
        threading.Thread(target=self.record_audio).start()