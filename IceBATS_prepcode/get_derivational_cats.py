from rmh_extractor import RmhExtractor
import re

def make_filters():
    filters = {}
    with open('all_filters.txt') as f:
        for i in f:
            filters[i.rstrip()] = 1
    return filters
 

def get_freqs():
    #hattur = {}
    #domur = {}
    #ingur = {}
    #isti = {}
    #skapur = {}
    #andi = {}
    #ari = {}
    #leiki = {}

    #legur = {}
    #ottur = {}
    #ugur = {}
    #skur = {}
    fjol_for = {}
    si_for = {}
    
    #era = {}
    #ast = {}
    #na = {}
    #a = {}
    #ja = {}
    #va = {}

    #o_for = {}
    #mis_for = {}
    #or_for = {}
    #van_for = {}
    #tor_for = {}
    #and_for = {}
    
    filters = make_filters()
    check_corpus = RmhExtractor(folder='../../RMH')
    for word in check_corpus.extract(forms=True, lemmas=True, pos=True):
        if word.lemma.lower() in filters:
            continue
        if (not all(i.isalpha() or i == '-' for i in word.lemma)):
            continue
        if word.lemma[-1] == '-':
            continue
        if word.lemma[0] == '-':
            continue
        if re.search(r'[cqwz]', word.lemma.lower()):
            continue
        if word.pos.startswith('n') and word.pos.endswith('s'):
            continue
        else:
            #if word.pos.startswith('n'):
            #    continue
                #if word.lemma.lower().endswith('ari'):
                #    if word.lemma.lower() in ari:
                #        ari[word.lemma.lower()] += 1
                #    else:
                #        ari[word.lemma.lower()] = 1
                #if word.lemma.lower().endswith('leiki'):
                #    if word.lemma.lower() in leiki:
                #        leiki[word.lemma.lower()] += 1
                #    else:
                #        leiki[word.lemma.lower()] = 1
                #if word.lemma.lower().endswith('háttur'):
                #    if word.lemma.lower() in hattur:
                #        hattur[word.lemma.lower()] += 1
                #    else:
                #        hattur[word.lemma.lower()] = 1
                #if word.lemma.lower().endswith('dómur'):
                #    if word.lemma.lower() in domur:
                #        domur[word.lemma.lower()] += 1
                #    else:
                #        domur[word.lemma.lower()] = 1
                #if word.lemma.lower().endswith('ingur'):
                #    if word.lemma.lower() in ingur:
                #        ingur[word.lemma.lower()] += 1
                #    else:
                #        ingur[word.lemma.lower()] = 1
                #if word.lemma.lower().endswith('isti'):
                #    if word.lemma.lower() in isti:
                #        isti[word.lemma.lower()] += 1
                #    else:
                #        isti[word.lemma.lower()] = 1
                #if word.lemma.lower().endswith('skapur'):
                #    if word.lemma.lower() in skapur:
                #        skapur[word.lemma.lower()] += 1
                #    else:
                #        skapur[word.lemma.lower()] = 1
                #if word.lemma.lower().endswith('andi'):
                #    if word.lemma.lower() in andi:
                #        andi[word.lemma.lower()] += 1
                #    else:
                #        andi[word.lemma.lower()] = 1
            #elif word.pos.startswith('l'):
            #    continue
                #if word.lemma.lower().endswith('skur'):
                #    if word.lemma.lower() in skur:
                #        skur[word.lemma.lower()] += 1
                #    else:
                #        skur[word.lemma.lower()] = 1
                #if word.lemma.lower().endswith('legur'):
                #    if word.lemma.lower() in legur:
                #        legur[word.lemma.lower()] += 1
                #    else:
                #        legur[word.lemma.lower()] = 1
                #if word.lemma.lower().endswith('óttur'):
                #    if word.lemma.lower() in ottur:
                #        ottur[word.lemma.lower()] += 1
                #    else:
                #        ottur[word.lemma.lower()] = 1
                #if word.lemma.lower().endswith('ugur'):
                #    if word.lemma.lower() in ugur:
                #        ugur[word.lemma.lower()] += 1
                #    else:
                #        ugur[word.lemma.lower()] = 1  
                #if word.lemma.lower().startswith('ó'):
                #    if word.lemma.lower() in o_for:
                #        o_for[word.lemma.lower()] += 1
                #    else:
                #        o_for[word.lemma.lower()] = 1
                #if word.lemma.lower().startswith('van'):
                #    if word.lemma.lower() in van_for:
                #        van_for[word.lemma.lower()] += 1
                #    else:
                #        van_for[word.lemma.lower()] = 1              
            #elif word.pos.startswith('s'):
            #    if word.lemma.lower().endswith('ja'):
            #        if word.lemma.lower() in ja:
            #            ja[word.lemma.lower()] += 1
            #        else:
            #            ja[word.lemma.lower()] = 1
            #    if word.lemma.lower().endswith('va'):
            #        if word.lemma.lower() in va:
            #            va[word.lemma.lower()] += 1
            #        else:
            #            va[word.lemma.lower()] = 1                                        
#                if word.lemma.lower().endswith('a'):
#                    if word.lemma.lower() in a:
#                        a[word.lemma.lower()] += 1
#                    else:
#                        a[word.lemma.lower()] = 1
#                if word.lemma.lower().endswith('na'):
#                    if word.lemma.lower() in na:
#                        na[word.lemma.lower()] += 1
#                    else:
#                        na[word.lemma.lower()] = 1
                #if len(word.lemma) > 5:
                #    if word.lemma.lower().endswith('era'):
                #        if word.lemma.lower() in era:
                #            era[word.lemma.lower()] += 1
                #        else:
                #            era[word.lemma.lower()] = 1 
                #if word.lemma.lower().endswith('ast'):
                #    if word.lemma.lower() in ast:
                #        ast[word.lemma.lower()] += 1
                #    else:
                #        ast[word.lemma.lower()] = 1
#            if word.lemma.lower().startswith('tor'):
#                if word.lemma.lower() in tor_for:
#                    tor_for[word.lemma.lower()] += 1
#                else:
#                    tor_for[word.lemma.lower()] = 1  
#            if word.lemma.lower().startswith('and'):
#                if word.lemma.lower() in and_for:
#                    and_for[word.lemma.lower()] += 1
#                else:
#                    and_for[word.lemma.lower()] = 1  
#            if word.lemma.lower().startswith('mis'):
#                if word.lemma.lower() in mis_for:
#                    mis_for[word.lemma.lower()] += 1
#                else:
#                    mis_for[word.lemma.lower()] = 1  
#            if word.lemma.lower().startswith('ör'):
#                if word.lemma.lower() in or_for:
#                    or_for[word.lemma.lower()] += 1
#                else:
#                    or_for[word.lemma.lower()] = 1  
            if word.lemma.lower().startswith('fjöl'):
                if word.lemma.lower() in fjol_for:
                    fjol_for[word.lemma.lower()] += 1
                else:
                    fjol_for[word.lemma.lower()] = 1 
            if word.lemma.lower().startswith('sí'):
                if word.lemma.lower() in si_for:
                    si_for[word.lemma.lower()] += 1
                else:
                    si_for[word.lemma.lower()] = 1 
    return si_for, fjol_for
    #return hattur, domur, ingur, isti, skapur, andi, legur, ottur, ugur, era, ast, o_for, van_for, or_for, mis_for, ari, leiki, and_for, tor_for, a, na, skur, ja, va

def write_file():
    si_for, fjol_for = get_freqs()
#    hattur, domur, ingur, isti, skapur, andi, legur, ottur, ugur, era, ast, o_for, van_for, or_for, mis_for, ari, leiki, and_for, tor_for, a, na, skur, ja, va = get_freqs()
    #with open('ja_vidskeyti.freq','w', encoding='utf-8') as out:
    #    sorted_ja = {k: v for k, v in sorted(ja.items(),
    #                  key=lambda item: item[1], reverse=True)}
    #    for key, value in sorted_ja.items():
    #        out.write(key + ': ' + str(value) + '\n')
    #with open('va_vidskeyti.freq','w', encoding='utf-8') as out:
    #    sorted_va = {k: v for k, v in sorted(va.items(),
    #                  key=lambda item: item[1], reverse=True)}
    #    for key, value in sorted_va.items():
    #        out.write(key + ': ' + str(value) + '\n')

    #with open('ari_vidskeyti.freq','w', encoding='utf-8') as out:
    #    sorted_ari = {k: v for k, v in sorted(ari.items(),
    #                  key=lambda item: item[1], reverse=True)}
    #    for key, value in sorted_ari.items():
    #        out.write(key + ': ' + str(value) + '\n')
    #with open('leiki_vidskeyti.freq','w', encoding='utf-8') as out:
    #    sorted_leiki = {k: v for k, v in sorted(leiki.items(),
    #                  key=lambda item: item[1], reverse=True)}
    #    for key, value in sorted_leiki.items():
    #        out.write(key + ': ' + str(value) + '\n')        
    #with open('a_vidskeyti.freq','w', encoding='utf-8') as out:
    #    sorted_a = {k: v for k, v in sorted(a.items(),
    #                  key=lambda item: item[1], reverse=True)}
    #    for key, value in sorted_a.items():
    #        out.write(key + ': ' + str(value) + '\n')
    #with open('na_vidskeyti.freq','w', encoding='utf-8') as out:
    #    sorted_na = {k: v for k, v in sorted(na.items(),
    #                  key=lambda item: item[1], reverse=True)}
    #    for key, value in sorted_na.items():
    #        out.write(key + ': ' + str(value) + '\n')
    #with open('skur_vidskeyti.freq','w', encoding='utf-8') as out:
    #    sorted_skur = {k: v for k, v in sorted(skur.items(),
    #                  key=lambda item: item[1], reverse=True)}
    #    for key, value in sorted_skur.items():
    #        out.write(key + ': ' + str(value) + '\n')
    #with open('tor_forskeyti.freq','w', encoding='utf-8') as out:
    #    sorted_tor = {k: v for k, v in sorted(tor_for.items(),
    #                  key=lambda item: item[1], reverse=True)}
    #    for key, value in sorted_tor.items():
    #        out.write(key + ': ' + str(value) + '\n')
    #with open('and_forskeyti.freq','w', encoding='utf-8') as out:
    #    sorted_and = {k: v for k, v in sorted(and_for.items(),
    #                  key=lambda item: item[1], reverse=True)}
    #    for key, value in sorted_and.items():
    #        out.write(key + ': ' + str(value) + '\n')
#    with open('hattur_vidskeyti.freq','w', encoding='utf-8') as out:
#        sorted_hattur = {k: v for k, v in sorted(hattur.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_hattur.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('domur_vidskeyti.freq','w', encoding='utf-8') as out:
#        sorted_domur = {k: v for k, v in sorted(domur.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_domur.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('ingur_vidskeyti.freq','w', encoding='utf-8') as out:
#        sorted_ingur = {k: v for k, v in sorted(ingur.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_ingur.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('isti_vidskeyti.freq','w', encoding='utf-8') as out:
#        sorted_isti = {k: v for k, v in sorted(isti.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_isti.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('skapur_vidskeyti.freq','w', encoding='utf-8') as out:
#        sorted_skapur = {k: v for k, v in sorted(skapur.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_skapur.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('andi_vidskeyti.freq','w', encoding='utf-8') as out:
#        sorted_andi = {k: v for k, v in sorted(andi.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_andi.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('legur_vidskeyti.freq','w', encoding='utf-8') as out:
#        sorted_legur = {k: v for k, v in sorted(legur.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_legur.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('ottur_vidskeyti.freq','w', encoding='utf-8') as out:
#        sorted_ottur = {k: v for k, v in sorted(ottur.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_ottur.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('ugur_vidskeyti.freq','w', encoding='utf-8') as out:
#        sorted_ugur = {k: v for k, v in sorted(ugur.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_ugur.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('era_vidskeyti.freq','w', encoding='utf-8') as out:
#        sorted_era = {k: v for k, v in sorted(era.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_era.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('ast_vidskeyti.freq','w', encoding='utf-8') as out:
#        sorted_ast = {k: v for k, v in sorted(ast.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_ast.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('o_forskeyti.freq','w', encoding='utf-8') as out:
#        sorted_o_for = {k: v for k, v in sorted(o_for.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_o_for.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('van_forskeyti.freq','w', encoding='utf-8') as out:
#        sorted_van_for = {k: v for k, v in sorted(van_for.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_van_for.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('or_forskeyti.freq','w', encoding='utf-8') as out:
#        sorted_or_for = {k: v for k, v in sorted(or_for.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_or_for.items():
#            out.write(key + ': ' + str(value) + '\n')
#    with open('mis_forskeyti.freq','w', encoding='utf-8') as out:
#        sorted_mis_for = {k: v for k, v in sorted(mis_for.items(),
#                      key=lambda item: item[1], reverse=True)}
#        for key, value in sorted_mis_for.items():
#            out.write(key + ': ' + str(value) + '\n')
    with open('si_forskeyti.freq','w', encoding='utf-8') as out:
        sorted_si_for = {k: v for k, v in sorted(si_for.items(),
                      key=lambda item: item[1], reverse=True)}
        for key, value in sorted_si_for.items():
            out.write(key + ': ' + str(value) + '\n')

    with open('fjol_forskeyti.freq','w', encoding='utf-8') as out:
        sorted_fjol_for = {k: v for k, v in sorted(fjol_for.items(),
                      key=lambda item: item[1], reverse=True)}
        for key, value in sorted_fjol_for.items():
            out.write(key + ': ' + str(value) + '\n')
write_file()