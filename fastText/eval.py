from gsft import *
from test_analogies import evaluate_word_analogies_mod
import argparse
from gensim.models.fasttext import load_facebook_model
msl_dictionary = load_msl('../MSL/msl.txt')


def evaluate_fasttext_model(file_name):
    mod_vectors = load_facebook_model(file_name).wv

    # (1)FT:INIT
    spear_sim = eval_vectors(mod_vectors, msl_dictionary)
    print(f"Spear sim: {spear_sim}")

    # (fBATS), run on clean vectors before postprocessing alterations
    print('Derivational analogy:')
    deriv_score = evaluate_word_analogies_mod('../IceBATS/analogy_derivational.txt', model=mod_vectors)
    print('Inflectional analogy:')
    infl_score = evaluate_word_analogies_mod('../IceBATS/analogy_inflectional.txt', model=mod_vectors)
    print('Encyclopedic analogy:')
    enc_score = evaluate_word_analogies_mod('../IceBATS/analogy_encyclopedic.txt', model=mod_vectors)
    print('Lexicographic analogy:')
    lex_score = evaluate_word_analogies_mod('../IceBATS/analogy_lexicographic.txt', model=mod_vectors)                            

    #(2)FT:+MC
    spear_sim_mc = eval_vectors(
        mean_center_vectors(mod_vectors),
        msl_dictionary
    )
    
    #(3)FT:+ABTT(-3)
    spear_sim_top3 = eval_vectors(all_but_the_top_vectors(mod_vectors, 3), msl_dictionary)
    print(f"Spear sim top3: {spear_sim_top3}")

    #(4)FT:+ABTT(-10)
    spear_sim_top10 = eval_vectors(
        all_but_the_top_vectors(mean_center_vectors(mod_vectors), 10),
        msl_dictionary
    )
    print(f"Spear sim top10 {spear_sim_top10}")

    #(5)FT:+UNCOVEC
    spear_uncovec = eval_vectors(
        uncovec_vectors(mean_center_vectors(mod_vectors), -0.3),
        msl_dictionary
    )
    print(f"Spear uncovec: {spear_uncovec}")

    #(1)+(2)+(5)+(3)
    spear_sim_uncovec_top3 = eval_vectors(
        all_but_the_top_vectors(
            uncovec_vectors(mean_center_vectors(mod_vectors), -0.3), 3),
        msl_dictionary)
    print(f"Spearh sim uncovec top3: {spear_sim_uncovec_top3}")

    #(1)+(2)+(5)+(10)
    spear_sim_uncovec_top10 = eval_vectors(
        all_but_the_top_vectors(
            uncovec_vectors(mean_center_vectors(mod_vectors), -0.3), 10),
        msl_dictionary)
    print(f"Spearh sim uncovec top10: {spear_sim_uncovec_top10}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model")
    args = parser.parse_args()
    evaluate_fasttext_model(args.model)