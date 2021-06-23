def main():
    """Collects information from the IGC regarding specific word categories.
    For each category, information on strong and weak declension is collected,
    as well as additional declension categories for adjectives and verbs.
    Additionally, information regarding gender, grading, mood etc. is 
    collected for research purposes. Each declension type for each wc 
    can be written out as txt files if desired (necessary for 
    get_word_candidates.py)"""

    with open('filtered_nouns_with_lemmas.freq') as f:
        allt = []
        med_greini = []
        an_greinis = []
        nefnifall = []
        tholfall = []
        thagufall = []
        eignarfall = []
        kvenkyn = []
        karlkyn = []
        hvorugkyn = []
        sterk_no = []
        veik_no = []
        for i in f:
            word = i.rstrip().split()
            if int(word[4]) > 78:
                allt.append(word)
                try:
                    if word[1][4] == 'g':
                        med_greini.append(word)
                    else:
                        an_greinis.append(word)
                except IndexError:
                    an_greinis.append(word)
                if word[1][3] == 'n':
                    nefnifall.append(word)
                elif word[1][3] == 'o':
                    tholfall.append(word)
                elif word[1][3] == 'þ':
                    thagufall.append(word)
                elif word[1][3] == 'e':
                    eignarfall.append(word)
                    if word[1][2] == 'e':
                        if word[0].endswith('s'):
                            if word[2] in sterk_no:
                                continue
                            else:
                                sterk_no.append(word[2])
                        elif word[0].endswith('r'):
                            if word[2] in sterk_no:
                                continue
                            else:
                                sterk_no.append(word[2])
                        else:
                            if word[2] in veik_no:
                                continue
                            else:
                                veik_no.append(word[2])
                if word[1][1] == 'k':
                    karlkyn.append(word)
                elif word[1][1] == 'v':
                    kvenkyn.append(word)
                elif word[1][1] == 'h':
                    hvorugkyn.append(word)

        print("Nafnorð")
        print("Hlutfall með greini: ", round(len(med_greini)/len(allt),3))
        print("Hlutfall án greinis: ", round(len(an_greinis)/len(allt),3))
        print("Hlutfall nefnifall: ", round(len(nefnifall)/len(allt),3))
        print("Hlutfall þolfall: ", round(len(tholfall)/len(allt),3))
        print("Hlutfall þágufall: ", round(len(thagufall)/len(allt),3))
        print("Hlutfall eignarfall: ", round(len(eignarfall)/len(allt),3))
        print("Hlutfall karlkyn: ", round(len(karlkyn)/len(allt),3))
        print("Hlutfall kvenkyn: ", round(len(kvenkyn)/len(allt),3))
        print("Hlutfall hvorugkyn: ", round(len(hvorugkyn)/len(allt),3))
        print("Hlutfall veik beyging: ", round(len(veik_no)/(len(veik_no)+len(sterk_no)),3))
        print("Hlutfall sterk beyging: ", round(len(sterk_no)/(len(sterk_no)+len(veik_no,)),3))
        print()

#        with open('veik_beyging_nafnord.txt', 'w+') as out:
#            for i in veik_no:
#                out.write(i+'\n')
#
#        with open('sterk_beyging_nafnord.txt', 'w+') as out:
#            for i in sterk_no:
#                out.write(i+'\n')

    with open('filtered_adjectives_with_lemmas.freq') as f:
        allt = []
        veik_beyging = []
        sterk_beyging = []
        obeygd = []
        karlkyn = []
        kvenkyn = []
        hvorugkyn = []
        frumstig = []
        midstig = []
        efstastig = []
        for i in f:
            word = i.rstrip().split()
            if int(word[4]) > 7:
                allt.append(word)
                if word[1][4] == 'v':
                    if word[2] in veik_beyging: #to write out, change to word[0]
                        continue
                    else:
                        veik_beyging.append(word[2]) #to write out, change to word[0]
                elif word[1][4] == 's':
                    if word[2] in sterk_beyging:
                        continue
                    else:
                        sterk_beyging.append(word[2])
                elif word[1][4] == 'o':
                    if word[2] in obeygd:
                        continue
                    else:
                        obeygd.append(word[2])
                if word[1][5] == 'f':
                    frumstig.append(word)
                elif word[1][5] == 'm':
                    midstig.append(word)
                elif word[1][5] == 'e':
                    efstastig.append(word)
                if word[1][1] == 'k':
                    karlkyn.append(word)
                elif word[1][1] == 'v':
                    kvenkyn.append(word)
                elif word[1][1] == 'h':
                    hvorugkyn.append(word)
    
#        with open('veik_beyging_lysingarord.txt', 'w+') as out:
#            for i in veik_beyging:
#                out.write(i+'\n')
#
#        with open('sterk_beyging_lysingarord.txt', 'w+') as out:
#            for i in sterk_beyging:
#                out.write(i+'\n')
#
#        with open('obeygd_lysingarord.txt', 'w+') as out:
#            for i in obeygd:
#                out.write(i+'\n')
#
        print('Lýsingarorð')
        print('Hlutfall veikrar beygingar: ', round(len(veik_beyging)/(len(veik_beyging)+len(sterk_beyging)+len(obeygd)), 3))
        print('Hlutfall sterkrar beygingar: ', round(len(sterk_beyging)/(len(veik_beyging)+len(sterk_beyging)+len(obeygd)), 3))
        print('Hlutfall óbeygjanleg: ', round(len(obeygd)/(len(veik_beyging)+len(sterk_beyging)+len(obeygd)), 3))
        print("Hlutfall frumstig: ", round(len(frumstig)/(len(frumstig)+len(midstig)+len(efstastig)),3))
        print("Hlutfall miðstig: ", round(len(midstig)/(len(frumstig)+len(midstig)+len(efstastig)),3))
        print("Hlutfall efstastig: ", round(len(efstastig)/(len(frumstig)+len(midstig)+len(efstastig)),3))
        print("Hlutfall karlkyn: ", round(len(karlkyn)/(len(karlkyn)+len(kvenkyn)+len(hvorugkyn)),3))
        print("Hlutfall kvenkyn: ", round(len(kvenkyn)/(len(karlkyn)+len(kvenkyn)+len(hvorugkyn)),3))
        print("Hlutfall hvorugkyn: ", round(len(hvorugkyn)/(len(karlkyn)+len(kvenkyn)+len(hvorugkyn)),3))
        print()

    with open('filtered_verbs_with_lemmas.freq') as f:
        allt = []
        veik_beyging = []
        sterk_beyging = []
        tags = {}
        framsoguhattur = []
        vidtengingarhattur = []
        nafnhattur = []
        lysingarhattur_thatidar = []
        lysingarhattur_nutidar = []
        bodhattur = []
        sagnbot = []
        for i in f:
            word = i.rstrip().split()
            if int(word[4]) > 0:
                allt.append(word)
                if word[1] in tags:
                    tags[word[1]] += 1
                else:
                    tags[word[1]] = 1
                if word[1][1] == 'f':
                    framsoguhattur.append(word)
                elif word[1][1] == 'v':
                    vidtengingarhattur.append(word)
                elif word[1][1] == 'n':
                    nafnhattur.append(word)
                elif word[1][1] == 'þ':
                    lysingarhattur_thatidar.append(word)
                elif word[1][1] == 'l':
                    lysingarhattur_nutidar.append(word)
                elif word[1][1] == 'b':
                    bodhattur.append(word)
                if word[1] == 'sfg1eþ':
                    if word[2] in veik_beyging:
                        continue
                    else:
                        if word[0].endswith('di'):
                            veik_beyging.append(word[2])
                        elif word[0].endswith('ði'):
                            veik_beyging.append(word[2])
                        elif word[0].endswith('ti'):
                            veik_beyging.append(word[2])
                        else:
                            sterk_beyging.append(word[2])
                if word[1] == 'sfg2eþ':
                    if word[2] in sterk_beyging:
                        continue
                    else:
                        if word[0].endswith('st'):
                            sterk_beyging.append(word[2])
                        else:
                            if word[2] in veik_beyging:
                                continue
                            else:
                                veik_beyging.append(word[2])
                if word[1] == 'sfg3eþ':
                    if word[2] in veik_beyging:
                        continue
                    else:
                        if word[0].endswith('di'):
                            veik_beyging.append(word[2])
                        elif word[0].endswith('ði'):
                            veik_beyging.append(word[2])
                        elif word[0].endswith('ti'):
                            veik_beyging.append(word[2])
                        else:
                            if word[2] in sterk_beyging:
                                continue
                            else:
                                sterk_beyging.append(word[2])
                if word[1] == 'svg1eþ':
                    if word[2] in veik_beyging:
                        continue
                    else:
                        if word[0].endswith('di'):
                            veik_beyging.append(word[2])
                        elif word[0].endswith('ði'):
                            veik_beyging.append(word[2])
                        elif word[0].endswith('ti'):
                            veik_beyging.append(word[2])
                        else:
                            if word[2] in sterk_beyging:
                                continue
                            else:
                                sterk_beyging.append(word[2])
                if word[1] == 'svg2eþ':
                    if word[2] in sterk_beyging:
                        continue
                    else:
                        if word[0].endswith('st'):
                            sterk_beyging.append(word[2])
                        else:
                            if word[2] in veik_beyging:
                                continue
                            else:
                                veik_beyging.append(word[2])
                if word[1] == 'svg3eþ':
                    if word[2] in veik_beyging:
                        continue
                    else:
                        if word[0].endswith('di'):
                            veik_beyging.append(word[2])
                        elif word[0].endswith('ði'):
                            veik_beyging.append(word[2])
                        elif word[0].endswith('ti'):
                            veik_beyging.append(word[2])
                        else:
                            if word[2] in sterk_beyging:
                                continue
                            else:
                                sterk_beyging.append(word[2])

        sorted_tags = {k: v for k, v in sorted(tags.items(),
                  key=lambda item: item[1], reverse=True)}
        print("Sagnorð")
        print("Hlutfall framsöguháttur: ", round(len(framsoguhattur)/len(allt), 3))
        print("Hlutfall viðtengingarháttur: ", round(len(vidtengingarhattur)/len(allt),3))
        print("Hlutfall nafnháttur: ", round(len(nafnhattur)/len(allt),3))
        print("Hlutfall lýsingarháttur þátíðar: ", round(len(lysingarhattur_thatidar)/len(allt),3))
        print("Hlutfall lýsingarháttur nútíðar: ", round(len(lysingarhattur_nutidar)/len(allt),3))
        print("Hlutfall boðháttur: ", round(len(bodhattur)/len(allt),3))
        print("Hlutfall sterk beyging: ", round(len(sterk_beyging) / (len(sterk_beyging)+len(veik_beyging)+15),3))
        print("Hlutfall veik beyging: ", round(len(veik_beyging) / (len(sterk_beyging)+len(veik_beyging)+15),3))

#        with open('sterk_beyging_sagnord.txt', 'w+') as out:
#            for i in sterk_beyging:
#                out.write(i+'\n')
#        with open('veik_beyging_sagnord.txt', 'w+') as out:
#            for i in veik_beyging:
#                out.write(i+'\n')

main()