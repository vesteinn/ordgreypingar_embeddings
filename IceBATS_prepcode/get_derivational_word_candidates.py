import random

def get_lists():
    """This function collects frequency information from the 
    100.000 top frequent words from the Gigaword corpus as 
    well as making wordlists from each subcategory"""

    print("Collecting lemma frequency information")

    all_words_original = {}
    with open('all_lemmas_300k.freq') as f:
        for num, line in enumerate(f, 1):
            word = line.rstrip().split()
            w = word[0][:-1]
            all_words_original[w] = num
    all_words = {k: v for k, v in sorted(all_words_original.items(), key=lambda item: item[1], reverse=False)}
    
    print("Collecting derivational wordlists")

    andi = []
    with open('andi_vidskeyti.freq') as f:
        for i in f:
            i = i.split()
            andi.append(i[0][:-1].rstrip())
    ast = []
    with open('ast_vidskeyti.freq') as f:
        for i in f:
            i = i.split()
            ast.append(i[0][:-1].rstrip())
    domur = []
    with open('domur_vidskeyti.freq') as f:
        for i in f:
            i = i.split()
            domur.append(i[0][:-1].rstrip())
    era = []
    with open('era_vidskeyti.freq') as f:
        for i in f:
            i = i.split()
            era.append(i[0][:-1].rstrip())
    hattur = []
    with open('hattur_vidskeyti.freq') as f:
        for i in f:
            i = i.split()
            hattur.append(i[0][:-1].rstrip())
    ingur = []
    with open('ingur_vidskeyti.freq') as f:
        for i in f:
            i = i.split()
            ingur.append(i[0][:-1].rstrip())
    isti = []
    with open('isti_vidskeyti.freq') as f:
        for i in f:
            i = i.split()
            isti.append(i[0][:-1].rstrip())
    legur = []
    with open('legur_vidskeyti.freq') as f:
        for i in f:
            i = i.split()
            legur.append(i[0][:-1].rstrip())
    ottur = []
    with open('ottur_vidskeyti.freq') as f:
        for i in f:
            i = i.split()
            ottur.append(i[0][:-1].rstrip())
    skapur = []
    with open('skapur_vidskeyti.freq') as f:
        for i in f:
            i = i.split()
            skapur.append(i[0][:-1].rstrip())
    ugur = []
    with open('ugur_vidskeyti.freq') as f:
        for i in f:
            i = i.split()
            ugur.append(i[0][:-1].rstrip())
    mis_for = []
    with open('mis_forskeyti.freq') as f:
        for i in f:
            i = i.split()
            mis_for.append(i[0][:-1].rstrip())    
    o_for = []
    with open('o_forskeyti.freq') as f:
        for i in f:
            i = i.split()
            o_for.append(i[0][:-1].rstrip())    
    or_for = []
    with open('or_forskeyti.freq') as f:
        for i in f:
            i = i.split()
            or_for.append(i[0][:-1].rstrip())    
    van_for = []
    with open('van_forskeyti.freq') as f:
        for i in f:
            i = i.split()
            van_for.append(i[0][:-1].rstrip())    

    return [all_words, hattur, domur, ingur, isti, skapur, andi, legur, ottur, ugur, era, ast, o_for, van_for, or_for, mis_for]


def candidates():
    """Categorizes candidates by frequency within the IGC. Writes out
    files containing 200 candidates per category, 10% from the most
    and least frequent range and 80% from the middle range."""
    
    candidates = get_lists()

    print("Collecting candidate frequency information from the IGC")

    num = 1
    for i in candidates[1:]:
        all_words = candidates[0]
        candidates_out = []

        most_freq = []
        second_freq = []
        least_freq = []
        
        for word in i[:1000]:
            for k, v in all_words.items():
                if int(v) < 50000:
                    if k == word:
                        most_freq.append(k)
                elif 50000 <= int(v) <= 150000:
                    if k == word:
                        second_freq.append(k)
                else:
                    if k == word:
                        least_freq.append(k)
    
        candidates_out.append("ALGENGUST \n")
        for word in most_freq:
            candidates_out.append(word)
        candidates_out.append("\n MIÐJA \n")
        for word in second_freq:
            candidates_out.append(word)
        candidates_out.append("\n SJALDGÆFUST \n")
        for word in least_freq:
            candidates_out.append(word)
       
        with open('FrankenBATS/'+str(num)+'_final.txt', 'w+') as out:
            for i in candidates_out:
                out.write(i+'\n')
        print("File "+str(num)+" of "+str(len(candidates[1:]))+" done")
        num += 1
        

candidates()