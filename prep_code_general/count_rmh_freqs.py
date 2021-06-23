from rmh_extractor import RmhExtractor
from string import punctuation

def count_freqs():
    freqs = {}
    corpus = RmhExtractor(folder='../RMH')
    for word in corpus.extract(forms=True, lemmas=True, pos=True):
        if word.lemma in freqs:
            freqs[word.lemma] += 1
        else:
            freqs[word.lemma] = 1
    return freqs

def writeout():
    with open('all_lemmas.freq', 'w+', encoding='utf8') as out:
        freqs = count_freqs()
        freqs = {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)}
        for key, value in freqs.items():
            if value > 1:
                out.write(key+" : "+str(value)+"\n")

writeout()