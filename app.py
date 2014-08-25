import os
from glob import glob
from pprint import pprint
import numpy as np
from numpy.random import random_sample
from numpy.random.mtrand import dirichlet
from random import choice
from pyomxplayer import OMXPlayer
import time

knowledge = {}
silent_knowledge = {}
player = None

def main():
  sample_names = [mp3_file for mp3_file in glob("/mnt/storage")]
  playing_song = choice(sample_names)

  selector = ["silent", "silent", "sound"]
  playing_selector = choice(selector)

  knowledge = generateMarkovChain(sample_names)
  silent_knowledge = generateMarkovChain(selector)

  player = OMXPlayer(playing_song, start_playback=True)

  while True:
    while player.finished == False:
      continue
    else:
      silent_picker = pick_next(playing_selector, silent_knowledge)
      next_step = silent_picker[0]

      print("===============================================")
      print("this round:")

      if next_step == "silent":
        next_prob = silent_picker[1]
        seconds_of_silence = float(next_prob*10)
        print "playing silence for " + str(seconds_of_silence) + " seconds"
        time.sleep(seconds_of_silence)
      else:
        picker = pick_next(playing_song, knowledge)
        next_song = picker[0]
        next_prob = picker[1]
        print("playing sound")
        print("selected song: " + playing_song) 
        print("selected song probability: " + str(next_prob))
        player = OMXPlayer(next_song, start_playback=True)    
        playing_song = next_song

def generateMarkovChain(sample_names):
  chain = {}
  for sample in sample_names:
    sample_probs = []
    chain[sample] = sample_probs
    random_distribution = dirichlet([1] * len(sample_names))
    for i, sample_child in enumerate(sample_names):
      song_prob = (sample_child, random_distribution[i])
      sample_probs.append(song_prob)
  return chain

def pick_next(sample, markov):
  size = 1
  this_sample = markov[sample]
  values = [val[0] for val in this_sample]
  probabilities = [val[1] for val in this_sample]
  bins = np.add.accumulate(probabilities)
  song_index = np.digitize(random_sample(size), bins)
  return (values[song_index], probabilities[song_index])

if __name__ == "__main__":
  main()
