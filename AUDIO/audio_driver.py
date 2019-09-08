import pygame as pg
import os
import time
import threading

class mp3():
    def __init__(self,files_directory,sample_rate=48000,bit_depth= -16,channels=2,buffer_size=2048):
        self.fs = sample_rate
        self.bit_depth = bit_depth
        self.channels = channels
        self.buffer_size = buffer_size
        
        self.thread = threading.Thread()
        self.player = pg
        self.player.mixer.init(self.fs, self.bit_depth, self.channels, self.buffer_size)
        self.files_directory = files_directory
        self.mp3s = []
        for file in os.listdir(files_directory):
            self.mp3s.append(file)
        
    def play(self,file_name,volume=0.85):
        audio_file_location = self.files_directory + file_name
        try: 
            user_volume = float(volume)
        except ValueError:
            print("Volume argument invalid. Please use a float (0.0 - 1.0)")
            self.player.mixer.music.fadeout(1000)
            self.player.mixer.music.stop()
            raise SystemExit
     
        print("Playing at volume: " + str(user_volume)+ "\n")
        self.player.mixer.music.set_volume(user_volume)
        
        '''
        stream music with mixer.music module in blocking manner
        this will stream the sound from disk while playing
        '''
        clock = self.player.time.Clock()
        try:
            self.player.mixer.music.load(audio_file_location)
            print("Music file {} loaded!".format(audio_file_location))
        except self.player.error:
            print("File {} not found! {}".format(audio_file_location, self.player.get_error()))
            return
     
        self.player.mixer.music.play()
        
        # If you want to fade in the audio...
        # for x in range(0,100):
        #     pg.mixer.music.set_volume(float(x)/100.0)
        #     time.sleep(.0075)
        # # check if playback has finished
        while self.player.mixer.music.get_busy():
            clock.tick(30)
    def stop(self):
        pg.mixer.music.fadeout(1000)
        pg.mixer.music.stop()
