#!/bin/sh

# Download and install word2vecf
if [ ! -f word2vecf ]; then
    ./install_word2vecf.sh
fi


# Download corpus. We chose a small corpus for the example, and larger corpora will yield better results.
wget http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2010.en.shuffled.gz
gzip -d news.2010.en.shuffled.gz
CORPUS=news.2010.en.shuffled.gz

# Clean the corpus from non alpha-numeric symbols
./clean_corpus.sh $CORPUS > $CORPUS.clean


# Create two example collections of word-context pairs:

# A) Window size 2 with "clean" subsampling
mkdir w2.sub
python corpus2pairs.py --win 2 --sub 1e-5 ${CORPUS}.clean > w2.sub/pairs
./pairs2counts.sh w2.sub/pairs > w2.sub/counts
python counts2vocab.py w2.sub/counts

# B) Window size 5 with dynamic contexts and "dirty" subsampling
mkdir w5.dyn.sub.oov
python corpus2pairs.py --win 5 --dyn --sub 1e-5 --oov ${CORPUS}.clean > w5.dyn.sub.oov/pairs
./pairs2counts.sh w5.dyn.sub.oov/pairs w5.dyn.sub.oov/counts
python counts2vocab.py w5.dyn.sub.oov/counts

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


# Create embeddings with SGNS (A). Commands 2-7 are necessary for loading the vectors with embeddings.py
./word2vecf -train w2.sub/pairs -pow 0.75 -cvocab w2.sub/counts.contexts.vocab -wvocab w2.sub/counts.words.vocab -dumpcv w2.sub/sgns.d500.n5.contexts -output w2.sub/sgns.d500.n5.words -threads 10 -negative 5 -size 500;
python text2numpy.py w2.sub/sgns.d500.n5.words w2.sub/sgns.d500.n5.words
python text2numpy.py w2.sub/sgns.d500.n5.contexts w2.sub/sgns.d500.n5.contexts
cp w2.sub/pmi.d500.n5.words.vocab w2.sub/sgns.d500.n5.words.vocab
cp w2.sub/pmi.d500.n5.contexts.vocab w2.sub/sgns.d500.n5.contexts.vocab
rm w2.sub/sgns.d500.n5.words
rm w2.sub/sgns.d500.n5.contexts

# Create embeddings with SGNS (B). Commands 2-7 are necessary for loading the vectors with embeddings.py
./word2vecf -train w5.dyn.sub.oov/pairs -pow 0.75 -cvocab w5.dyn.sub.oov/counts.contexts.vocab -wvocab w5.dyn.sub.oov/counts.words.vocab -dumpcv w5.dyn.sub.oov/sgns.d500.n5.contexts -output w5.dyn.sub.oov/sgns.d500.n5.words -threads 10 -negative 5 -size 500;
python text2numpy.py w5.dyn.sub.oov/sgns.d500.n5.words w5.dyn.sub.oov/sgns.d500.n5.words
python text2numpy.py w5.dyn.sub.oov/sgns.d500.n5.contexts w5.dyn.sub.oov/sgns.d500.n5.contexts
cp w5.dyn.sub.oov/pmi.d500.n5.words.vocab w5.dyn.sub.oov/sgns.d500.n5.words.vocab
cp w5.dyn.sub.oov/pmi.d500.n5.contexts.vocab w5.dyn.sub.oov/sgns.d500.n5.contexts.vocab
rm w5.dyn.sub.oov/sgns.d500.n5.words
rm w5.dyn.sub.oov/sgns.d500.n5.contexts


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
