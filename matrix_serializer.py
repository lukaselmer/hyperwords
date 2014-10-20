import numpy as np
from scipy.sparse import csr_matrix


def save_matrix(f, m):
    np.save(f + '_d', m.data)
    np.save(f + '_i', m.indices)
    np.save(f + '_p', m.indptr)


def load_matrix(f, la, lb):
    data = np.load(f + '_d.npy')
    indices = np.load(f + '_i.npy')
    indptr = np.load(f + '_p.npy')
    return csr_matrix((data, indices, indptr), shape=(la, lb))


def save_vocabulary(path, vocab):
    with open(path, 'w') as f:
        for w in vocab:
            print >>f, w


def load_vocabulary(path):
    with open(path) as f:
        vocab = [line.strip() for line in f if len(line) > 0]
    return dict([(a, i) for i, a in enumerate(vocab)]), vocab


def save_count_vocabulary(path, vocab):
    with open(path, 'w') as f:
        for w, c in vocab:
            print >>f, w, c


def load_count_vocabulary(path):
    with open(path) as f:
        # noinspection PyTypeChecker
        vocab = dict([line.strip().split() for line in f if len(line) > 0])
    return vocab
