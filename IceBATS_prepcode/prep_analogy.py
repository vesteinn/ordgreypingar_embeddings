"""Goes through the individual files containing the word pairs
for IceBATS and writes out a joint file with all possible 
combinations of the pairs"""

import glob
from progress.bar import IncrementalBar
import sys

files = glob.glob('../IceBATS/final/lexicographic/*.txt', recursive=True)

filebar = IncrementalBar('Inntaksskjöl lesin', max = len(files))
cat_dict = {}
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        cat = []
        for i in f: 
            i = i.rstrip().split()
            cat.append(i[0]+" "+i[1])
        cat_dict[file.split('/')[-1][:-4]] = cat 
    filebar.next()
    sys.stdout.flush()
filebar.finish()

with open('analogy_lexicographic.txt', 'w+') as out:
    for cat, word_list in cat_dict.items():
        out.write(': '+ cat +'\n')
        for wp in word_list:
            for i in range(len(word_list[:50])):
                if wp == word_list[i]:
                    continue
                else:
                    out.write(wp+" "+word_list[i]+'\n')