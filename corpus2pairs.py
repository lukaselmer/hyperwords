from collections import Counter
from math import sqrt
from random import Random

from docopt import docopt


def main():
    args = docopt("""
    Usage:
        corpus2pairs.py [options] <corpus>
    
    Options:
        --thr NUM    The minimal word count for being in the vocabulary [default: 100]
        --win NUM    Window size [default: 2]
        --pos        Positional contexts
        --dyn        Dynamic context windows
        --sub NUM    Subsampling threshold [default: 0]
        --oov        Remove out-of-vocabulary and subsampled placeholders
    """)
    
    corpus_file = args['<corpus>']
    thr = int(args['--thr'])
    win = int(args['--win'])
    pos = args['--pos']
    dyn = args['--dyn']
    subsample = float(args['--float'])
    sub = subsample != 0
    oov = args['--oov']
    
    vocab = readVocab(corpus_file, thr)
    corpus_size = sum(vocab.values())
    
    subsample *= corpus_size
    subsampler = dict([(word, 1-sqrt(subsample/count)) for word, count in vocab.items() if count > subsample])
    
    rnd = Random(17)
    with open(corpus_file) as f: 
        for line in f:
            
            toks = [t if t in vocab else None for t in line.strip().split()]
            if sub:
                toks = [t if t not in subsampler or rnd.random() > subsampler[t] else None for t in toks]
            if oov:
                toks = [t for t in toks if t is not None]
            
            len_toks = len(toks)
            
            for i, tok in enumerate(toks):
                if tok is not None:
                    if dyn:
                        dynamic_window = rnd.randint(1, win)
                    else:
                        dynamic_window = win
                    start = i - dynamic_window
                    if start < 0:
                        start = 0
                    end = i + dynamic_window + 1
                    if end > len_toks:
                        end = len_toks
                    
                    if pos:
                        output = '\n'.join([row for row in [tok + ' ' + toks[j] + '_'+str(j-i) for j in xrange(start, end) if j != i and toks[j] is not None] if len(row) > 0]).strip()
                    else:
                        output = '\n'.join([row for row in [tok + ' ' + toks[j] for j in xrange(start, end) if j != i and toks[j] is not None] if len(row) > 0]).strip()
                    if len(output) > 0:
                        print output

def readVocab(corpus_file, thr):
    vocab = Counter()
    with open(corpus_file) as f:
        for line in f:
            vocab.update(Counter(line.strip().split()))
    return dict([(token, count) for token, count in vocab.items() if count >= thr])


if __name__ == '__main__':
    main()
