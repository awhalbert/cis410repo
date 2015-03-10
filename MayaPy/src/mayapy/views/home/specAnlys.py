import pylab as plt
import numpy
import scipy.io.wavfile as wav
import scipy.fftpack
from nimble import cmds
import sys
import colorsys
from mayapy.views.home.Scene import DropScene
from mayapy.views.home.Scene import BoxScene


def main():
    # set up audio for playback in Maya
    # audioNode = cmds.sound( offset=10, file=filename)
    # gPlayBackSlider = maya.mel.eval( '$tmpVar=$gPlayBackSlider' )
    # cmds.timeControl( gPlayBackSlider, edit=True, sound=audioNode )


    # read audio faile into raw data
    #filename = '../../resources/They Won\'t Go When I Go.wav'
    #filename = '../../resources/Yesterday I Heard the Rain.wav'
    #filename = '../../resources/220-440-880Hz.wav'
    filename = '../../resources/Ouroboros.wav'

    print "Reading file " + filename + "..."
    rate,data=wav.read(filename)

    print "Creating Scenes..."
    scene = BoxScene(data.T[0], rate, 0, int(1e4), (-10, 1, 2))

    print "Animating Scenes..."
    scene.animate()


    # normalize data from -1 to 1
    norms = data / (2.**15)
    print "Length of audio:"
    print str(norms.shape[0]/rate) + ' Seconds'
    print "Audio Shape:"
    print data.shape

    lastFrame = int(len(norms)/float(rate) * 24)
    cmds.playbackOptions( min='1', max=str(lastFrame))

    #bouncingBubble(data.T[0], rate)
    #exit()


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

def getMax(amp, sampRate, beginFreq, endFreq):
    #fftResult = numpy.fft.rfft(amp[beginSamp:endSamp]) # calculate fft
    fftResult = numpy.fft.fft(amp) # calculate fft
    fftFreq = numpy.abs(numpy.fft.fftfreq(len(fftResult))*sampRate)

    fftResult = fftResult[:len(fftResult)/2]
    fftFreq = fftFreq[:len(fftFreq)/2]
    #print "Sizes: ", len(fftResult), len(amp[beginSamp:endSamp])
    #fftResult = numpy.abs(fftResult[0:len(fftResult)/2]) # only get symmetric side
    #plt.plot(fftResult)
    #print str(len(fftResult))
   # print len(fftResult)
    #beginFreq = beginFreq*len(fftResult)
    #endFreq = endFreq*len(fftResult)
    beginIndex = 0
    endIndex = len(fftFreq)
    print beginFreq, endFreq, numpy.min(fftFreq), numpy.max(fftFreq)
    for i in range(len(fftFreq)):
        #if(i%5==0 and i+5 < len(fftFreq)):
            #print fftFreq[i], fftFreq[i+1], fftFreq[i+2], fftFreq[i+3], fftFreq[i+4]

        if(i+1 <= len(fftFreq) and fftFreq[i] <= beginFreq and fftFreq[i+1] > beginFreq):
            print "Begin index: ", fftFreq[i], fftFreq[i+1], beginFreq
            beginIndex = i
        if(i > 0 and fftFreq[i] >= endFreq and fftFreq[i-1] < endFreq):
            print "End index: ", fftFreq[i], fftFreq[i-1], endFreq
            endIndex = i

    print
    idx = numpy.argmax(numpy.abs(fftResult[beginIndex:endIndex]))
    #print "Max is from " + str(beginIndex) + " to " + str(endIndex)
    return numpy.abs(fftResult[idx])
    '''
    print fftFreq[idx], fftResult[idx]
   # fftFreq = fftFreq[0:len(fftFreq)/2]
   # idx = numpy.argmax(fftResult[beginFreq:endFreq])
   # print fftFreq[idx]*sampRate
    #print [str(ele) for ele in fftFreq]
    print fftFreq.min(), fftFreq.max()
    startidx = int(beginFreq*len(fftFreq)/2)
    endidx = int(endFreq*len(fftFreq)/2)
    print fftFreq[0], fftFreq[(len(fftFreq)/2)]
    print "finding freqs from " + str(fftFreq[startidx]) + " to " + str(fftFreq[endidx])
    #print "finding freqs from " + str(beginFreq*len(fftResult)) + " to " + str(endFreq*len(fftResult))
    max = numpy.max(fftResult[startidx:endidx])
    return numpy.abs(max)
    '''

def bouncingBubble(amp, sampFreq):
    '''
    timeArray = numpy.arange(0, amp.shape[0], 1)
    timeArray = timeArray / sampFreq
    timeArray = timeArray * 1000
    '''

    wholeFFT = numpy.fft.rfft(amp)
    fftFreq = numpy.abs(numpy.fft.fftfreq(len(wholeFFT)))
    wholeFFT = numpy.abs(wholeFFT[0:len(wholeFFT)/2])
    fftFreq = fftFreq[:len(fftFreq)/2]
    normalizeFactor = numpy.max(numpy.abs(wholeFFT))
    print "Most prominent frequency has value " + str(normalizeFactor)

    numFreqs = 10;
    freqsPerBox = len(wholeFFT)/numFreqs
    #print "Number of frequencies:", numFreqs, "", "Total Frequencies:", len(wholeFFT)
    objects = list()
    framesPerKeyframe = 3
    secsPerKeyframe = 3/24.
    totalFrames = 24*amp.shape[0]/sampFreq
    for i in range(numFreqs):
        objects.append(cmds.polyCube(n='VisBox')[0])
        #print "Keyframing object " + objects[i]
        cmds.xform(t=(2*i, 0, 0))
        beginFreq = 220*i
        endFreq = 220*(i+1)
        '''
        beginFreq = i*freqsPerBox/float(len(wholeFFT))
        endFreq = (i+1)*freqsPerBox/float(len(wholeFFT))
        '''
        #print "Frequencies " + str(beginFreq) + "-" + str(endFreq)
        print "===================="
        print "Keyframing Box " + objects[i] + " (Frequencies " + str(beginFreq) + " to " + str(endFreq) + ")"
        print "===================="
        for f in range(0, totalFrames, framesPerKeyframe):
            curSamp = f*amp.shape[0]/totalFrames
            endSamp = curSamp+(secsPerKeyframe*sampFreq)
            #print "Setting keyframe at frame: " + str(f)
            #print "Searching samples " + str(curSamp) + "-" + str(endSamp)

            #fftPiece = numpy.fft.fft(amp[curSamp:endSamp])
            #fftPiece = numpy.abs(fftPiece[0:len(fftPiece)/2])/normalizeFactor
            #power = numpy.max(numpy.abs(fftPiece[beginFreq:endFreq]))/normalizeFactor
            power = getMax(amp[curSamp:endSamp], sampFreq, beginFreq, endFreq)/normalizeFactor
            print "Frame " + str(f) + " = " + str(power)
           # objects[i].scale(1, power*10, 1)
            #print "ScaleY is: " + str(abs(power))
            cmds.setKeyframe(objects[i], v=power, at='scaleY', t=f)
        print ""
    #plt.show()
            #if i==0:
               # plt.plot(fftPiece)
   # plt.show()





        #fftPiece = numpy.fft.fft(amp[i*freqsPerBox:(i+1)*freqsPerBox])

'''

    for i in range(0, len(amp), 1000):
        fftPiece = numpy.fft.fft(amp[i:i+1000])
        idx = numpy.argmax(numpy.abs(fftPiece))
        print i/1000, abs(numpy.fft.fftfreq(len(fftPiece))[idx])*sampFreq

    exit()
    #plt.plot(abs(fftResult[:len(fftResult)/2]), 'r')
    plt.show()


    spf = sampFreq/24 # approximate samples per frame
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

    frameWin = 10
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
    '''

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