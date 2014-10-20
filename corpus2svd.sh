#!/bin/sh

# Parse input params
??????????????????????????????????

# Clean the corpus from non alpha-numeric symbols
./clean_corpus.sh $CORPUS > $CORPUS.filtered

# Make a temporary directory
mkdir $OUTPUT_DIR

# Create collection of word-context pairs
python corpus2pairs.py $OPTS ${CORPUS}.clean > $OUTPUT_DIR/pairs
sort -T $OUTPUT_DIR $OUTPUT_DIR/pairs | uniq -c > $OUTPUT_DIR/pair_counts

# Calculate PMI matrices for each collection of pairs
python pairs2pmi.py $OPTS $OUTPUT_DIR/pair_counts $OUTPUT_DIR/pmi

# Create embeddings with SVD
python pmi2svd.py $OPTS $OUTPUT_DIR/pmi $OUTPUT_DIR/svd
cp $OUTPUT_DIR/pmi.words.vocab $OUTPUT_DIR/svd.words.vocab
cp $OUTPUT_DIR/pmi.contexts.vocab $OUTPUT_DIR/svd.contexts.vocab

# Save the embeddings in the textual format 
python svd2text.py $OPTS $OUTPUT_DIR/svd $OUTPUT_DIR/vectors.txt

# Remove temporary files
rm $CORPUS.clean
rm $OUTPUT_DIR/pair*
rm $OUTPUT_DIR/pmi*
rm $OUTPUT_DIR/svd*
