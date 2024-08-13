import pygame
import librosa
import numpy as np
import time

class BusSound():
    def __init__(self):
        self.cur_freq = 1000
#        pygame.mixer.pre_init(4100, -16, 2, 2048)
        pygame.mixer.init()
#        self.sound_file = "bus-engine2.wav"
#        self.bussound = pygame.mixer.Sound(self.sound_file)
#        self.original_sound = AudioSegment.from_file("bus-engine.mp3")
        self.acceleration_values = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
#        self.current_acceleration = 1.0
        self.sound_channel = pygame.mixer.Channel(0)  # Create a mixer channel
        self.sound_stop = False
        self.sec = time.time()
        self.sound_dict = {}

        # Load the sound
        self.original_sound, self.sr = librosa.load("bus-engine2.wav", sr=None, mono=False)
        self.testsound = pygame.mixer.Sound("bus-engine2.wav")

    # Function to change pitch
    def change_pitch(self, sound, sr, n_steps):
        return librosa.effects.pitch_shift(sound, sr=sr, n_steps=n_steps)

#    # Function to convert NumPy array to Pygame Sound object
#    def numpy_array_to_pygame_sound(self, array):
#        # Convert the NumPy array to bytes
#        raw_data = (array * 32767).astype(np.int16).tobytes()
#        # Create a Pygame sound object
#        sound = pygame.mixer.Sound(buffer=raw_data)
#        return sound



    # Function to convert NumPy array to Pygame Sound object
    def numpy_array_to_pygame_sound(self, array, sr, channels):
        # Convert the NumPy array to bytes
        if channels == 2:
            raw_data = (array.T * 32767).astype(np.int16).tobytes()
        else:
            raw_data = (array * 32767).astype(np.int16).tobytes()
        # Create a Pygame sound object
        sound = pygame.mixer.Sound(buffer=raw_data)
        return sound








    def make_pitches(self):
        for i in range(1, 4):
            
            # Change the pitch of the sound based on the current_pitch value
            pitch_changed_sound = self.change_pitch(self.original_sound, self.sr, i)  #current_pitch)
            # Convert the pitch-changed NumPy array to a Pygame Sound object
#            self.sound_dict[i/10] = self.numpy_array_to_pygame_sound(pitch_changed_sound)


          # Convert the pitch-changed NumPy array to a Pygame Sound object
            channels = pitch_changed_sound.shape[0] if pitch_changed_sound.ndim > 1 else 1
            sound = self.numpy_array_to_pygame_sound(pitch_changed_sound, self.sr, channels)



            self.sound_dict[i/10] = sound

        print(self.sound_dict)


    def sound_routine(self, current_pitch):
        if time.time() - self.sec >= 3 and self.sound_stop:
            pass
            #self.sound_channel.stop()
            

        # Play the sound if it's not already playing
        #if not self.sound_channel.get_busy():  # and not self.sound_stop:
        if not pygame.mixer.get_busy():
#            self.sound_dict[current_pitch].play()
            self.sound_channel.play(self.sound_dict[current_pitch])

            #pygame.mixer.Sound.play(self.testsound)
            self.sound_stop = True


















#
#    def change_pitch(self,  speed=1.0):
#        # Change the playback speed
#        sound_with_changed_pitch = self.original_sound._spawn(self.original_sound.raw_data, overrides={
#            "frame_rate": int(self.original_sound.frame_rate * speed)
#        })
#    
#        # Adjust the frame rate to maintain the original duration
#        sound_with_changed_pitch = sound_with_changed_pitch.set_frame_rate(self.original_sound.frame_rate)
#        return sound_with_changed_pitch
#
#    # Function to play sound
#    def play_sound(self, sound):
#        print("play_sound")
#        if self.play_obj and self.play_obj.is_playing():
#            self.play_obj.stop()
#        raw_data = sound.raw_data
#        
#        self.wave_obj = sa.WaveObject(raw_data, num_channels=sound.channels, bytes_per_sample=sound.sample_width, sample_rate=sound.frame_rate)
#        self.play_obj = self.wave_obj.play()
#        #self.play_obj.wait_done()
#
#    def play_sound2(self, sound):
#        pygame.mixer.Sound.play(sound)
#        #self.sound_file = "bus-engine2.wav"
#        self.bussound = pygame.mixer.Sound(buffer=sound)
#
        #play(sound)


#
#    def play_sound(self):
##        #pygame.mixer.Sound.play(self.bus_sound)
##        # Clamp the acceleration value to a reasonable range
##        self.current_acceleration = max(0.5, min(self.current_acceleration, 2.0))
##
##        # Change the pitch of the sound based on the current acceleration
##        pitch_changed_sound = self.change_pitch(self.original_sound, self.current_acceleration)
##
#        # Convert the pitch-changed sound to a format Pygame can play
#        raw_data = self.original_sound.raw_data
#        audio = sa.WaveObject(raw_data, num_channels=pitch_changed_sound.channels, bytes_per_sample=pitch_changed_sound.sample_width, sample_rate=pitch_changed_sound.frame_rate)
#        play_obj = audio.play()
#
#        # Allow the sound to play (non-blocking)
#        play_obj.wait_done()
#

