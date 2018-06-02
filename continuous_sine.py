import pyaudio
import numpy as np
import threading

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
f = None        # sine frequency, Hz, may be float
output = None


# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)


def generate(freq):
    # sin2pift
    f = float(freq)
    num_samples = int(fs*duration)
    global output
    samples = []
    for samp_count in range(0,num_samples):
        samples.append((volume*np.sin(2*np.pi*f*samp_count/fs))) # t = samp_count/fs
    output = np.array(samples, "Float32")

# play. May repeat with different volume values (if done interactively) 
# stream.write(samples*volume) - original
def play():
    while True:
        if(output != None):
            stream.write(output)

def read_freq():
    while True:
        freq = raw_input("Enter a frequency:\n")
        generate(freq)

try:
    a = threading.Thread(target=play)
    a.start()
    b = threading.Thread(target=read_freq)
    b.start()
except Exception:
    import traceback
    print traceback.format_exc()