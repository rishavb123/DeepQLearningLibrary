import numpy as np

def savgol_filter(y, window_size, degree): #Savitzky-Golay Filter
    y_smooth = []
    for x in range(len(y)):
        a = int(x - window_size / 2 if x >= window_size / 2 else 0)
        b = int(x + window_size / 2 if x + window_size < len(y) else len(y))
        p_vec = np.polyfit(range(a, b), y[a:b], degree)
        p = lambda x: np.dot([x ** d for d in range(degree + 1)], np.flip(p_vec))
        y_smooth.append(p(x))

    return y_smooth