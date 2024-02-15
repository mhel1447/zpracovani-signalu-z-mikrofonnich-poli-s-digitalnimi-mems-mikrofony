"""
This file plots processed data to 3 polar plots for 3 predefined frequencies. All 3 desired frequencies
are defined in list "frequencies" in "VARIABLES DEFINITION" part of the script. In the thesis the data
has been generated for 2000, 4000, 6000, 10000, 14000 and 18000 Hz.
"""
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import ComputationFunctions.ComputationFunctions as cf

# ------------------------------------------------------------
# ------------------- VARIABLES DEFINITION -------------------
# ------------------------------------------------------------
frequencies = [2000, 4000, 6000]
frequency = 5000  # Hz
radius = 0.05  # meters
phi = 0  # degrees
theta = 90 # degrees
M = 8
c = 343  # meters/second
resolution = 100
quantize_frequency = 48000  # Hz

# -------------------------------------------------------------
# ------------- REFERENCE BEAM PATTERN CALCULATION ------------
# -------------------------------------------------------------

beampatterns_calculated = []
for freq in frequencies:
    beampattern_normal = cf.cma_beampattern(theta, phi, freq, M, radius, c, resolution)
    amplitudes_normal = cf.signal_to_decibels([np.abs(x) for x in beampattern_normal])

    beampatterns_calculated.append(amplitudes_normal)

# -------------------------------------------------------------
# ------------- REFERENCE BEAM PATTERN CALCULATION ------------
# -------------------------------------------------------------
beampatterns_measured = []
for freq in frequencies:
    spectral_values = np.zeros(100, dtype=float)
    for i in range(0, 200, 2):
        # Load data from files
        wav_file_path = ""
        if (i < 10):
            wav_file_path = f"Processed_recordings/krok_00{i}_processed.wav"
        elif (i < 100):
            wav_file_path = f"Processed_recordings/krok_0{i}_processed.wav"
        else:
            wav_file_path = f"Processed_recordings/krok_{i}_processed.wav"
        data, samplerate = sf.read(wav_file_path)

        # Remove DC Offset
        means = data.mean(0)
        means_array = np.tile(means, (data.shape[0], 1))
        for j in range(0, data.shape[0]):
            data[j] = data[j].item() - means_array[j].item()

        # FFT analysis
        spectrum = abs(np.fft.fft(data, axis=0))
        chosen_frequency_sample_number = int(np.floor(data.shape[0] * freq / samplerate))
        # Convert to decibels
        spec_db = 20*np.log10(spectrum)
        spectral_values[int(i/2)] = spec_db[chosen_frequency_sample_number]

    # -------- NORMALIZING SPECTRAL VALUES TO 0 dB --------
    max_spectr_vals = spectral_values.max()
    spectral_values = spectral_values - abs(max_spectr_vals)
    beampatterns_measured.append(spectral_values)

# ------------------------------------------------
# --------------- DISPLAYING PLOTS ---------------
# ------------------------------------------------
reference_radians_values = np.linspace(0, 2 * np.pi, 100)

fig, axes = plt.subplots(ncols=3, subplot_kw={'projection': 'polar'}, figsize=(10.3, 3), dpi=300)
for cols in range(0, 3):
    axes[cols].plot(reference_radians_values, beampatterns_calculated[cols], color='green', linewidth='1.2')
    axes[cols].plot(reference_radians_values, beampatterns_measured[cols], color='red', linewidth='1.2')
    axes[cols].set_ylim([-40, 0])
    axes[cols].set_title(f"{frequencies[cols]} Hz", va='bottom')
    box = axes[cols].get_position()
    axes[cols].set_position([box.x0, box.y0, box.width * 0.9, box.height * 0.9])
    axes[cols].set_yticks([-40, -30, -20, -10, 0])

plt.show()


