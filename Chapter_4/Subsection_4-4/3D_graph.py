import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import ComputationFunctions.ComputationFunctions as cf
import numpy as np
import matplotlib.pyplot as plt

c = 343
phi = 180
theta = 90
M = 8
radius = 0.05
resolution = 3000
min_frequency = 20
max_frequency = 8000
# ------------------ GRAPH CALCULATIONS ------------------
frequencies_to_display = np.arange(min_frequency, max_frequency, 5)
radians_reference = np.linspace(0, 2 * np.pi, resolution)

X, Y = np.meshgrid(radians_reference, frequencies_to_display)
Z = np.empty((len(frequencies_to_display), resolution))
for frequency in range(0, len(frequencies_to_display)):
    beampattern = cf.cma_beampattern(theta, phi, frequencies_to_display[frequency], M, radius, c, resolution)
    beampattern_amplitudes = cf.signal_to_decibels([abs(x) for x in beampattern])
    Z[frequency] = beampattern_amplitudes
    if frequencies_to_display[frequency] % 100 == 0:
        print("Calculated already till "+str(frequencies_to_display[frequency])+" Hz")

ax = plt.axes(projection="3d")
ax.plot_surface(X, Y, Z, cmap='winter', rstride=10, cstride=10, linewidth=0)
ax.set_box_aspect([1, 3, 1])
ax.set_title(f"CMA directivity pattern at radius {radius} meters", weight='bold')
ax.set_xlabel("Degrees [radians]")
ax.set_ylabel("Frequency [Hz]")
ax.set_zlabel("Amplitude [dB]")

# # Defaultní rozsahy os
# default_xlim = ax.get_xlim()
# default_ylim = ax.get_ylim()
# default_zlim = ax.get_zlim()
#
# print("Defaultní rozsah os X:", default_xlim)
# print("Defaultní rozsah os Y:", default_ylim)
# print("Defaultní rozsah os Z:", default_zlim)
#
plt.show()
print("FINISHED")