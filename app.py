import os
from glob import glob
from pprint import pprint
import numpy as np
from numpy.random import random_sample
from numpy.random.mtrand import dirichlet
from numpy.random import choice
import mad
import pyaudio

knowledge = {}
p = pyaudio.PyAudio()

def main():

  assets_dir = './assets'
  os.chdir(assets_dir)
  sample_names = [mp3_file for mp3_file in glob("*.mp3")]
  playing_song = choice(sample_names)

  generateMarkovChain(sample_names)
  
  stream = p.open(format =
                p.get_format_from_width(pyaudio.paInt32),
                channels = 2,
                rate = 44100,
                output = True)

  while True:
    next_song = pick_next(playing_song, 1)[0]
    play(next_song, stream)

    next = pick_next(playing_song, 1)
    playing_song = next[0]

    print("===============================================")
    print("next round:")
    pprint(knowledge[playing_song])   
    pprint("selected song: " + playing_song) 
    pprint("selected song probability: " + str(next[1]))

def generateMarkovChain(sample_names):
  for sample in sample_names:
    sample_probs = []
    knowledge[sample] = sample_probs
    random_distribution = dirichlet([1] * len(sample_names))
    for i, sample_child in enumerate(sample_names):
      song_prob = (sample_child, random_distribution[i])
      sample_probs.append(song_prob)

def pick_next(sample, size):
  this_sample = knowledge[sample]
  values = [val[0] for val in this_sample]
  probabilities = [val[1] for val in this_sample]
  bins = np.add.accumulate(probabilities)
  song_index = np.digitize(random_sample(size), bins)
  return (values[song_index], probabilities[song_index])

def play(filename, stream):
  mf = mad.MadFile(filename)
  data = mf.read()
  while data != None:
    stream.write(data)
    data = mf.read()
#  stream.close()
#  p.terminate()

if __name__ == "__main__":
  main()