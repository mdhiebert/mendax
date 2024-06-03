import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

def read_iq_data(file_path, dtype=np.int16, max_samples=None):
    # Read the binary file
    raw_data = np.fromfile(file_path, dtype=dtype)
    
    if max_samples:
        raw_data = raw_data[:max_samples * 2]  # Since I and Q are interleaved
    
    # Separate I and Q components
    I = raw_data[0::2]
    Q = raw_data[1::2]
    
    # Normalize data if using int8 or int16
    if dtype == np.int8:
        I = I / 128.0
        Q = Q / 128.0
    elif dtype == np.int16:
        I = I / 32768.0
        Q = Q / 32768.0
    
    # Combine I and Q into complex numbers
    complex_data = I + 1j * Q
    
    return I, Q, complex_data

def plot_spectrogram(complex_data, fs, nperseg=256):
    # Calculate the spectrogram
    f, t, Sxx = spectrogram(complex_data, fs=fs, nperseg=nperseg)
    
    # Plot the spectrogram
    plt.figure(figsize=(14, 6))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.title('Spectrogram')
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.colorbar(label='Intensity [dB]')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Replace 'path_to_your_file.bin' with the path to your I/Q data file
    file_path = 'data\hackrf_exps\exp_2_transfer.bin'
    
    # Read the I/Q data, limiting to a smaller subset
    max_samples = 1_000_000  # Adjust this number based on your system's capabilities
    I, Q, complex_data = read_iq_data(file_path, dtype=np.int16, max_samples=max_samples)  # Using int16 for higher resolution
    
    # Sampling rate (default for HackRF is 10 MHz)
    fs = 10e6  # 10 MHz
    
    # Plot the spectrogram with reduced FFT points
    plot_spectrogram(complex_data, fs, nperseg=256)
