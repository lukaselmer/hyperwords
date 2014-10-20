from sparsesvd import sparsesvd

from docopt import docopt
import numpy as np

from explicit import PositiveExplicit
from logger import initialize_logger, log_info
from matrix_serializer import save_vocabulary


def main():
    initialize_logger()
    
    args = docopt("""
    Usage:
        pmi2svd.py [options] <pmi_path> <output_path>
    
    Options:
        --dim NUM    Dimensionality of eigenvectors [default: 500]
        --neg NUM    Number of negative samples; subtracts its log from PMI [default: 1]
    """)
    
    pmi_path = args['<pmi_path>']
    output_path = args['<output_path>']
    dim = args['--dim']
    neg = args['--neg']
    
    explicit = PositiveExplicit(pmi_path, normalize=False, neg=neg)
    log_info('LOADED PPMI')
    
    ut, s, vt = sparsesvd(explicit.m.tocsc(), dim)
    log_info('DONE SVD')
    
    np.save(output_path + '.d' + str(dim) + '.n' + str(neg) + '.ut.npy', ut)
    np.save(output_path + '.d' + str(dim) + '.n' + str(neg) + '.s.npy', s)
    np.save(output_path + '.d' + str(dim) + '.n' + str(neg) + '.vt.npy', vt)
    save_vocabulary(output_path + '.d' + str(dim) + '.n' + str(neg) + '.words.vocab', explicit.iw)
    save_vocabulary(output_path + '.d' + str(dim) + '.n' + str(neg) + '.contexts.vocab', explicit.ic)
    log_info('SAVED MATRICES')


if __name__ == '__main__':
    main()
