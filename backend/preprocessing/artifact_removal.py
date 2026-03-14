import numpy as np

def remove_artifacts(signal):

    threshold = 100

    signal = np.clip(signal, -threshold, threshold)

    return signal