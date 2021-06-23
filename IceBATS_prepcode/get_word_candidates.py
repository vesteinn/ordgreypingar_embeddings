import random

def get_lists():
    """This function collects frequency information from the 
    100.000 top frequent words from the Gigaword corpus as 
    well as making wordlists from each subcategory"""

    print("Collecting lemma frequency information")

    all_words_original = {}
    with open('all_lemmas_clean.freq') as f:
        for num, line in enumerate(f, 1):
            word = line.rstrip().split()
            w = word[0][:-1]
            all_words_original[w] = num
    all_words = {k: v for k, v in sorted(all_words_original.items(), key=lambda item: item[1], reverse=False)}
    
    print("Collecting POS wordlists")

    sterk_no = []
    with open('sterk_beyging_nafnord.txt') as f:
        for i in f:
            sterk_no.append(i.rstrip())

    veik_no = []
    with open('veik_beyging_nafnord.txt') as f:
        for i in f:
            veik_no.append(i.rstrip())

    sterk_so = []
    with open('sterk_beyging_sagnord.txt') as f:
        for i in f:
            sterk_so.append(i.rstrip())

    veik_so = []
    with open('veik_beyging_sagnord.txt') as f:
        for i in f:
            veik_so.append(i.rstrip())
    
    bland_so = []
    with open('lemmas_blandadar_sagnir.freq') as f:
        for i in f:
            i = i.split()
            bland_so.append(i[0])

    sterk_lo = []
    with open('sterk_beyging_lysingarord.txt') as f:
        for i in f:
            sterk_lo.append(i.rstrip())
    
    veik_lo = []
    with open('veik_beyging_lysingarord.txt') as f:
        for i in f:
            veik_lo.append(i.rstrip())
    
    obeygd_lo = []
    with open('obeygd_lysingarord.txt') as f:
        for i in f:
            obeygd_lo.append(i.rstrip())

    return all_words, sterk_no, veik_no, sterk_so, veik_so, bland_so, sterk_lo, veik_lo, obeygd_lo

def nouns(all_words,sterk_no, veik_no):
    """Categorizes nouns by frequency within the IGC. Writes 
    out a file containing 400 random nouns (24% weak 76% strong declension), 
    with approx 80% coming from the selected frequency range."""
    
    print("Collecting noun frequency information from the IGC")

    nouns_out = []
    
    most_freq_sterk = []
    second_freq_sterk = []
    least_freq_sterk = []
    most_freq_veik = []
    second_freq_veik = []
    least_freq_veik = []
    for word in sterk_no[:4000]:
        for i, k in all_words.items():
            if int(k) < 2000:
                if i == word:
                    most_freq_sterk.append(i)
            elif 2000 <= int(k) <= 20000:
                if i == word:
                    second_freq_sterk.append(i)
            else:
                if i == word:
                    least_freq_sterk.append(i)

    for word in veik_no[:4000]:
        for i, k in all_words.items():
            if int(k) < 2000:
                if i == word:
                    most_freq_veik.append(i)
            elif 2000 <= int(k) <= 20000:
                if i == word:
                    second_freq_veik.append(i)
            else:
                if i == word:
                    least_freq_veik.append(i)
    
    print("Writing out noun file")

    nouns_out.append("STERK ALGENGUST \n")
    for word in random.sample(most_freq_sterk, k=32):
        nouns_out.append(word)
    nouns_out.append("\n STERK MIÐJA \n")
    for word in random.sample(second_freq_sterk, k=240):
        nouns_out.append(word)
    nouns_out.append("\n STERK SJALDGÆFUST \n")
    for word in random.sample(least_freq_sterk, k=32):
        nouns_out.append(word)
    nouns_out.append("\n VEIK ALGENGUST \n")
    for word in random.sample(most_freq_veik, k=12):
        nouns_out.append(word)
    nouns_out.append("\n VEIK MIÐJA \n")
    for word in random.sample(second_freq_veik, k=72):
        nouns_out.append(word)
    nouns_out.append("\n VEIK SJALDGÆFUST \n")
    for word in random.sample(least_freq_veik, k=12):
        nouns_out.append(word)

    with open('nafnord_final.txt', 'w+') as out:
        for i in nouns_out:
            out.write(i+'\n')

def verbs(all_words, sterk_so, veik_so, bland_so):
    """Categorizes verbs by frequency within the IGC. Writes 
    out a file containing 400 random verbs (3.5% mixed 51.5% weak 
    45% strong declension), with approx 80% coming from the 
    selected frequency range."""

    print("Collecting verb frequency information from the IGC")

    verbs_out = []
    
    most_freq_sterk = []
    second_freq_sterk = []
    least_freq_sterk = []
    most_freq_veik = []
    second_freq_veik = []
    least_freq_veik = []
    most_freq_bland = []
    second_freq_bland = []
    least_freq_bland = []
    for word in sterk_so[:4000]:
        for i, k in all_words.items():
            if int(k) < 2000:
                if i == word:
                    most_freq_sterk.append(i)
            elif 2000 <= int(k) <= 20000:
                if i == word:
                    second_freq_sterk.append(i)
            else:
                if i == word:
                    least_freq_sterk.append(i)

    for word in veik_so[:4000]:
        for i, k in all_words.items():
            if int(k) < 2000:
                if i == word:
                    most_freq_veik.append(i)
            elif 2000 <= int(k) <= 20000:
                if i == word:
                    second_freq_veik.append(i)
            else:
                if i == word:
                    least_freq_veik.append(i)

    for word in bland_so:
        for i, k in all_words.items():
            if int(k) < 2000:
                if i == word:
                    most_freq_bland.append(i)
            elif 2000 <= int(k) <= 20000:
                if i == word:
                    second_freq_bland.append(i)
            else:
                if i == word:
                    least_freq_bland.append(i)
    
    print("Writing out verb file")

    verbs_out.append("STERK ALGENGUST \n")
    for word in random.sample(most_freq_sterk, k=16):
        verbs_out.append(word)
    verbs_out.append("\n STERK MIÐJA \n")
    for word in random.sample(second_freq_sterk, k=144):
        verbs_out.append(word)
    verbs_out.append("\n STERK SJALDGÆFUST \n")
    for word in random.sample(least_freq_sterk, k=16):
        verbs_out.append(word)
    verbs_out.append("\n VEIK ALGENGUST \n")
    for word in random.sample(most_freq_veik, k=16):
        verbs_out.append(word)
    verbs_out.append("\n VEIK MIÐJA \n")
    for word in random.sample(second_freq_veik, k=164):
        verbs_out.append(word)
    verbs_out.append("\n VEIK SJALDGÆFUST \n")
    for word in random.sample(least_freq_veik, k=16):
        verbs_out.append(word)
    verbs_out.append("\n BLAND ALGENGUST \n")
    for word in most_freq_bland:
        verbs_out.append(word)
    verbs_out.append("\n BLAND MIÐJA \n")
    for word in second_freq_bland:
        verbs_out.append(word)
    verbs_out.append("\n BLAND SJALDGÆFUST \n")
    for word in least_freq_bland:
        verbs_out.append(word)

    with open('sagnord_final.txt', 'w+') as out:
        for i in verbs_out:
            out.write(i+'\n')


def adjectives(all_words, sterk_lo, veik_lo, obeygd_lo):
    """Categorizes adjectives by frequency within the IGC. Writes 
    out a file containing 400 random adjectives (5% indeclinable 72% weak 
    23% strong declension), with approx 80% coming from the 
    selected frequency range."""
    
    print("Collecting adjective frequency information from the IGC")

    adjectives_out = []
    
    most_freq_sterk = []
    second_freq_sterk = []
    least_freq_sterk = []
    most_freq_veik = []
    second_freq_veik = []
    least_freq_veik = []
    most_freq_obeygd = []
    second_freq_obeygd = []
    least_freq_obeygd = []
    for word in sterk_lo[:4000]:
        for i, k in all_words.items():
            if int(k) < 2000:
                if i == word:
                    most_freq_sterk.append(i)
            elif 2000 <= int(k) <= 20000:
                if i == word:
                    second_freq_sterk.append(i)
            else:
                if i == word:
                    least_freq_sterk.append(i)

    for word in veik_lo[:4000]:
        for i, k in all_words.items():
            if int(k) < 2000:
                if i == word:
                    most_freq_veik.append(i)
            elif 2000 <= int(k) <= 20000:
                if i == word:
                    second_freq_veik.append(i)
            else:
                if i == word:
                    least_freq_veik.append(i)

    for word in obeygd_lo:
        for i, k in all_words.items():
            if int(k) < 2000:
                if i == word:
                    most_freq_obeygd.append(i)
            elif 2000 <= int(k) <= 20000:
                if i == word:
                    second_freq_obeygd.append(i)
            else:
                if i == word:
                    least_freq_obeygd.append(i)
    print("Writing out adjective file")
    
    adjectives_out.append("STERK ALGENGUST \n")
    for word in random.sample(most_freq_sterk, k=24):
        adjectives_out.append(word)
    adjectives_out.append("\n STERK MIÐJA \n")
    for word in random.sample(second_freq_sterk, k=216):
        adjectives_out.append(word)
    adjectives_out.append("\n STERK SJALDGÆFUST \n")
    for word in random.sample(least_freq_sterk, k=24):
        adjectives_out.append(word)
    adjectives_out.append("\n VEIK ALGENGUST \n")
    for word in random.sample(most_freq_veik, k=12):
        adjectives_out.append(word)
    adjectives_out.append("\n VEIK MIÐJA \n")
    for word in random.sample(second_freq_veik, k=80):
        adjectives_out.append(word)
    adjectives_out.append("\n VEIK SJALDGÆFUST \n")
    for word in random.sample(least_freq_veik, k=12):
        adjectives_out.append(word)
    adjectives_out.append("\n ÓBEYGÐ ALGENGUST \n")
    for word in random.sample(most_freq_obeygd, k=8):
        adjectives_out.append(word)
    adjectives_out.append("\n ÓBEYGÐ MIÐJA \n")
    for word in random.sample(second_freq_obeygd, k=16):
        adjectives_out.append(word)
    adjectives_out.append("\n ÓBEYGÐ SJALDGÆFUST \n")
    for word in random.sample(least_freq_obeygd, k=8):
        adjectives_out.append(word)

    with open('lysingarord_final.txt', 'w+') as out:
        for i in adjectives_out:
            out.write(i+'\n')

all_words, sterk_no, veik_no, sterk_so, veik_so, bland_so, sterk_lo, veik_lo, obeygd_lo = get_lists()
nouns(all_words, sterk_no, veik_no)
verbs(all_words, sterk_so, veik_so, bland_so)
adjectives(all_words, sterk_lo, veik_lo, obeygd_lo)
print("Finished")