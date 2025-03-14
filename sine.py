import numpy as np
import numpy.matlib
import struct

# bram parameters
block_size = 128  # <bram data_width>
bits_per_val = 16 # <rfdc input data size> 16 bits for rfsoc4x2
blocks = 2**13    # 2**<bram address_width>
num_vals = int(block_size / bits_per_val * blocks)

# sine wave parameters
fs = 1966.08e6      # Sampling frequency
fc = 393.216e6      # Carrier frequency
dt = 1/fs           # Time length between samples
tau = dt * num_vals # Time length of bram 

# Useful info if running from a script
print(f"fs = {fs}")
print(f"fc = {fc}")

# Setup our array
t = np.arange(0,tau,dt)

# Generate our sine wave
# frequency fc
# range 0, 1
x = 0.5*(1+np.cos(2*np.pi* fc *t))
# scale our function to use the whole DAC range
maxVal = 2**14-1
x *= maxVal
# set each value to a 16 bit integer, for DAC compatibility
x = np.round(np.short(x))
# Shift right, DAC is 14 bits
x <<= 2

# Save our array x as a set of bytes  
buf = bytes()
for i in x:
  buf += struct.pack('>h',i)

# We're done!, we can now write buf to our
# bram. To make sure it exists, enter len(buf)
# in your ipython terminal

# If needed we can save it as a file 
# for later use, or transferability  
f = open("sine.txt", "bw")
f.write(buf)