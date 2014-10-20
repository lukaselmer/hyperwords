#!/bin/sh

???? Download the latest wikipedia corpus.

???? Download and MAKE word2vecf

# Clean the corpus from non alpha-numeric symbols
./clean_corpus.sh $CORPUS > $CORPUS.clean

# Create two example collections of word-context pairs:

# A) Window size 2 with "clean" subsampling
mkdir w2.sub
python corpus2pairs.py --win 2 --sub 1e-5 ${CORPUS}.clean > w2.sub/pairs
./pairs2counts.sh w2.sub/pairs > w2.sub/counts

# B) Window size 5 with dynamic contexts and "dirty" subsampling
mkdir w5.dyn.sub.oov
python corpus2pairs.py --win 5 --dyn --sub 1e-5 --oov ${CORPUS}.clean > w5.dyn.sub.oov/pairs
./pairs2counts.sh w5.dyn.sub.oov/pairs w5.dyn.sub.oov/counts

# Calculate PMI matrices for each collection of pairs
python counts2pmi.py --cds 0.75 w2.sub/counts w2.sub/pmi
python counts2pmi.py --cds 0.75 w5.dyn.sub.oov/counts w5.dyn.sub.oov/pmi

# Create embeddings with SVD
python pmi2svd.py --dim 500 --neg 5 w2.sub/pmi w2.sub/svd
cp w2.sub/pmi.words.vocab w2.sub/svd.words.vocab
cp w2.sub/pmi.contexts.vocab w2.sub/svd.contexts.vocab
python pmi2svd.py --dim 500 --neg 5 w5.dyn.sub.oov/pmi w5.dyn.sub.oov/svd
cp w5.dyn.sub.oov/pmi.words.vocab w5.dyn.sub.oov/svd.words.vocab
cp w5.dyn.sub.oov/pmi.contexts.vocab w5.dyn.sub.oov/svd.contexts.vocab

????run word2vecf
??? create word and context vocabs from PMI
??? maybe have pairs2pmi.py also deposit vocabs with counts? 
./word2vecf -train tacl/${corpus}_4w2v -pow 0.75 -cvocab tacl/${corpus}.contexts.vocab -wvocab tacl/${corpus}.words.vocab -iters 1 -dumpcv tacl/sgns/${corpus}.075.d${dims}.n${k}.contexts -output tacl/sgns/${corpus}.075.d${dims}.n${k}.words -threads 21 -negative ${k} -size ${dims};
python text2numpy.py tacl/sgns/${corpus}.075.d${dims}.n${k}.words tacl/sgns/${corpus}.075.d${dims}.n${k}.words;
python text2numpy.py tacl/sgns/${corpus}.075.d${dims}.n${k}.contexts tacl/sgns/${corpus}.075.d${dims}.n${k}.contexts;
cp vocab tacl/sgns/${corpus}.075.d${dims}.n${k}.words.vocab;
cp vocab tacl/sgns/${corpus}.075.d${dims}.n${k}.contexts.vocab;
rm tacl/sgns/${corpus}.075.d${dims}.n${k}.words;
rm tacl/sgns/${corpus}.075.d${dims}.n${k}.contexts;
*********************************************************
python text2numpy.py text_path** output_path**

?????do the same with GloVe?

# Evaluate on Word Similarity
echo "WS353 Results"

python ws_test.py --neg 5 PPMI w2.sub/pmi ws/ws353.txt
python ws_test.py --eig 0.5 SVD w2.sub/svd ws/ws353.txt
python ws_test.py --w+c SGNS w2.sub/sgns ws/ws353.txt

python ws_test.py --neg 5 PPMI w5.dyn.sub.oov/pmi ws/ws353.txt
python ws_test.py --eig 0.5 SVD w5.dyn.sub.oov/svd ws/ws353.txt
python ws_test.py --w+c SGNS w5.dyn.sub.oov/sgns ws/ws353.txt

# Evaluate on Analogies
echo "Google Analogy Results"

python analogy_test.py PPMI w2.sub/pmi analogy/google.txt
python analogy_test.py --eig 0 SVD w2.sub/svd analogy/google.txt
python analogy_test.py SGNS w2.sub/sgns analogy/google.txt

python analogy_test.py PPMI w5.dyn.sub.oov/pmi analogy/google.txt
python analogy_test.py --eig 0 SVD w5.dyn.sub.oov/svd analogy/google.txt
python analogy_test.py SGNS w5.dyn.sub.oov/sgns analogy/google.txt
