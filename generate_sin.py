import pyaudio
import numpy as np

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
# samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32) - original

# sin2pift
num_samples = int(fs*duration)
samples = []
for samp_count in range(0,num_samples):
    samples.append((volume*np.sin(2*np.pi*f*samp_count/fs))) # t = samp_count/fs
samples = np.array(samples, "Float32")

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively) 
# stream.write(samples*volume) - original
x=0
while(x<20):
    stream.write(samples)
    print x
    x= x+1

stream.stop_stream()
stream.close()

p.terminate()