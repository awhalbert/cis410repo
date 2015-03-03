from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import arange, ifft
from numpy import sin, linspace, pi, fft, abs
from scipy.io.wavfile import read,write
from nimble import cmds

def main():
    Fs = 44100;  # sampling rate

    filename = 'They Won\'t Go When I Go.wav'
    rate,data=read('../../resources/' + filename)
    cmds.playbackOptions( animationStartTime='1', animationEndTime='8640' )
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

def averageAmplitude(amp, sampleCount):
    avgs = list()
    accum = 0
    for i in range(len(amp)):
        accum += abs(amp[i])
        if i % sampleCount == 0 or i == len(amp) - 1:
            avgs.append(accum / sampleCount)
            accum = 0
    return avgs

def bouncingBubble(amp):
    spf = 1838 # approximate samples per frame

    sphere = cmds.polySphere(n='bubble')[0]

    # cmds.xform('column', t = [0,.5,0], sp=[0,-.5,0]) # move scale pivot to bottom of shape

    frameWin = 3

    avgs = averageAmplitude(amp, spf * frameWin) # this averages amplitude every frameWindow frames
    print(avgs)
    for i in range(1,len(avgs)):
        h = normalize(avgs, i) * 10.
        cmds.setKeyframe(sphere, v = h, at = 'scaleX', t = i*frameWin)
        cmds.setKeyframe(sphere, v = h, at = 'scaleY', t = i*frameWin)
        cmds.setKeyframe(sphere, v = h, at = 'scaleZ', t = i*frameWin)

    frameWin = 24
    avgs = averageAmplitude(amp, spf*frameWin) # this average amplitude every 24 frames (1 s)
    print(avgs)
    shader = str(cmds.listConnections(cmds.listHistory(sphere,f=1),type='lambert')[0])
    for i in range(2,len(avgs)):
        hue = normalize(avgs, i)
        # listConnections returns a list with unicode strings
        cmds.setAttr(shader + '.color', hue, 0, 0, type='double3')
        cmds.setKeyframe(shader + '.color', at = 'color', t = i*frameWin)

def normalize(data, index):
    """
    :param data: list of data to use for normalization
    :param index: index in data we wish to normalize among the set
    :return: the normalized value, a float between 0.0 and 1.0
    """
    return float(data[index] - min(data))/(max(data) - min(data))

if __name__ == '__main__':
    main()


"""
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
"""