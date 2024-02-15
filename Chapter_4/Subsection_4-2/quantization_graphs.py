from ComputationFunctions import ComputationFunctions as cf
import numpy as np
import matplotlib.pyplot as plt

# --------------- VARIABLES DECLARATIONS ---------------
frequencies = [2000, 4000, 6000, 10000, 15000, 18000]
c = 343
phi = 20
theta = 90
M = 8
radius = 0.05
resolution = 2000
sampling_frequency = 48000

# --------------- BEAMPATTERN CALCULATION ---------------
beampatterns = []

for freq in frequencies:
    beampattern_normal = cf.cma_beampattern(theta, phi, freq, M, radius, c, resolution)
    amplitudes_normal = cf.signal_to_decibels([np.abs(x) for x in beampattern_normal])

    beampattern_quantized = cf.cma_beampattern_quantization(theta, phi, freq, M, radius, c, resolution, sampling_frequency)
    amplitudes_quantized = cf.signal_to_decibels([np.abs(x) for x in beampattern_quantized])

    beampatterns.append((amplitudes_normal, amplitudes_quantized))

# --------------- DISPLAYING PLOTS ---------------

fig, axes = plt.subplots(nrows=2, ncols=3, subplot_kw={'projection': 'polar'}, figsize=(10.3, 7), dpi=200)
reference_radians_values = np.linspace(0, 2 * np.pi, resolution)
beampatern_index = 0
for rows in range(0, 2):
    for cols in range(0, 3):
        axes[rows][cols].plot(reference_radians_values, beampatterns[beampatern_index][0], color='green', linewidth='1.2')
        axes[rows][cols].plot(reference_radians_values, beampatterns[beampatern_index][1], color='red', linewidth='1.2')
        axes[rows][cols].set_ylim([-40, 0])
        axes[rows][cols].set_title(f"{frequencies[beampatern_index]} Hz", va='bottom')
        box = axes[rows][cols].get_position()
        axes[rows][cols].set_position([box.x0, box.y0, box.width * 0.9, box.height * 0.9])
        axes[rows][cols].set_yticks([-40, -30, -20, -10, 0])
        beampatern_index += 1

plt.show()