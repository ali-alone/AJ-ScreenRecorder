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
        
        self.title_label = ctk.CTkLabel(root,text="AJ screen recorder",font=("Arial",25))
        self.title_label.pack(pady = 10)
        
        self.start_button = ctk.CTkButton(root, text= "start recording",font=("Arial",20), command=self.start_recording)
        self.start_button.pack(pady = 25)
        
        self.stop_button = ctk.CTkButton(root, text= "stop recording",font=("Arial",20), command=self.stop_recording, state=ctk.DISABLED)
        self.stop_button.pack(pady = 20)
        
        self.status_label = ctk.CTkLabel(root,  text= "Status idle",font=("Arial",15))
        self.status_label.pack(pady =30)

    def start_recording(self):
        self.recording = True
        self.start_button.configure(state = ctk.DISABLED)
        self.stop_button.configure(state = ctk.NORMAL)
        self.status_label.configure(text = "Status: Recording...")
        
        # record video settings
        
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter("output_video.mp4", fourcc ,20.0,screen_size)
        
        #mic settings
        
        self.audio_frames = []
        self.audio = pyaudio.PyAudio()
        self.audio_stream = self.audio.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
        
        # thread recording
        
        self.start_time = time.time()
        threading.Thread(target=self.record_screen).start()
        threading.Thread(target=self.record_audio).start()
        
    def record_screen(self):
        while self.recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            self.video_writer.write(frame)
            
            # record time stream
            
            elapsed_time = time.time() - self.start_time
            self.status_label.configure(text=f"Status: Recording...{int(elapsed_time)}s")
            
    def record_audio(self):
        while self.recording:
            data = self.audio_stream.read(1024)
            self.audio_frames.append(data)
                    
                    
    def stop_recording(self):
        self.recording = False
        self.start_button.configure(state = ctk.NORMAL)
        self.stop_button.configure(state= ctk.DISABLED)
        self.status_label.configure(text="status: idle")
                
                
        #stop video recording
                
        self.video_writer.release()
                
        #stop audio recording
                
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio.terminate()
                
                
        #mic sound save 
                
        with wave.open("output_audio.wav","wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b"".join(self.audio_frames))
        
        
            # sound and video mix
        self.combine_audio_video("output_video.mp4" ,"output_audio.wav","output_final.mp4")
        messagebox.showinfo("info", "video saved as output_final")
                
    def combine_audio_video(self,video_path,audio_path,output_path):
        # save path
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        
        #video and mic combine 
        
        final_clip = video_clip.with_audio(audio_clip)
        final_clip.write_videofile(output_path,codec="libx264")
        
        #close
        
        video_clip.close()
        audio_clip.close()
        
if __name__ == "__main__":
    root = ctk.CTk()
    recorder = ScreenRecorder(root)
    root.mainloop()