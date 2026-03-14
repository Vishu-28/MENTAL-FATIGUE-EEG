import numpy as np

def segment(signal, window=256, step=128):

    segments = []

    for i in range(0, len(signal)-window, step):

        segments.append(signal[i:i+window])

    return np.array(segments)