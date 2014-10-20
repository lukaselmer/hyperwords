from docopt import docopt

import numpy as np


def main():
    args = docopt("""
    Usage:
        text2numpy.py <text_path> <output_path>
    """)
    
    text_path = args['<text_vectors>']
    output_path = args['<output_path>']
    
    matrix = readVectors(text_path)
    iw = sorted(matrix.keys())
    
    new_matrix = np.zeros(shape=(len(iw), len(matrix[iw[0]])), dtype=np.float32)
    for i, word in enumerate(iw):
        if word in matrix:
            new_matrix[i, :] = matrix[word]
    
    np.save(output_path+'.npy', new_matrix)

def readVectors(path):
    vectors = {}
    with open(path) as input_f:
        i = -1
        for line in input_f.readlines():
            i += 1
            if i <= 1:
                continue
            tokens = line.strip().split(' ')
            vectors[tokens[0]] = np.asarray([float(x) for x in tokens[1:]])
    return vectors


if __name__ == '__main__':
    main()
