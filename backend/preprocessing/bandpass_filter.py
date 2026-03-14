from scipy.signal import butter, lfilter

def bandpass_filter(data, low=4, high=45, fs=256):

    nyq = 0.5 * fs

    low = low / nyq
    high = high / nyq

    b, a = butter(5, [low, high], btype="band")

    return lfilter(b, a, data)