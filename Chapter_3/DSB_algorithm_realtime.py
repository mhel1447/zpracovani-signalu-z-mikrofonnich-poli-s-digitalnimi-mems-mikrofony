"""
This script is calculating delays on the 8 microphone channels in real time.

First off, it prints input/output audio devices with their id. At the start please see which id is
currently holding the microphone array input and set it in variable sd.default.device. Second number is 
ID of an output device (e.g. your computer speakers).IDs usually differes every time you turn on the
computer or plug in or remove any audio devices.

Duration of the programm can be specified in seconds in variable duration. Output signal is saved in
output_data folder.
"""
import sys
import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write 

# Import of ComputationFunctions from different directory
current_dir = os.path.dirname(__file__)
computation_functions_path = os.path.join(current_dir, '..', 'ComputationFunctions')
computation_functions_path = os.path.abspath(computation_functions_path)
sys.path.append(computation_functions_path)
import ComputationFunctions as cf

print(sd.query_devices())
duration = 3  # determines how long a program should run in seconds
sd.default.device = 3, 4  # Selection of input and output devices (usually different for every computer)

# ------------------------------------------------------------
# ------------------- VARIABLES DEFINITION -------------------
# ------------------------------------------------------------
radius = 0.05  # radius of a circular microphone array in meters
M = 8  # number of microphones in circular microphone array
theta = 90
phi = 0
c = 343  # speed of sound in meters/seconds
sampling_frequency = 48000  # sampling frequency of microphones in Hz

buffer_size = 4800
channels_in = 8
history = None
previous_buffer = np.zeros((buffer_size, channels_in))
recording_normal = np.empty((0, channels_in))
recording_dsb = np.empty((0, 1))
round_delays_to_decimal_spaces = 2
delays = cf.cma_tmi(radius, M, phi, theta, c)
sample_delays = cf.quantize_tmi_to_samples(delays, sampling_frequency)

# ----------------------------------------------------------------
# ------------------------- CALCULATIONS -------------------------
# ----------------------------------------------------------------

def delay_signal_by_frames(delays: list, input_buffer: np.array, delay_buffer: np.array) -> np.array:
    """
    This function takes in previous buffer and uses it to delay data in the current "input_buffer" buffer. It re
    Signal cannot be delayed by more samples than the size of the buffer.
    :param delays: list of delays, where index of an array matches channel number
    :param input_buffer: current buffer
    :param delay_buffer: previous buffer
    :return:
    """
    if delays == 0:
        return input_buffer
    history = delay_buffer[-delays:]
    delayed_signal = np.concatenate((history, input_buffer))
    delayed_signal = delayed_signal[:-delays]
    return delayed_signal

def callback(indata, outdata, frames, time, status):
    """
    This function delays signal in real time by using global variable delay_buffer to remember signals from the previous
    buffer. Both delayed and not delayed signal is then stored in global variables "recording_normal" and "recording_delayed"
    and then stored in wav files to the output_data folder.

    Delayed signal is stored in outdata and then played by sounddevice library in the device's speakers (delayed
    signal is converted to stereo for 2 user's device speakers).
    :param indata: Input data
    :param outdata: Output data
    :param frames:
    :param time:
    :param status:
    """
    # If the signal is too low it can be amplified by raising value of this variable
    gain = 1
    # Rearanging microphones in the correct order
    indata = indata[:, (4, 0, 5, 1, 6, 2, 7, 3)]
    # Delaying signal
    global previous_buffer
    delayed_ch1 = delay_signal_by_frames(sample_delays[0], indata[:, 0], previous_buffer[:, 0])
    delayed_ch2 = delay_signal_by_frames(sample_delays[1], indata[:, 1], previous_buffer[:, 1])
    delayed_ch3 = delay_signal_by_frames(sample_delays[2], indata[:, 2], previous_buffer[:, 2])
    delayed_ch4 = delay_signal_by_frames(sample_delays[3], indata[:, 3], previous_buffer[:, 3])
    delayed_ch5 = delay_signal_by_frames(sample_delays[4], indata[:, 4], previous_buffer[:, 4])
    delayed_ch6 = delay_signal_by_frames(sample_delays[5], indata[:, 5], previous_buffer[:, 5])
    delayed_ch7 = delay_signal_by_frames(sample_delays[6], indata[:, 6], previous_buffer[:, 6])
    delayed_ch8 = delay_signal_by_frames(sample_delays[7], indata[:, 7], previous_buffer[:, 7])
    added_signals = np.empty((4800, 1))
    global M
    for i in range(0, len(delayed_ch1)):
        added_signals[i] = (delayed_ch1[i] + 
                            delayed_ch2[i] + 
                            delayed_ch3[i] + 
                            delayed_ch4[i] + 
                            delayed_ch5[i] + 
                            delayed_ch6[i] + 
                            delayed_ch7[i] + 
                            delayed_ch8[i]) / M
        added_signals[i] *= gain
    # Saving data into delay buffer for next time
    previous_buffer = indata.copy()

    # output stream
    outdata[:, 0] = added_signals[:, 0]
    outdata[:, 1] = added_signals[:, 0]

    # Recording both added and not modified signal together for later analysis
    global recording_normal
    global recording_dsb
    recording_normal = np.concatenate((recording_normal, indata))
    recording_dsb = np.concatenate((recording_dsb, added_signals))

with sd.Stream(samplerate=sampling_frequency, channels=[8, 2], callback=callback, blocksize=buffer_size):
    sd.sleep(int(duration * 1000))
    # Saving recorded data in wav files
    write("zpracovani-signalu-z-mikrofonnich-poli-s-digitalnimi-mems-mikrofony/Chapter_3/output_data/output_dsb.wav", sampling_frequency, recording_normal)
    write("zpracovani-signalu-z-mikrofonnich-poli-s-digitalnimi-mems-mikrofony/Chapter_3/output_data/output_8ch_not_processed.wav", sampling_frequency, recording_dsb)
    print("Finished")
    