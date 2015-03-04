from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import arange, ifft
from numpy import sin, linspace, pi, fft, abs
from scipy.io.wavfile import read,write
from nimble import cmds
import sys
import colorsys
# import maya.mel

def main():
    # set up audio for playback in Maya
    # audioNode = cmds.sound( offset=10, file=filename)
    # gPlayBackSlider = maya.mel.eval( '$tmpVar=$gPlayBackSlider' )
    # cmds.timeControl( gPlayBackSlider, edit=True, sound=audioNode )


    # read audio faile into raw data
    # filename = '../../resources/They Won\'t Go When I Go.wav'
    filename = '../../resources/Yesterday I Heard the Rain.wav'
    rate,data=read(filename)

    lastFrame = int(len(data)/float(rate) * 24)
    cmds.playbackOptions( min='1', max=str(lastFrame))

    y=data[:,1]
    bouncingBubble(y)
    exit()

def averageAmplitude(amp, sampleCount):
    avgs = list()
    accum = 0
    tenPercent = len(amp) // 10
    curProg = 1
    for i in range(len(amp)):
        accum += abs(amp[i])
        if i % sampleCount == 0 or i == len(amp) - 1:
            avgs.append(accum / sampleCount)
            accum = 0
        if i % tenPercent == 0 and not (curProg == 0 or curProg==10):
            sys.stdout.write(str(curProg) + '0%...')
            curProg += 1
    print('100%')
    return avgs

def bouncingBubble(amp):
    spf = 1838 # approximate samples per frame
    sphere = cmds.polySphere(n='bubble')[0]
    shader = str(cmds.listConnections(cmds.listHistory(sphere,f=1),type='lambert')[0])
    print('Created ' + sphere + ' with shader ' + shader)
    # cmds.xform('column', t = [0,.5,0], sp=[0,-.5,0]) # move scale pivot to bottom of shape

    frameWin = 3
    print('Calculating average amplitude for every ' + str(frameWin)
          + '-frame ('  + str(frameWin/24.) + ' second) ' + 'window')
    avgs = averageAmplitude(amp, spf * frameWin)
    curProg = 1
    tenPercent = len(avgs) / 10
    print('Keyframing size translations')
    for i in range(1,len(avgs)):
        h = normalize(avgs, i) * 10.
        cmds.setKeyframe(sphere, v = h, at = 'scaleX', t = i*frameWin)
        cmds.setKeyframe(sphere, v = h, at = 'scaleY', t = i*frameWin)
        cmds.setKeyframe(sphere, v = h, at = 'scaleZ', t = i*frameWin)
        if i % tenPercent == 0:
            if not (curProg == 0 or curProg == 10):
                sys.stdout.write(str(curProg) + '0%...')
                curProg += 1
    print('100%')

    frameWin = 60
    print('Calculating average amplitude for every ' + str(frameWin)
          + '-frame ('  + str(frameWin/24.) + ' second) ' + 'window')
    avgs = averageAmplitude(amp, spf*frameWin)
    curProg = 1
    tenPercent = len(avgs) / 10
    print('Keyframing color translations')
    for i in range(1,len(avgs)):
        norm = normalize(avgs, i)
        rgb = colorsys.hsv_to_rgb(norm, 1, norm) # hue and value both vary with amplitude
        # listConnections returns a list with unicode strings
        cmds.setAttr(shader + '.color', rgb[0], rgb[1], rgb[2], type='double3')
        cmds.setKeyframe(shader + '.color', at = 'color', t = i*frameWin)
        if i % tenPercent == 0:
            if not (curProg == 0 or curProg == 10):
                sys.stdout.write(str(curProg) + '0%...')
                curProg += 1
    print('100%')

def normalize(data, index):
    """
    Normalizes the value data[index] as a float between 0.0 and 1.0
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

"""
this code was formerly in main()

# lungime=len(y)
# timp=len(y)/float(rate)
# t=linspace(0,timp,len(y))

# subplot(2,1,1)
# plot(t,y)
# xlabel('Time')
# ylabel('Amplitude')
# subplot(2,1,2)
# plotSpectrum(y,Fs)
# show()
"""