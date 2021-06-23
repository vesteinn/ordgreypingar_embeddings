'''
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

glove_file = datapath('vectors_rmh_glove.txt')
tmp_file = get_tmpfile("vectors_rmh_w2v.txt")
_ = glove2word2vec(glove_file, tmp_file)
model = KeyedVectors.load_word2vec_format(tmp_file)
'''
import operator
import gensim
from gensim.models import KeyedVectors
from test_analogies import evaluate_word_analogies_mod
import logging
from scipy import stats
import os
import numpy as np
from sklearn.decomposition import PCA
import copy
from datetime import datetime
import sys

# INPUT
# echo "$ $PYTHON glove_msl.py -$VOCAB_MIN_COUNT -$VECTOR_SIZE -$WINDOW_SIZE -$X_MAX"

# DOCUMENTATION
# https://www.rdocumentation.org/packages/text2vec/versions/0.5.1/topics/GlobalVectors
# x_max: integer maximum number of co-occurrences to use in the weighting function. see the GloVe paper for details: http://nlp.stanford.edu/pubs/glove.pdf
# https://www.tutorialexample.com/best-practice-to-create-word-embeddings-using-glove-deep-learning-tutorial/
# VOCAB_MIN_COUNT=5 # the min count [i.e. frequency] of a word in vocabulary file
# https://stackoverflow.com/questions/55584776/the-meaning-of-hyperparameters-in-glove
# WINDOW_SIZE: yes, it's the context size (check: https://github.com/stanfordnlp/GloVe/blob/master/src/cooccur.c)
# i.e. If WINDOW_SIZE is 15, choose 15 words from right and choose 15 words from left


INPUT_FILENAME = "vectors_rmh_glove_w2v.txt"
#INPUT_FILENAME = "vectors_rmh_glove_w2v.txt"
#INPUT_FILENAME = "vectors_bylgjan_w2v.txt"

CSV_DER = 0
CSV_INF = 1
CSV_ENC = 2
CSV_LEX = 3
CSV_MSL1 = 4
CSV_MSL2 = 5
CSV_MSL3 = 6
CSV_MSL4 = 7
CSV_MSL5 = 8
CSV_MSL1253 = 9
CSV_MSL1254 = 10
CSV_VOC_MINCOUNT = 11
CSV_VECTOR_SIZE = 12
CSV_EPOCH = 13
CSV_WIN_SIZE = 14
CSV_X_MAX = 15

# Loads a dictionary with key tuple (word1, word2) and value its average score scaled to [0,1]
# Input file has tab-separated lines with word1, word2, original average, scaled average
def load_msl(input_filename):
    input_dict = dict()
    with open(input_filename, "r", encoding="utf8") as f_in:
        for line in f_in:
            line_tab = line.split("\t")
            key_tup = (line_tab[0], line_tab[1])
            val = float(line_tab[3])
            input_dict[key_tup] = val
    return input_dict


def load_vectors():
    load_vec = gensim.models.keyedvectors.Word2VecKeyedVectors.load_word2vec_format(INPUT_FILENAME, binary=False)
    return load_vec

# Create two sequences of 1,888 values each - annotator averages and cosine similarities - then compare
# them using Spearman's correlation. Note that since some words are in fact multiword phrases, which require
# a different kind of cosine similarity calculation than single words do, we can't use the Gensim function
# evaluate_word_pairs() out of them box ... but since that function simply creates the lists and then
# calls on stats.spearmanr, the following code is fully comparable.
def eval_vectors(ft_vectors, msl_dic):
    spear_list_ann_scores = []
    spear_list_cos_similarities = []
    curr_cos_similarity: float
    keys_exist: bool
    
    for key, value in msl_dic.items():
        keys_exist = True
        if not ((" " in key[0]) or (" " in key[1])):
            keys_exist = (ft_vectors.has_index_for(key[0]) and ft_vectors.has_index_for(key[1]))
            if keys_exist:
                curr_cos_similarity = ft_vectors.similarity(key[0], key[1])
        else:
            phrase1 = key[0].split()
            phrase2 = key[1].split()
            for w in phrase1:
                if not ft_vectors.has_index_for(w):
                    keys_exist = False
            for w in phrase2:
                if not ft_vectors.has_index_for(w):
                    keys_exist = False
            if keys_exist:
                curr_cos_similarity = ft_vectors.n_similarity(phrase1, phrase2)
        if keys_exist:
            spear_list_ann_scores.append(value)
            spear_list_cos_similarities.append(curr_cos_similarity)
    # stats.spearmanr() returns a tuple; the first value is the actual spearman's correlation
    spear = stats.spearmanr(spear_list_ann_scores, spear_list_cos_similarities)
    spear_number = spear[0]
    return spear_number


def mean_center_vectors(in_vectors):
    for vec_array in in_vectors.vectors:
        mean_point = vec_array.mean()
        vec_array -= mean_point
    return in_vectors


def all_but_the_top_vectors(in_vectors, dda):
    pca = PCA(n_components=dda)
    in_vectors.vectors = in_vectors.vectors.astype(np.single)
    mean = np.average(in_vectors.vectors, axis=0)
    temp = in_vectors.vectors - mean
    principal_components = pca.fit_transform(temp)
    principal_axes = pca.components_
    to_subtract = np.matmul(np.matmul(in_vectors.vectors, principal_axes.T), principal_axes)
    in_vectors.vectors = temp - to_subtract
    return in_vectors

def uncovec_vectors(in_vectors, alpha):
    in_vectors.vectors = in_vectors.vectors.astype(np.csingle)
    l, q = np.linalg.eigh(in_vectors.vectors.T.dot(in_vectors.vectors))
    l = l.astype(np.csingle)
    w = q * (l ** alpha)
    in_vectors.vectors = in_vectors.vectors @ w
    in_vectors.vectors = in_vectors.vectors.astype(np.single)
    return in_vectors


def train_vectors(msl_dict, mod_vectors):
    with open('hyper-out-glove.txt', "a", encoding="utf8") as h_out:

        startnow = datetime.now()
        h_out.write(str(startnow))
        h_out.write("\n")
        h_out.flush()
        os.fsync(h_out)

        li = [""] * 16
        li[CSV_VOC_MINCOUNT] = VOCAB_MIN_COUNT
        li[CSV_VECTOR_SIZE] = VECTOR_SIZE
        li[CSV_EPOCH] = MAX_ITER
        li[CSV_WIN_SIZE] = WINDOW_SIZE
        li[CSV_X_MAX] = X_MAX

        # (1)FT:INIT
        spear_similarity = eval_vectors(mod_vectors, msl_dict)
        li[CSV_MSL1] = str(spear_similarity)

        # (fBATS), run on clean vectors before postprocessing alterations
        li[CSV_DER] = str(evaluate_word_analogies_mod('analogy_derivational.txt', mod_vectors))
        li[CSV_INF] = str(evaluate_word_analogies_mod('analogy_inflectional.txt', mod_vectors))
        li[CSV_ENC] = str(evaluate_word_analogies_mod('analogy_encyclopedic.txt', mod_vectors))
        li[CSV_LEX] = str(evaluate_word_analogies_mod('analogy_lexicographic.txt', mod_vectors))
        # (2)FT:+MC
        mod_vectors = mean_center_vectors(mod_vectors)
        spear_sim_mc = eval_vectors(mod_vectors, msl_dict)
        li[CSV_MSL2] = str(spear_sim_mc)

        # (3)FT:+ABTT(-3)
        mod_vectors = all_but_the_top_vectors(mod_vectors, 3)
        spear_sim_top3 = eval_vectors(mod_vectors, msl_dict)
        li[CSV_MSL3] = str(spear_sim_top3)

        # (4)FT:+ABTT(-10)
        mod_vectors = load_vectors()
        mod_vectors = mean_center_vectors(mod_vectors)
        mod_vectors = all_but_the_top_vectors(mod_vectors, 10)
        spear_sim_top10 = eval_vectors(mod_vectors, msl_dict)
        li[CSV_MSL4] = str(spear_sim_top10)

        # (5)FT:+UNCOVEC
        mod_vectors = load_vectors()
        mod_vectors = mean_center_vectors(mod_vectors)
        mod_vectors = uncovec_vectors(mod_vectors, -0.3)
        spear_uncovec = eval_vectors(mod_vectors, msl_dict)
        li[CSV_MSL5] = str(spear_uncovec)

        # (1)+(2)+(5)+(3)
        mod_vectors = load_vectors()
        mod_vectors = mean_center_vectors(mod_vectors)
        mod_vectors = uncovec_vectors(mod_vectors, -0.3)
        mod_vectors = all_but_the_top_vectors(mod_vectors, 3)
        spear_sim_uncovec_top3 = eval_vectors(mod_vectors, msl_dict)
        li[CSV_MSL1253] = str(spear_sim_uncovec_top3)

        # (1)+(2)+(5)+(4)
        mod_vectors = load_vectors()
        mod_vectors = mean_center_vectors(mod_vectors)
        mod_vectors = uncovec_vectors(mod_vectors, -0.3)
        mod_vectors = all_but_the_top_vectors(mod_vectors, 10)
        spear_sim_uncovec_top10 = eval_vectors(mod_vectors, msl_dict)
        li[CSV_MSL1254] = str(spear_sim_uncovec_top10)

        '''
        str_result = "Spearman: Original = " + str(spear_similarity) + ", MC = " + str(spear_sim_mc) + "\n" \
                     + "ABTT(-3) = " + str(spear_sim_top3) + ", ABTT(-10) = " + str(spear_sim_top10) + ", UNCOVEC = " + str(spear_uncovec) + "\n" \
                     + "MC, UNCOVEC, ABTT(-3) = " + str(spear_sim_uncovec_top3) + ", MC, UNCOVEC, ABTT(-10) = " + str(spear_sim_uncovec_top10) + "\n"
        str_input_values = "VOCAB_MIN_COUNT = " + VOCAB_MIN_COUNT + ", VECTOR SIZE = " + VECTOR_SIZE + ", MAX_ITER = " \
                           + MAX_ITER + ", WINDOW_SIZE = " + WINDOW_SIZE + ", X_MAX = " + X_MAX + "\n"
        str_final = str_input_values + str_result
        h_out.write(str_final)

        h_out.write("End training: ")
        endnow = datetime.now()
        h_out.write(str(endnow))
        h_out.write("\n\n")
        h_out.flush()
        os.fsync(h_out)
        '''
        h_out.write(("\t".join(entry for entry in li)) + "\n\n")


### MAIN STARTS ###

# Parse command line arguments: minimum word frequency in vocabulary; size of embedding vector,
# size of context window; and the integer maximum number of co-occurrences to use in the weighting function.
#shell_array = str(sys.argv)
VOCAB_MIN_COUNT = str(sys.argv[1])
VECTOR_SIZE = str(sys.argv[2])
MAX_ITER = str(sys.argv[3])
WINDOW_SIZE = str(sys.argv[4])
X_MAX = str(sys.argv[5])

msl_dictionary = load_msl('msl.txt')
vectors = load_vectors()
train_vectors(msl_dictionary, vectors)
print("Program complete")
