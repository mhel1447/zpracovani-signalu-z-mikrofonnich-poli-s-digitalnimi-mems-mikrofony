import ComputationFunctions.ComputationFunctions as cf
import numpy as np
import matplotlib.pyplot as plt

# --------------- VARIABLES DECLARATIONS ---------------
frequency = 2000
c = 343
phi = 0
theta = 90
M = 8
radius = 0.05
resolution = 1000

# --------------- BEAMPATTERN CALCULATION ---------------

beampattern = cf.cma_beampattern(theta, phi, frequency, M, radius, c, resolution)
amplitudes = cf.signal_to_decibels([np.abs(x) for x in beampattern])

# --------------- DISPLAY PLOT ---------------

fig, axes = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(3, 3), dpi=200)
reference_radians_values = np.linspace(0, 2 * np.pi, resolution)
axes.plot(reference_radians_values, amplitudes)
axes.set_ylim([-40, 0])
axes.set_yticks([-40, -30, -20, -10, 0])

plt.show()