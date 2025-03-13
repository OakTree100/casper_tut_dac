import numpy as np
import numpy.matlib
import struct

block_size = 128  # <bram data_width>
bits_per_val = 16 # <rfdc input data size> 16 bits for rfsoc4x2
blocks = 2**13    # 2**<bram address_width>
num_vals = np.int32(block_size / bits_per_val * blocks) # numpy > 1.20

fs = 1966.08e6      # Sampling frequency
fc = 393.216e6      # Carrier frequency
dt = 1/fs           # Time length between samples
tau = dt * num_vals # Time length of bram 

print(f"fs = {fs}, fc = {fc}")
print(f"dt = {dt}, tau = {tau}")

if (False):
    if(repeats == round(repeats)):
        print(f"repeats = {repeats}")
        repeats = fs/fc
        nice_len = num_vals - (num_vals % repeats)
        print(f"Consider setting your waveform length to {round(nice_len)}")


t = np.arange(0,tau,dt)
print('Expected ' + str(num_vals) + ' values. Got ' + str(len(t)))

x = 0.5*(1+np.cos(2*np.pi*(fc/fs*2000e6)*t))
maxVal = 2**13-1
x *= maxVal
x = np.round(np.short(x))
x <<= 2
# print(x[0:2*round(repeats)])

buf = bytes()
for i in x:
  buf += struct.pack('>h',i)
print(len(buf))
print(buf[0:8])

f = open("sine.txt", "bw")
f.write(buf)
