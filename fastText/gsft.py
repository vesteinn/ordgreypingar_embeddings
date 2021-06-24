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

L_MIN_COUNT = [5]
L_WINDOW = [2]
L_SG = [0]
L_VECTOR_SIZE = [200]
L_MIN_N = [1]
L_MAX_N = [2]
L_EPOCHS = [13]
L_ALPHA = [0.01]
L_HSOFT_NEGSAMP = [0]
L_SAMPLE = [1.00E-05]
L_NEGATIVE = [5]
L_NEGEXP = [0.5]

INPUT_FILENAME = '../all_sentences_lower.txt'
#INPUT_FILENAME = '../all_sentences_lower_lemmatized.txt'



FILE_OUT_STRINGLIST = []
CSV_HEADER = "DERIVATIONAL\tINFLECTIONAL\tENCYCLOPEDIC\tMSL-1\tMSL-2\tMSL-3\tMSL-4\tMSL-5\tMSL-1.2.5.3\tMSL-1.2.5.4\t" \
             + "MÓDEL\tSG/CB\tLEMMMAÐ\tSIZE\tWINDOW\tALPHA\tEPOCH\tNEGATIVE\tSAMPLE\tH-SOFTMAX\tNEG EXP\t" + \
             "HASHFXN\tTRIM_RULE\tMIN_N\tMAX_N\tWORD_NGR\tBUCKET\n"
CSV_DER = 0
CSV_INF = 1
CSV_ENC = 2
CSV_LEX = 3
CSV_MSL1 = 4
CSV_MSL2 =  5
CSV_MSL3 = 6
CSV_MSL4 = 7
CSV_MSL5 = 8
CSV_MSL1253 =9
CSV_MSL1254 = 10
CSV_MODEL = 11
CSV_SGCB = 12
CSV_LEMMAD = 13
CSV_SIZE = 14
CSV_WINDOW =15
CSV_ALPHA =16
CSV_EPOCH =17
CSV_NEG =18
CSV_SAMPLE = 19
CSV_HSOFTMAX = 20
CSV_NEGEXP = 21
CSV_HASH = 22
CSV_TRIM = 23
CSV_MINN = 24
CSV_MAXN = 25
CSV_WORDNGR = 26
CSV_BUCKET = 27
CSV_MINCOUNT = 28


def train_ft(input_file, output_file, min_count_var, window_var, sg_cbow_var, size_var, min_n_var, max_n_var, iter_var, alpha_var, hsoft_negsamp_var, sample_var, negative_var, negexp_var):
    logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)
    sentences = gensim.models.word2vec.LineSentence(input_file)
    ft_model = gensim.models.fasttext.FastText(sentences,
                                               min_count=min_count_var,
                                               window=window_var,
                                               sg=sg_cbow_var,
                                               vector_size=size_var,
                                               workers=8,
                                               min_n=min_n_var,
                                               max_n=max_n_var,
                                               epochs=iter_var,
                                               alpha=alpha_var,
                                               hs=hsoft_negsamp_var,
                                               sample=sample_var,
                                               negative=negative_var,
                                               ns_exponent=negexp_var,
                                               max_vocab_size=1000000000)
    ft_model.save(output_file)
    return ft_model


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


# Create two sequences of 1,888 values each - annotator averages and cosine similarities - then compare
# them using Spearman's correlation. Note that since some words are in fact multiword phrases, which require
# a different kind of cosine similarity calculation than single words do, we can't use the Gensim function
# evaluate_word_pairs() out of them box ... but since that function simply creates the lists and then
# calls on stats.spearmanr, the following code is fully comparable.
def eval_model(ft_model, msl_dic):
    spear_list_ann_scores = []
    spear_list_cos_similarities = []
    curr_cos_similarity: float
    for key, value in msl_dic.items():
        spear_list_ann_scores.append(value)
        if not ((" " in key[0]) or (" " in key[1])):
            curr_cos_similarity = ft_model.wv.similarity(key[0], key[1])
        else:
            phrase1 = key[0].split()
            phrase2 = key[1].split()
            curr_cos_similarity = ft_model.wv.n_similarity(phrase1, phrase2)
        spear_list_cos_similarities.append(curr_cos_similarity)
    # stats.spearmanr() returns a tuple; the first value is the actual spearman's correlation
    spear = stats.spearmanr(spear_list_ann_scores, spear_list_cos_similarities)
    spear_number = spear[0]
    return spear_number


# Create two sequences of 1,888 values each - annotator averages and cosine similarities - then compare
# them using Spearman's correlation. Note that since some words are in fact multiword phrases, which require
# a different kind of cosine similarity calculation than single words do, we can't use the Gensim function
# evaluate_word_pairs() out of them box ... but since that function simply creates the lists and then
# calls on stats.spearmanr, the following code is fully comparable.
def eval_vectors(ft_vectors, msl_dic):
    spear_list_ann_scores = []
    spear_list_cos_similarities = []
    curr_cos_similarity: float
    for key, value in msl_dic.items():
        spear_list_ann_scores.append(value)
        if not ((" " in key[0]) or (" " in key[1])):
            curr_cos_similarity = ft_vectors.similarity(key[0], key[1])
        else:
            phrase1 = key[0].split()
            phrase2 = key[1].split()
            curr_cos_similarity = ft_vectors.n_similarity(phrase1, phrase2)
        spear_list_cos_similarities.append(curr_cos_similarity)
    # stats.spearmanr() returns a tuple; the first value is the actual spearman's correlation
    spear = stats.spearmanr(spear_list_ann_scores, spear_list_cos_similarities)
    spear_number = spear[0]
    return spear_number


def train_model(msl_dict):
    with open('hyper-out.txt', "a", encoding="utf8") as h_out:
        str_mod = INPUT_FILENAME

        list_min_count = L_MIN_COUNT
        list_window = L_WINDOW
        list_sg = L_SG
        list_size = L_VECTOR_SIZE
        list_min_n = L_MIN_N
        list_max_n = L_MAX_N
        list_iter_epoch = L_EPOCHS
        list_alpha = L_ALPHA
        list_hsoft_negsamp = L_HSOFT_NEGSAMP
        list_sample = L_SAMPLE
        list_negative = L_NEGATIVE
        list_negexp = L_NEGEXP

        for m_c in list_min_count:
            for l_w in list_window:
                for sg in list_sg:
                    for si in list_size:
                        for min_n in list_min_n:
                            for max_n in list_max_n:
                                for i in list_iter_epoch:
                                    for a in list_alpha:
                                        for hs in list_hsoft_negsamp:
                                            for sa in list_sample:
                                                for neg in list_negative:
                                                    for nexp in list_negexp:

                                                        # Populate our output list with known values
                                                        li = [""] * 29
                                                        li[CSV_MODEL] = "ft"
                                                        if sg == 1:
                                                            li[CSV_SGCB] = "SG"
                                                        else:
                                                            li[CSV_SGCB] = "CB"
                                                        li[CSV_LEMMAD] = "NEI"
                                                        li[CSV_SIZE] = str(si)
                                                        li[CSV_WINDOW] = str(l_w)
                                                        li[CSV_ALPHA] = str(a)
                                                        li[CSV_EPOCH] = str(i)
                                                        li[CSV_NEG] = str(neg)
                                                        li[CSV_SAMPLE] = str(sa)
                                                        li[CSV_HSOFTMAX] = str(hs)
                                                        li[CSV_NEGEXP] = str(nexp)
                                                        li[CSV_HASH] = ""
                                                        li[CSV_TRIM] = ""
                                                        li[CSV_MINN] = str(min_n)
                                                        li[CSV_MAXN] = str(max_n)
                                                        li[CSV_WORDNGR] = ""
                                                        li[CSV_BUCKET] = ""
                                                        li[CSV_MINCOUNT] = str(m_c)


                                                        # To train a full-size model and save its vectors
                                                        full_model = train_ft(str_mod, 'rmh_ft.bin', m_c, l_w, sg, si, min_n, max_n, i, a, hs, sa, neg, nexp)
                                                        mod_vectors = full_model.wv
                                                        mod_vectors.save('rmh_ft_vectors.kv')
                                                        
                                                        # To load pre-trained model
                                                        # loaded_model = load_model()

                                                        # To load pre-trained vectors
                                                        mod_vectors = KeyedVectors.load('rmh_ft_vectors.kv')

                                                        # (1)FT:INIT
                                                        spear_similarity = eval_vectors(mod_vectors, msl_dict)
                                                        li[CSV_MSL1] = str(spear_similarity)

                                                        # (fBATS), run on clean vectors before postprocessing alterations
                                                        print('Derivational analogy:')
                                                        li[CSV_DER] = str(evaluate_word_analogies_mod('analogy_derivational.txt', 'rmh_ft_vectors.kv'))
                                                        print('Inflectional analogy:')
                                                        li[CSV_INF] = str(evaluate_word_analogies_mod('analogy_inflectional.txt', 'rmh_ft_vectors.kv'))
                                                        print('Encyclopedic analogy:')
                                                        li[CSV_ENC] = str(evaluate_word_analogies_mod('analogy_encyclopedic.txt', 'rmh_ft_vectors.kv'))
                                                        print('Lexicographic analogy:')
                                                        li[CSV_LEX] = str(evaluate_word_analogies_mod('analogy_lexicographic.txt', 'rmh_ft_vectors.kv'))                                 

                                                        #(2)FT:+MC
                                                        mod_vectors = mean_center_vectors(mod_vectors)
                                                        spear_sim_mc = eval_vectors(mod_vectors, msl_dict)
                                                        li[CSV_MSL2] = str(spear_sim_mc)

                                                        #(3)FT:+ABTT(-3)
                                                        mod_vectors = all_but_the_top_vectors(mod_vectors, 3)
                                                        spear_sim_top3 = eval_vectors(mod_vectors, msl_dict)
                                                        li[CSV_MSL3] = str(spear_sim_top3)

                                                        #(4)FT:+ABTT(-10)
                                                        mod_vectors = KeyedVectors.load('rmh_ft_vectors.kv')
                                                        mod_vectors = mean_center_vectors(mod_vectors)
                                                        mod_vectors = all_but_the_top_vectors(mod_vectors, 10)
                                                        spear_sim_top10 = eval_vectors(mod_vectors, msl_dict)
                                                        li[CSV_MSL4] = str(spear_sim_top10)

                                                        #(5)FT:+UNCOVEC
                                                        mod_vectors = KeyedVectors.load('rmh_ft_vectors.kv')
                                                        mod_vectors = mean_center_vectors(mod_vectors)
                                                        mod_vectors = uncovec_vectors(mod_vectors, -0.3)
                                                        spear_uncovec = eval_vectors(mod_vectors, msl_dict)
                                                        li[CSV_MSL5] = str(spear_uncovec)

                                                        #(1)+(2)+(5)+(3)
                                                        mod_vectors = KeyedVectors.load('rmh_ft_vectors.kv')
                                                        mod_vectors = mean_center_vectors(mod_vectors)
                                                        mod_vectors = uncovec_vectors(mod_vectors, -0.3)
                                                        mod_vectors = all_but_the_top_vectors(mod_vectors, 3)
                                                        spear_sim_uncovec_top3 = eval_vectors(mod_vectors, msl_dict)
                                                        li[CSV_MSL1253] = str(spear_sim_uncovec_top3)

                                                        #(1)+(2)+(5)+(4)
                                                        mod_vectors = KeyedVectors.load('rmh_ft_vectors.kv')
                                                        mod_vectors = mean_center_vectors(mod_vectors)
                                                        mod_vectors = uncovec_vectors(mod_vectors, -0.3)
                                                        mod_vectors = all_but_the_top_vectors(mod_vectors, 10)
                                                        spear_sim_uncovec_top10 = eval_vectors(mod_vectors, msl_dict)
                                                        li[CSV_MSL1254] = str(spear_sim_uncovec_top10)

                                                        h_out.write(("\t".join(entry for entry in li)) + "\n\n")

def load_model():
    load_m = gensim.models.fasttext.FastText.load('rmh_ft.bin')
    return load_m


def mean_center_model(in_model):
    for vec_array in in_model.wv.vectors:
        mean_point = vec_array.mean()
        vec_array -= mean_point
    return in_model


def mean_center_vectors(in_vectors):
    for vec_array in in_vectors.vectors:
        mean_point = vec_array.mean()
        vec_array -= mean_point
    return in_vectors


def all_but_the_top(in_model, dda):
    pca = PCA(n_components=dda)
    embedding_matrix = in_model.wv.vectors
    embedding_matrix = embedding_matrix.astype(np.single)
    mean = np.average(embedding_matrix, axis=0)
    temp = embedding_matrix - mean
    principal_components = pca.fit_transform(temp)
    principal_axes = pca.components_
    to_subtract = np.matmul(np.matmul(embedding_matrix, principal_axes.T), principal_axes)
    in_model.wv.vectors = temp - to_subtract
    return in_model


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


def uncovec(in_model, alpha):
    embedding_matrix = in_model.wv.vectors
    embedding_matrix = embedding_matrix.astype(np.csingle)
    l, q = np.linalg.eigh(embedding_matrix.T.dot(embedding_matrix))
    l = l.astype(np.csingle)
    w = q * (l**alpha)
    in_model.wv.vectors = in_model.wv.vectors @ w
    in_model.wv.vectors = in_model.wv.vectors.astype(np.csingle)
    return in_model


def uncovec_vectors(in_vectors, alpha):
    in_vectors.vectors = in_vectors.vectors.astype(np.csingle)
    l, q = np.linalg.eigh(in_vectors.vectors.T.dot(in_vectors.vectors))
    l = l.astype(np.csingle)
    w = q * (l ** alpha)
    in_vectors.vectors = in_vectors.vectors @ w
    in_vectors.vectors = in_vectors.vectors.astype(np.single)
    return in_vectors


### MAIN STARTS ###
msl_dictionary = load_msl('msl.txt')
train_model(msl_dictionary)