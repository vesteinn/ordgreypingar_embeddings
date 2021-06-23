with open('all_sentences_lower_lemmatized.txt', 'r') as f:
    with open('all_sentences_lower_lemmatized_oneline.txt', 'w+') as out:
        for line in f:
            out.write(line.rstrip()+' ')