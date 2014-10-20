from docopt import docopt
from sparsesvd import sparsesvd

from explicit import PositiveExplicit
from logger import initializeLogger, logInfo
from matrix_serializer import saveVocabulary
import numpy as np


def main():
    initializeLogger()
    
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
    logInfo('LOADED PPMI')
    
    ut, s, vt = sparsesvd(explicit.m.tocsc(), dim)
    logInfo('DONE SVD')
    
    np.save(output_path+'.d'+str(dim)+'.n'+str(neg)+'.ut.npy', ut)
    np.save(output_path+'.d'+str(dim)+'.n'+str(neg)+'.s.npy', s)
    np.save(output_path+'.d'+str(dim)+'.n'+str(neg)+'.vt.npy', vt)
    saveVocabulary(output_path+'.d'+str(dim)+'.n'+str(neg)+'.words.vocab', explicit.iw)
    saveVocabulary(output_path+'.d'+str(dim)+'.n'+str(neg)+'.contexts.vocab', explicit.ic)
    logInfo('SAVED MATRICES')


if __name__ == '__main__':
    main()
