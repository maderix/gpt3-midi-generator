'''
this python script converts MIDI notes to actual sounds by generating corresponding notes using a tone generator library

The input midi sheet is in below format.
C C D C
G G A G
E E F E
C C D C
G G A G
E E F E
C C D C
G G A G
F F E D
C C
'''

#import midi
import os
import pygame.mixer
import pygame.sndarray
import pygame.time
import pygame.midi as midi
import sys
import numpy
import math
import time

import wave

from frequencies import frequencies

#you can try editing the frequency and channels according to your taste



def generate_note(note,length=1.0):
    
    frequency = frequencies[note[0]]
    if len(note) == 3:
        frequency = frequency*(2**(int(note[-1])-4))
    # Generate the note
    start = time.time()
    samples,sampleRate = sine_array(frequency,length)
    snd = pygame.sndarray.make_sound(samples)
    #snd.play(fade_ms=0)
    #print('after play',time.time()-start)
    #while time.time() - start < 0.35:
    #    continue
    snd.stop()
    sample = snd.get_raw()
    return sample
    


def sine_array(frequency,length):
    # Generate a sine wave of the given frequency and length
    sampleRate = 44100
    nSamples = int(round(length*sampleRate))
    buf = numpy.zeros((nSamples,2),dtype=numpy.int16)
    maxVol = 2**15-1.0
    for s in range(nSamples):
        t = float(s)/sampleRate
        buf[s][0] = maxVol*math.sin(2*math.pi*frequency*t)
        buf[s][1] = buf[s][0]
    return buf,sampleRate


def generate_and_save_wav(notes_file,wav_file, channels=2, samplerate=44100, samplewidth=2, play_song=False):
    assert os.path.exists(notes_file), 'File %s does not exist' % notes_file
    pygame.midi.init()
    pygame.mixer.init(frequency=samplerate, size=-16, channels=channels, buffer=1024)
    fileObject = open(notes_file,'r')
    counter = 0
    samples = []
    import tqdm
    # Read the file line by line
    print('rendering sound...')
    for line in tqdm.tqdm(fileObject):
        # Split the line into individual notes
        notes = line.split()
        # render each note one by one
        for note in notes:
            sample = generate_note(note,0.5)
            samples.append(sample)
        # Wait for a second after each line
        #pygame.time.wait(100)
        counter += 1

    #save samples to wav file
    print('writing wav file..')
    with wave.open(wav_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(samplewidth)
        wf.setframerate(samplerate)
        wf.writeframes(b''.join(samples))
    #play wav file using pygame
    if play_song:
        pygame.mixer.music.load(wav_file)
        pygame.mixer.music.play()
        print('playing audio',wav_file)
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

if __name__ == '__main__':
    generate_and_save_wav('notes/Original_nokia_theme.txt','out.wav',True)