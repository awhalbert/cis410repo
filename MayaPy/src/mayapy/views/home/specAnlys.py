from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import arange, ifft
from numpy import sin, linspace, pi, fft, abs
from scipy.io.wavfile import read,write
from nimble import cmds

def plotSpectrum(y,Fs):
    n = len(y) # number of samples
    k = arange(n) # enumerate k integers [0,n)
    T = n/Fs # number of samples / sampling rate = time
    frq = k/T #
    print('freq: ' + str(frq))
    frq = frq[range(n/2)] # one side frequency range


    Y = fft.rfft(y)/n # fft computing and normalization
    print('test1')

    Y = Y[range(n/2)]

    plot(frq,abs(Y),'r') # plotting the spectrum
    xlabel('Freq (Hz)')
    ylabel('|Y(freq)|')

def main():
    Fs = 44100;  # sampling rate

    filename = 'They Won\'t Go When I Go.wav'
    rate,data=read('../../resources/' + filename)
    y=data[:,1]
    print(data)
    lungime=len(y)
    timp=len(y)/44100.
    t=linspace(0,timp,len(y))

    subplot(2,1,1)
    plot(t,y)
    xlabel('Time')
    ylabel('Amplitude')
    # subplot(2,1,2)
    # plotSpectrum(y,Fs)
    # show()
    bouncingBubble(y)
    exit()

def beatDetect(amp):
    avgs = list()
    spf = 1838 # number of samples per frame (1/24 second)
    sampleCount = spf * 3 # this grabs 3 frames (.125 s) of audio
    accum = 0
    for i in range(len(amp)):
        accum += amp[i]
        if i % sampleCount == 0 or i == len(amp) - 1:
            # this happens once per second
            avgs.append(accum / sampleCount)
            accum = 0
    print(len(avgs))
    return avgs

def bouncingBubble(amp):
    kfps = 24 # keyframes per second

    name = 'bubble'
    cmds.polyCube(n=name)
    cmds.xform('bubble', sp=[0,-.5,0]) # move scale pivot to bottom of shape

    avgs = beatDetect(amp)
    span = max(avgs) - min(avgs)
    for i in range(1,len(avgs)):
        normalized = float(avgs[i] - min(avgs))/span # normalized between 0 and 1
        h = normalized * 10.
        cmds.setKeyframe(name, v = h, at = 'scaleY', t = i*3)

if __name__ == '__main__':
    main()
