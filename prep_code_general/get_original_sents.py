from rmh_extractor import RmhExtractor
from string import punctuation

def extract_sents():
    corpus = RmhExtractor(folder='../RMH')
    sent_end = ['.', '?', '!']
    with open('all_sentences_lower.txt', 'w', encoding='utf-8') as out:
        for word in corpus.extract(forms=True, lemmas=True, pos=True):
            if word.word_form in sent_end:
                out.write('\n')
            else:
                if word.pos.startswith('n') and word.pos.endswith('s'):
                    out.write(word.word_form + ' ')
                else:
                    out.write(word.word_form.lower() + ' ')

extract_sents()