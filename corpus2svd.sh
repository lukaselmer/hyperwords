# Parse input params
??????????????????????????????????

# Clean the corpus from non alpha-numeric symbols
iconv -c -f utf-8 -t ascii < $CORPUS | tr '[A-Z]' '[a-z]' | sed "s/[^a-z0-9]*[ \t\n\r][^a-z0-9]*/ /g" | sed "s/[^a-z0-9]*$/ /g" | sed "s/  */ /g" > $CORPUS.filtered

# Make a temporary directory
mkdir $OUTPUT_DIR

# Create collection of word-context pairs
python extract_pairs.py $OPTS ${CORPUS}.filtered > $OUTPUT_DIR/pairs
sort -T $OUTPUT_DIR $OUTPUT_DIR/pairs | uniq -c > $OUTPUT_DIR/pair_counts

# Calculate PMI matrices for each collection of pairs
python pairs2pmi.py $OPTS $OUTPUT_DIR/pair_counts $OUTPUT_DIR/pmi

# Create embeddings with SVD
python svd.py $OPTS $OUTPUT_DIR/pmi $OUTPUT_DIR/svd
cp $OUTPUT_DIR/pmi.words.vocab $OUTPUT_DIR/svd.words.vocab
cp $OUTPUT_DIR/pmi.contexts.vocab $OUTPUT_DIR/svd.contexts.vocab

# Save the embeddings in the textual format 
python svd2text.py $OPTS $OUTPUT_DIR/svd $OUTPUT_DIR/vectors.txt

# Remove temporary files
rm $CORPUS.filtered
rm $OUTPUT_DIR/pair*
rm $OUTPUT_DIR/pmi*
rm $OUTPUT_DIR/svd*
