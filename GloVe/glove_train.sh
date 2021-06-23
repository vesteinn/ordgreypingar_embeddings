#!/bin/bash
set -e

# Makes programs, trains a GloVe model, then evaluates it.

make

CORPUS=../../all_sentences_lower_lemmatized_oneline.txt
#CORPUS=bylgjan_sentences_oneline.txt
VOCAB_FILE=vocab_rmh_glove.txt
#VOCAB_FILE=vocab_bylgjan.txt
COOCCURRENCE_FILE=cooccurrence.bin
COOCCURRENCE_SHUF_FILE=cooccurrence.shuf.bin
BUILDDIR=build
SAVE_FILE=vectors_rmh_glove
#SAVE_FILE=vectors_bylgjan
VERBOSE=2
MEMORY=4.0
VOCAB_MIN_COUNT=10
VECTOR_SIZE=300
MAX_ITER=10
WINDOW_SIZE=10
BINARY=2
NUM_THREADS=8
X_MAX=40
#if hash python 2>/dev/null; then
#    PYTHON=python
#else
#    PYTHON=python3
#fi
PYTHON=python3

echo
echo "$ $BUILDDIR/vocab_count -min-count $VOCAB_MIN_COUNT -verbose $VERBOSE < $CORPUS > $VOCAB_FILE"
$BUILDDIR/vocab_count -min-count $VOCAB_MIN_COUNT -verbose $VERBOSE < $CORPUS > $VOCAB_FILE
echo "$ $BUILDDIR/cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $CORPUS > $COOCCURRENCE_FILE"
$BUILDDIR/cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $CORPUS > $COOCCURRENCE_FILE
echo "$ $BUILDDIR/shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE"
$BUILDDIR/shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE
echo "$ $BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE"
$BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE
if [ "$CORPUS" = '../../all_sentences_lower_oneline.txt' ]; then
#if [ "$CORPUS" = 'bylgjan_sentences_oneline.txt' ]; then
   echo "$PYTHON -m gensim.scripts.glove2word2vec --input vectors_rmh_glove.txt --output vectors_rmh_glove_w2v.txt"
   $PYTHON -m gensim.scripts.glove2word2vec --input vectors_rmh_glove.txt --output vectors_rmh_glove_w2v.txt
   #echo "$PYTHON -m gensim.scripts.glove2word2vec --input vectors_rmh_glove.txt --output vectors_rmh_glove_w2v.txt"
   #$PYTHON -m gensim.scripts.glove2word2vec --input vectors_bylgjan.txt --output vectors_bylgjan_w2v.txt
   echo "$ $PYTHON glove_msl.py $VOCAB_MIN_COUNT $VECTOR_SIZE $MAX_ITER $WINDOW_SIZE $X_MAX"
   $PYTHON glove_msl.py $VOCAB_MIN_COUNT $VECTOR_SIZE $MAX_ITER $WINDOW_SIZE $X_MAX
   #$PYTHON -m gensim.scripts.glove2word2vec --input vectors_rmh_glove.txt --output vectors_rmh_glove_w2v.txt
   #HD: Keyra skipunina að ofan. Keyra svo eitthvað .py sem hleður inn skránni og vinnur úr henni, g.d. glove_msl.py
   #Fengið af https://stackoverflow.com/questions/27139908/load-precomputed-vectors-gensim
   #
   #Eða:: Í stað evaluate.py, keyra hérna gsft.py (eða equivalent) skrá sem umbreytir vigrunum í w2v format
   #(sjá https://stackoverflow.com/questions/27139908/load-precomputed-vectors-gensim þar sem stendur
   # python -m gensim.scripts.glove2word2vec --input  glove.840B.300d.txt --output glove.840B.300d.w2vformat.txt
   # (greinilega er notað gensim scripts sem heitir glove2word2vec))
   # og keyra svo bara minn eigin evaluation kóða á því
fi
