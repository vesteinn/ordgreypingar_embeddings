vocab = []
with open('FrankenBATS/final/inflectional/nouns_plur_article.txt') as f:
    for i in f:
        word1, word2 = i.rstrip().split()
        vocab.append(word1)
        word2 = word2.rstrip().split('/')
        for i in word2:
            vocab.append(i)

freqs = []
freqs1 = []
#with open('all_lemmas_300k.freq') as f2:
with open('all_wordforms.freq') as f2:
    for i in f2:
        w, fr = i.rstrip().split(':')
        freqs.append((w,fr))
        freqs1.append(w)

count=0
for w in freqs:
    if w[0] in vocab:
        print(w)
        count+=1
print(len(vocab))
print(count)

for w in vocab:
    if w in freqs1:
        continue
    else:
        print(w)

