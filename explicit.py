import heapq

from scipy.sparse import dok_matrix, csr_matrix

from matrix_serializer import loadVocabulary, loadMatrix
import numpy as np


class Explicit:
    '''
    Base class for explicit representations. Assumes that the serialized input is e^PMI.
    '''
    
    def __init__(self, path, normalize=True):
        self.wi, self.iw = loadVocabulary(path + '.words.vocab')
        self.ci, self.ic = loadVocabulary(path + '.contexts.vocab')
        self.m = loadMatrix(path, len(self.iw), len(self.ic))
        self.m.data = np.log(self.m.data)
        self.normal = normalize
        if normalize:
            self.m = self.normalize(self.m)
    
    def normalize(self, m):
        m2 = m.copy()
        m2.data = m2.data**2
        norm = np.reciprocal(np.sqrt(np.array(m2.sum(axis=1))[:, 0]))
        normalizer = dok_matrix((len(norm), len(norm)))
        normalizer.setdiag(norm)
        return normalizer.tocsr().dot(m)
    
    def represent(self, w):
        if w in self.wi:
            return self.m[self.wi[w], :]
        else:
            return csr_matrix((1, len(self.ic)))
    
    def similarityFirstOrder(self, w, c):
        return self.m[self.wi[w], self.ci[c]]
    
    def similarity(self, w1, w2):
        ''' Assumes the vectors have been normalized. '''
        return self.represent(w1).dot(self.represent(w2))[0, 0]
    
    def closestContexts(self, w, n=10):
        '''Assumes the vectors have been normalized.'''
        scores = self.represent(w)
        return heapq.nlargest(n, zip(scores, self.ic))
    
    def closest(self, w, n=10):
        '''Assumes the vectors have been normalized.'''
        scores = self.m.dot(self.represent(w))
        return heapq.nlargest(n, zip(scores, self.iw))


class PositiveExplicit(Explicit):
    '''
    Positive PMI (PPMI) with negative sampling (neg).
    Negative samples shift the PMI matrix before truncation. 
    '''
    
    def __init__(self, path, normalize=True, neg=1):
        Explicit.__init__(self, path, False)
        self.m.data -= np.log(neg)
        self.m.data[self.m.data < 0] = 0
        self.m.eliminate_zeros()
        if normalize:
            self.m = self.normalize(self.m)
