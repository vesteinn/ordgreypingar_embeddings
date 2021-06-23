from rmh_extractor import RmhExtractor

def extract_sents():
    corpus = RmhExtractor(folder='../RMH')
    sent_end = ['.', '?', '!']
    with open('all_sentences_lower_lemmatized.txt', 'w', encoding='utf-8') as out:
        for word in corpus.extract(forms=True, lemmas=True, pos=True):
            if word.word_form in sent_end:
                out.write('\n')
            else:
                if word.pos.startswith('n') and word.pos.endswith('s'):
                    out.write(word.lemma + ' ')
                else:
                    out.write(word.lemma.lower() + ' ')

extract_sents()