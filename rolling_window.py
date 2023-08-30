import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Checks if there is a local peak detected at the current index


def detect_local_peak(data: np.array, curr_index: int, order: int) -> bool:
    if curr_index < order * 2 + 1:
        return False

    peak_detected = True
    k = curr_index - order
    v = data[k]
    for i in range(1, order + 1):
        if data[k + i] > v or data[k - i] > v:
            peak_detected = False
            break

    return peak_detected

# Checks if there is a local valley detected at the current index


def detect_local_valley(data: np.array, curr_index: int, order: int) -> bool:
    if curr_index < order * 2 + 1:
        return False

    valley_detected = True
    k = curr_index - order
    v = data[k]
    for i in range(1, order + 1):
        if data[k + i] < v or data[k - i] < v:
            valley_detected = False
            break

    return valley_detected


def find_extremes(data: np.array, order: int):
    # Rolling window local peaks and valleys
    peaks = []
    valleys = []
    for i in range(len(data)):
        if detect_local_peak(data, i, order):
            peak = [i, i - order, data[i - order]]
            peaks.append(peak)

        if detect_local_valley(data, i, order):
            valley = [i, i - order, data[i - order]]
            valleys.append(valley)

    return peaks, valleys


if __name__ == "__main__":
    financial_data = pd.read_csv(
        'data/EURUSD_Candlestick_4_Hour_ASK_05.05.2003-16.10.2021.csv')
    financial_data['date'] = pd.to_datetime(
        financial_data['date'], format='%d.%m.%Y %H:%M:%S.%f')
    financial_data = financial_data.set_index('date')

    financial_data = financial_data[:200]

    detected_peaks, detected_valleys = find_extremes(
        financial_data['close'].to_numpy(), 5)
    financial_data['close'].plot()
    idx = financial_data.index
    for peak in detected_peaks:
        plt.plot(idx[peak[1]], peak[2], marker='o', color='green')

    for valley in detected_valleys:
        plt.plot(idx[valley[1]], valley[2], marker='o', color='red')

    plt.show()
