from docopt import docopt

from embedding import EnsembleEmbedding, SVDEmbedding


def main():
    args = docopt("""
    Usage:
        svd2text.py [options] <svd_path> <output_path>
    
    Options:
        --w+c        Use ensemble of word and context vectors (not applicable to PPMI)
        --eig NUM    Weighted exponent of the eigenvalue matrix (only applicable to SVD) [default: 0.5]
    """)
    
    svd_path = args['<svd_path>']
    output_path = args['<output_path>']
    w_c = args['--w+c']
    eig = float(args['--eig'])
    
    if w_c:
        svd = EnsembleEmbedding(SVDEmbedding(svd_path, False, eig, False), SVDEmbedding(svd_path, False, eig, True), True)
    else:
        svd = SVDEmbedding(svd_path, True, eig)
    
    with open(output_path, 'w') as f:
        for i, w in enumerate(svd.iw):
            print >>f, w, ' '.join([str(x) for x in svd.m[i]])


if __name__ == '__main__':
    main()
