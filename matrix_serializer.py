import numpy as np
from scipy.sparse import csr_matrix


def saveMatrix(f, m):
    np.save(f + '_d', m.data)
    np.save(f + '_i', m.indices)
    np.save(f + '_p', m.indptr)

def loadMatrix(f, la, lb):
    data = np.load(f + '_d.npy')
    indices = np.load(f + '_i.npy')
    indptr = np.load(f + '_p.npy')
    return csr_matrix((data, indices, indptr), shape=(la, lb))

def saveVocabulary(path, vocab):
    with open(path, 'w') as f:
        for w in vocab:
            print >>f, w

def loadVocabulary(path):
    with open(path) as f:
        vocab = [line.strip() for line in f if len(line) > 0]
    return dict([(a, i) for i, a in enumerate(vocab)]), vocab
