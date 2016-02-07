import math, string 

# Read raw data.
data=open("keysound1_ampl.wav","rb").read()[44:]
samples=[]
for i in range(len(data)/2):
    smp=ord(data[i*2+1])*256+ord(data[i*2])
    if smp>=256*256/2:
        smp-=256*256
    samples.append(smp)
print "Got samples from file..."

RAVG=400 # Running average length
THR=4600 # Threshold of peak finding
HYST=100 # Hysteresis of peak finding
PEAKLEN=600 # Length (in samples) of one key press
SIM_THR=1000 # Similarity threshold
UNK_SAMPLES=42 # Number of key presses, after which known text begins

# Calculate root running mean square.
ravg=[]
sm=0
for i in range(RAVG/2,len(samples)):
    if i>=RAVG*3/2:
        sm-=samples[i-RAVG]**2
    sm+=samples[i]**2
    ravg.append(3*math.sqrt(sm/(RAVG+0.0)))
print "Calculated rms..."

# Find peaks (key presses).
i=0
peaks=[]
while i<len(ravg):
    if ravg[i]<THR+HYST:
        i+=1
        continue
    mx=0
    mxind=i
    while i<len(ravg) and ravg[i]>THR-HYST:
        if ravg[i]>mx:
            mx=ravg[i]
            mxind=i
        i+=1
    peaks.append(mxind)
print "Found peaks..."

# Getting samples of each character.
chardata={}
for i, char in enumerate(open("Blog Text.txt").read()):
    peak=peaks[i+UNK_SAMPLES]
    peakdata=samples[peak-PEAKLEN:peak+PEAKLEN]
    if char not in chardata:
        chardata[char]=[peakdata]
    else:
        chardata[char].append(peakdata)
print "Gathered character samples..."

def difference(arr1, arr2):
    sm=0
    for i in range(len(arr1)):
        sm+=(arr1[i]-arr2[i])**2
    return sm/len(arr1)

# Finding best fit for unknown key presses.
unkpeaks=sorted(peaks[:UNK_SAMPLES]+[137259]) # One of keypresses was not detected.
for peak in unkpeaks:
    unk_key=samples[peak-PEAKLEN:peak+PEAKLEN]
    s="["
    for c in chardata:
        for arr in chardata[c]:
            if difference(unk_key, arr)<SIM_THR:
                s=s+c
                break
    s=s+"]"
    print s,
print ""
