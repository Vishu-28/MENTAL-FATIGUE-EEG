import numpy as np

def statistical_features(signal):

    mean = np.mean(signal)
    std = np.std(signal)
    kurt = np.mean((signal-mean)**4)

    return [mean, std, kurt]