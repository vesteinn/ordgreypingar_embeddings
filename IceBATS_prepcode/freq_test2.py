"""A very simple script that compares the word pairs in IceBATS to
a list of frequencies from the Icelandic Gigaword Corpus in order
to evaluate which pairs can be used for testing"""

import glob
import numpy as np

files = glob.glob('../IceBATS/final/*/*.txt', recursive=True)

vocab = []

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        for i in f:
            word1, word2 = i.rstrip().split()
            vocab.append(word1)
            word2 = word2.rstrip().split('/')
            for i in word2:
                vocab.append(i)

print(len(set(vocab)))

freqs = []
#with open('all_lemmas.freq') as f2:
with open('all_wordforms.freq') as f2:
    for i in f2:
        w, fr = i.rstrip().split(':')
        freqs.append((w,fr))

low = 0
medium = 0
high = 0
superhigh = 0
inlist = []

for w in freqs:
    if w[0] in vocab:
        if int(w[1]) in range(100,500):
            low += 1
            inlist.append(w[0])
        elif int(w[1]) in range(500,1000):
            medium += 1
            inlist.append(w[0])
        elif int(w[1]) in range (1000,10000):
            high += 1
            inlist.append(w[0])
        elif int(w[1]) > 10000:
            superhigh += 1
            inlist.append(w[0])

print(low, medium, high, superhigh)

print(len(list(np.setdiff1d(vocab,inlist))))