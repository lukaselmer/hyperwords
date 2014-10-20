from docopt import docopt
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np

from logger import log_info, initialize_logger
from matrix_serializer import save_matrix, save_vocabulary


def main():
    initialize_logger()
    
    args = docopt("""
    Usage:
        counts2pmi.py [options] <pair_counts> <output_path>
    
    Options:
        --cds NUM    Context distribution smoothing [default: 1.0 (no smoothing)]
    """)
    
    counts_path = args['<pair_counts>']
    vectors_path = args['<output_path>']
    words_vocab_path = vectors_path + '.words.vocab'
    contexts_vocab_path = vectors_path + '.contexts.vocab'
    
    cds = float(args['--cds'])
    
    counts, iw, ic = read_counts_matrix(counts_path)
    log_info('LOADED COUNTS')
    
    pmi = calc_pmi(counts, cds)
    log_info('CALCULATED PMI')
    
    save_matrix(vectors_path, pmi)
    save_vocabulary(words_vocab_path, iw)
    save_vocabulary(contexts_vocab_path, ic)
    log_info('SAVED EVERYTHING')


def read_counts_matrix(counts_path):
    """
    Reads the counts into a sparse matrix (CSR) from the count-word-context textual format.
    """
    words = set()
    contexts = set()
    with open(counts_path) as f:
        for line in f:
            count, word, context = line.strip().split()
            words.add(word)
            contexts.add(context)
    
    words = list(words)
    contexts = list(contexts)
    iw = sorted(words)
    ic = sorted(contexts)
    wi = dict([(w, i) for i, w in enumerate(iw)])
    ci = dict([(c, i) for i, c in enumerate(ic)])
    log_info('LOADED VOCABS')
    
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


def calc_pmi(counts, cds):
    """
    Calculates e^PMI; PMI without the log().
    """
    sum_w = np.array(counts.sum(axis=1))[:, 0]
    sum_c = np.array(counts.sum(axis=0))[0, :]
    if cds != 1:
        sum_c = sum_c ** cds
    sum_total = sum_c.sum()
    sum_w = np.reciprocal(sum_w)
    sum_c = np.reciprocal(sum_c)
    
    pmi = csr_matrix(counts)
    pmi = multiply_by_rows(pmi, sum_w)
    pmi = multiply_by_columns(pmi, sum_c)
    pmi = pmi * sum_total
    return pmi


def multiply_by_rows(matrix, row_coefs):
    normalizer = dok_matrix((len(row_coefs), len(row_coefs)))
    normalizer.setdiag(row_coefs)
    return normalizer.tocsr().dot(matrix)


def multiply_by_columns(matrix, col_coefs):
    normalizer = dok_matrix((len(col_coefs), len(col_coefs)))
    normalizer.setdiag(col_coefs)
    return matrix.dot(normalizer.tocsr())


if __name__ == '__main__':
    main()
