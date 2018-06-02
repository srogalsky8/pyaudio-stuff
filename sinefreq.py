"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import numpy as np

CHUNK = 2048

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read data
data = wf.readframes(CHUNK)

# play stream (3)
frame_count = 0
period_start = None
period_end = None

total_period_len = 0
num_periods = 0

overall_idx = 0
while len(data) > 0:
    data_array = np.fromstring(data, 'Int16')
    for idx, val in enumerate(data_array):
        overall_idx += 1
        if (idx == 0):
            pass
        elif (idx == (len(data)-1)):
            pass
        elif (data_array[idx-1]<=0 and val > 0):
            if(period_start == None):
                period_start = overall_idx
            else:
                period_end = overall_idx
        
        if(period_start and period_end):
            period_found = True
            total_period_len += (period_end - period_start)
            num_periods += 1

            period_start = period_end
            period_end = None
    frame_count = frame_count + 1
    # stream.write(data)
    data = wf.readframes(CHUNK)

print total_period_len

avg_period_len = total_period_len/num_periods # average num of samples per period
freq = wf.getframerate() / avg_period_len
print "frequency: " + str(freq) + "Hz"

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()