import numpy as np
from scipy.signal import welch

def band_power(signal, fs, band):

    fmin, fmax = band

    freqs, psd = welch(signal, fs)

    mask = (freqs >= fmin) & (freqs <= fmax)

    return np.mean(psd[mask])