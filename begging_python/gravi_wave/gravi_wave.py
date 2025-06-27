import imp
from tokenize import PlainToken
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

rate_h, hstrain = wavfile.read(r'H1_Strain.wav', 'rb')
print(rate_h,hstrain.shape)
rate_l, lstrain = wavfile.read(r'L1_Strain.wav', 'rb')
reftime, ref_H1 = np.genfromtxt('wf_template.txt').transpose()

htime_interval = 1/rate_h
ltime_interval = 1/rate_l

htime_len= hstrain.shape[0]/rate_h
htime = np.arange(-htime_len/2, htime_len/2, htime_interval)
ltime_len = lstrain.shape[0]/rate_l
ltime = np.arange(-ltime_len/2, ltime_len/2, ltime_interval)

fig = plt.figure(figsize=(12,6))

plth = fig.add_subplot(221)
plth.plot(htime, hstrain, 'y')
plth.set_xlabel('Time(seconds)')
plth.set_ylabel('H1 Strain')
plth.set_title('H1 strain')

pltl = fig.add_subplot(222)
pltl.plot(ltime, lstrain, 'g')
plth.set_xlabel('Time(seconds)')
plth.set_ylabel('L1 Strain')
plth.set_title('L1 strain')

pltref = fig.add_subplot(212)
pltref.plot(reftime, ref_H1)
pltref.set_xlabel('Time(seconds)')
pltref.set_ylabel('Template Strain')
pltref.set_title('Template')
fig.tight_layout()

fig.tight_layout()

plt.savefig('Gravtational_Waves_Orig.png')
plt.show()
plt.close(fig)