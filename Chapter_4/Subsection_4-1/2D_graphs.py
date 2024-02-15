import ComputationFunctions.ComputationFunctions as cf
import numpy as np
import matplotlib.pyplot as plt

# --------------- VARIABLES DECLARATIONS ---------------
frequencies = [2000, 4000, 6000]  # Frequencies used to calculate 3 graphs at the time
c = 343
theta = 90
M = 8
radius = 0.05
resolution = 2000

# --------------- BEAMPATTERN CALCULATION ---------------
beampatterns = []

for freq in frequencies:
    beampattern_normal = cf.cma_beampattern(theta, 0, freq, M, radius, c, resolution)
    amplitudes_normal = cf.signal_to_decibels([np.abs(x) for x in beampattern_normal])

    beampattern_30 = cf.cma_beampattern(theta, 30, freq, M, radius, c, resolution)
    amplitudes_30 = cf.signal_to_decibels([np.abs(x) for x in beampattern_30])

    beampatterns.append((amplitudes_normal, amplitudes_30))

# --------------- DISPLAYING PLOTS ---------------

fig, axes = plt.subplots(ncols=3, subplot_kw={'projection': 'polar'}, figsize=(10.3, 3), dpi=200)
reference_radians_values = np.linspace(0, 2 * np.pi, resolution)
for cols in range(0, 3):
    #axes[cols].plot(reference_radians_values, beampatterns[cols][1], color='#96BAFF', linewidth='1.2')
    axes[cols].plot(reference_radians_values, beampatterns[cols][0], color='green', linewidth='1.2')
    axes[cols].set_ylim([-40, 0])
    axes[cols].set_title(f"{frequencies[cols]} Hz", va='bottom')
    box = axes[cols].get_position()
    axes[cols].set_position([box.x0, box.y0, box.width * 0.9, box.height * 0.9])
    axes[cols].set_yticks([-40, -30, -20, -10, 0])

plt.show()