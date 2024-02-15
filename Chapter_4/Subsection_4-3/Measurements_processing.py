"""
This script applies DSB algorithm to measured data by David Vágner, Jan Šedivý and David Ringsmuth. The output data
are then stored in "Processed_recordings" folder.
"""
import soundfile as sf
import numpy as np
import ComputationFunctions.ComputationFunctions as cf

# ------------------------------------------------------------
# ------------------- VARIABLES DEFINITION -------------------
# ------------------------------------------------------------
MIC_ORDER = [3, 4, 6, 0, 2, 5, 7, 1]  # Sorting channels in the correct positions
radius = 0.05  # in meters
M = 8
phi = 0  # degrees
theta = 90  # degrees
c = 343  # meters/second
sampling_frequency = 48000  # Hz

# -------------------------------------------------------------
# ------------------- CALCULATION OF DELAYS -------------------
# -------------------------------------------------------------
delays_seconds = cf.cma_tmi(radius, M, phi, theta, c)
delays_samples = cf.quantize_tmi_to_samples(delays_seconds, sampling_frequency)
heighest_delay = max(delays_samples)

# ----------------------------------------------------------------
# ------------------- PROCESSING OF RECORDINGS -------------------
# ----------------------------------------------------------------
for i in range(0, 200, 2):
    # Load data from files
    wav_file = ""
    if (i < 10):
        wav_file = f"krok_00{i}"
    elif (i < 100):
        wav_file = f"krok_0{i}"
    else:
        wav_file = f"krok_{i}"
    data, samplerate = sf.read("measurement_2023-07-27_14-44/" + wav_file + ".wav")
    print(f"Processing of file {wav_file}.wav ...")

    # Rearrange microphones in correct order
    if data.shape[1] == 8:
        data[:, [0, 1, 2, 3, 4, 5, 6, 7]] = data[:, MIC_ORDER]

    data_delayed = np.zeros((52815, M))
    # Addition of delays
    for channel_index in range(0, data.shape[1]):
        data_delayed[:, channel_index] = np.pad(data[:, channel_index], (delays_samples[channel_index], heighest_delay-delays_samples[channel_index]), 'constant', constant_values=(0, 0))

    # Sum of all channels into a mono channel
    sum_signal = np.sum(data_delayed, axis=1) / data.shape[1]

    # Save files
    sf.write(f'Processed_recordings/{wav_file}_processed.wav', sum_signal, samplerate)
    print(f"File {wav_file}.wav processed!")