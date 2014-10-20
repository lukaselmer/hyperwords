from docopt import docopt
from scipy.sparse import dok_matrix, csr_matrix

from logger import logInfo, initializeLogger
from matrix_serializer import saveMatrix, saveVocabulary
import numpy as np


def main():
    initializeLogger()
    
    args = docopt("""
    Usage:
        pairs2pmi.py [options] <pair_counts> <output_path>
    
    Options:
        --cds NUM    Context distribution smoothing [default: 1.0 (no smoothing)]
    """)
    
    counts_path = args['<pair_counts>']
    vectors_path = args['<output_path>']
    words_vocab_path = vectors_path+'.words.vocab'
    contexts_vocab_path = vectors_path+'.contexts.vocab'
    
    cds = float(args['--cds'])
    
    counts, iw, ic = readCountsMatrix(counts_path)
    logInfo('LOADED COUNTS')
    
    pmi = calcPMI(counts, cds)
    logInfo('CALCULATED PMI')
    
    saveMatrix(vectors_path, pmi)
    saveVocabulary(words_vocab_path, iw)
    saveVocabulary(contexts_vocab_path, ic)
    logInfo('SAVED EVERYTHING')

def readCountsMatrix(counts_path):
    '''
    Reads the counts into a sparse matrix (CSR) from the count-word-context textual format. 
    '''
    words = set()
    contexts = set()
    with open(counts_path) as f:
        for line in f:
            count, word, context = line.strip().split()
            count = int(count)
            words.add(word)
            contexts.add(context)
    
    words = list(words)
    contexts = list(contexts)
    iw = sorted(words)
    ic = sorted(contexts)
    wi = dict([(w, i) for i, w in enumerate(iw)])
    ci = dict([(c, i) for i, c in enumerate(ic)])
    logInfo('LOADED VOCABS')
    
    counts = csr_matrix((len(wi), len(ci)), dtype=np.float32)
    tmp_counts = dok_matrix((len(wi), len(ci)), dtype=np.float32)
    update_threshold = 100000
    i = 0
    with open(counts_path) as f:
        for line in f:
            count, word, context = line.strip().split()
            if word in wi and context in ci:
                tmp_counts[wi[word], ci[context]] = int(count)
            i += 1
            if i == update_threshold:
                counts = counts + tmp_counts.tocsr()
                tmp_counts = dok_matrix((len(wi), len(ci)), dtype=np.float32)
                i = 0
    
    return counts, iw, ic

def calcPMI(counts, cds):
    '''
    Calculates e^PMI; PMI without the log().
    '''
    sum_w = np.array(counts.sum(axis=1))[:, 0]
    sum_c = np.array(counts.sum(axis=0))[0, :]
    if cds != 1:
        sum_c = sum_c**cds
    sum_total = sum_c.sum()
    sum_w = np.reciprocal(sum_w)
    sum_c = np.reciprocal(sum_c)
    
    pmi = csr_matrix(counts)
    pmi = multiplyByRows(pmi, sum_w)
    pmi = multiplyByColumns(pmi, sum_c)
    pmi = pmi * sum_total
    return pmi

def multiplyByRows(matrix, row_coefs):
    normalizer = dok_matrix((len(row_coefs), len(row_coefs)))
    normalizer.setdiag(row_coefs)
    return normalizer.tocsr().dot(matrix)

def multiplyByColumns(matrix, col_coefs):
    normalizer = dok_matrix((len(col_coefs), len(col_coefs)))
    normalizer.setdiag(col_coefs)
    return matrix.dot(normalizer.tocsr())


if __name__ == '__main__':
    main()
