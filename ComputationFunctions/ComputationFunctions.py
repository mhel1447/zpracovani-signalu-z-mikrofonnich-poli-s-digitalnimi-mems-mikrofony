"""
Source code for all essential functions used along the thesis are defined in this python file. This is to avoid
copying code used in other scripts.
"""
import numpy as np

def degrees_to_radians(degrees):
    """ Converts degrees to radians """
    return degrees * (np.pi / 180)

def signal_to_decibels(signal, reference=1):
    """ Converts signal given in unitless format to decibels """
    decibels = []
    for i in signal:
        decibels.append(10 * np.log10(i / reference))
    return decibels

def quantize_tmi(latencies, sampling_frequency):
    minimum_latency = (1 / sampling_frequency)
    result = []
    for i in latencies:
        result.append(round(i / minimum_latency)*minimum_latency)
    return result

def quantize_tmi_to_samples(latencies: list, sampling_frequency: int) -> list:
    """
    Takes an array of latencies as an input and returns them back quantized to a given sampling frequency.
    Most common sampling frequencies are 44.1 kHz, 48 kHz and 96 kHz.
    :param latencies: input Latencies ment to be quantized.
    :param sampling_frequency: Sampling frequency for quantization.
    :return: Array of latencies quantized to certain sampling frequency.
    """
    minimum_latency = (1 / sampling_frequency)
    result = []
    for i in latencies:
        result.append(round(i / minimum_latency))
    return result

def cma_tmi(radius: float, M: int, phi_angle: float, theta_angle: float, c: int) -> list:
    """
    Calculates delay times on all microphones in circular microphone array. Results are stored and returned in a list,
    which indices are matching indices of each microphone.
    :param radius: radius of circular microphone array
    :param M: number of microphones in circular microphone array
    :param phi_angle: horizontal angle of a sound source
    :param theta_angle: vertical angle of a sound source
    :param c: speed of sound
    :return: list of delays where every index of the list corresponds to the microphone index delay
    """
    latencies = []
    k_hat_vector = np.array([
        np.sin(degrees_to_radians(theta_angle)) * np.cos(degrees_to_radians(phi_angle)),
        np.sin(degrees_to_radians(theta_angle)) * np.sin(degrees_to_radians(phi_angle)),
        np.cos(degrees_to_radians(theta_angle))
    ])
    # Dot product for k_hat and r_m_i for all mics
    for mic_id in range(M):
        rm_vector = radius * np.array([
            np.cos(2 * np.pi * (mic_id / M)),
            np.sin(2 * np.pi * (mic_id / M)),
            0
        ])
        t_m_i = np.dot(k_hat_vector, rm_vector)/c
        latencies.append(t_m_i)
    # Find smallest t_m_i and adds it to the latencies according to fomrula 1.2
    t_m_c = np.max(latencies)
    for i in range(M):
        latencies[i] = t_m_c - latencies[i]
    return latencies

def cma_beampattern(theta: float, phi: float, frequency: int, M: int, radius: float, c: int, resolution: int) -> list:
    """
    This function calculates beam pattern of circular microphone array. Beam pattern is calculated in frequency domain,
    therefore frequency as a parameter is required. Returned data are best displayed on polar plot.
    :param theta: vertical angle of a sound source
    :param phi: horizontal angle of a sound source
    :param frequency: frequency of a beam pattern
    :param M: number of microphones in circular microphone array
    :param radius: radius of circular microphone array
    :param c: speed of sound
    :param resolution: number of points that should be generated in range of 0..360 degrees
    :return: list of all magnitudes of the signals dispersed in directions of 0.360 degrees
    """
    ro = 2 * np.pi * frequency
    beampattern = []
    tmcmi = cma_tmi(radius, M, phi, theta, c)
    degrees_resolution = np.linspace(0, 360, resolution)
    # Calculate H_DSB according to formula 1.4
    for phi_s in degrees_resolution:
        kj = cma_tmi(radius, M, phi_s, theta, c)
        sum = 0
        for index in range(0, M):
            sum += np.exp(1j * ro * (tmcmi[index] - kj[index]))
        beampattern.append(sum / M)
    return beampattern

def cma_beampattern_quantization(theta: float, phi: float, frequency: int, M: int, radius: float, c: int, resolution: int, sf: int) -> list:
    """
    This function calculates beam pattern of circular microphone array. Beam pattern is calculated in frequency domain,
    therefore frequency as a parameter is required. Returned data are best displayed on polar plot.
    :param theta: vertical angle of a sound source
    :param phi: horizontal angle of a sound source
    :param frequency: frequency of a beam pattern
    :param M: number of microphones in circular microphone array
    :param radius: radius of circular microphone array
    :param c: speed of sound
    :param resolution: number of points that should be generated in range of 0..360 degrees
    :return: list of all magnitudes of the signals dispersed in directions of 0.360 degrees with applied quantization.
    """
    ro = 2 * np.pi * frequency
    result = []
    tmcmi = quantize_tmi(cma_tmi(radius, M, phi, theta, c), sf)
    degrees_resolution = np.linspace(0, 360, resolution)
    # Calculate H_DSB according to formula 1.4
    for phi_s in degrees_resolution:
        kj = cma_tmi(radius, M, phi_s, theta, c)
        sum = 0
        for index in range(0, M):
            sum += np.exp(1j * ro * (tmcmi[index] - kj[index]))
        result.append(sum / M)
    return result