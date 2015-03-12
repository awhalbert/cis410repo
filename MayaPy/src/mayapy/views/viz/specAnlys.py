import sys
import colorsys
import time

import numpy
import scipy.io.wavfile as wav

from nimble import cmds
from mayapy.views.viz.Scene import BoxOnSphereScene
from mayapy.views.viz.Box import BoxOnSphere


# from mayapy.views.home.Scene import DropScene

# TODO figured out why high frequencies aren't showing up as much
# it's because they are usually shorter sounds, and since we only sample really short
# lengths of time for high frequencies, we may completely miss many audible frequencies
# so we need to sample every frame length and then average every 3

def main(fn):
    startTime = time.time()
    # set up audio for playback in Maya
    # audioNode = cmds.sound( offset=10, file=filename)
    # gPlayBackSlider = maya.mel.eval( '$tmpVar=$gPlayBackSlider' )
    # cmds.timeControl( gPlayBackSlider, edit=True, sound=audioNode )


    # read audio faile into raw data
    filename = '../../resources/' + fn + '.wav'

    print "Reading file " + filename + "..."
    rate,data=wav.read(filename)
    lastFrame = int(len(data)/float(rate) * 24)
    cmds.playbackOptions( min='1', max=str(lastFrame))

    print "Creating Scenes..."
    sphere = bouncingBubble(data.T[0], rate)
    # scene = BoxScene(data.T[0], rate, 0, int(1e4), (-9, .5, 0))
    scene = BoxOnSphereScene(data.T[0], rate, 0, int(1e4), sphere)

    print "Animating Scenes..."
    scene.animate()


    # normalize data from -1 to 1
    norms = data / (2.**15)
    print "Length of audio:"
    print str(norms.shape[0]/rate) + ' Seconds'
    # print "Audio Shape:"
    # print data.shape

    elapsed = time.time() - startTime
    if elapsed >= 60:
        min = elapsed//60
        sec = elapsed % 60
    else:
        min = 0
        sec = elapsed
    print('Elapsed time: ' + str(int(min)) + 'm' + str(int(sec)) + 's')
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
    startRadius = 1.0 #2.865
    spf = sampFreq/24 # approximate samples per frame
    sphere = cmds.polySphere(n='bubble', r=startRadius)[0] # bakes in radius, scale of 1.0 makes radius 2.865
    shader = str(cmds.listConnections(cmds.listHistory(sphere,f=1),type='lambert')[0])

    print('Created ' + sphere + ' with shader ' + shader)
    # cmds.xform('column', t = [0,.5,0], sp=[0,-.5,0]) # move scale pivot to bottom of shape

    frameWin = BoxOnSphere.SPHERE_STEP
    print('Calculating average amplitude for every ' + str(frameWin)
          + '-frame ('  + str(frameWin/24.) + ' second) ' + 'window')
    avgs = averageAmplitude(amp, spf * frameWin)
    curProg = 1
    tenPercent = len(avgs) / 10
    scaleFactor = 10.0
    print('Keyframing size translations')
    for i in range(1,len(avgs)):
        h = normalize(avgs, i) * scaleFactor # take away or add + 1 to allow or disallow the sphere to decay infinitely small
        cmds.setKeyframe(sphere, v = h, at = 'scaleX', t = (i-1)*frameWin)
        cmds.setKeyframe(sphere, v = h, at = 'scaleY', t = (i-1)*frameWin)
        cmds.setKeyframe(sphere, v = h, at = 'scaleZ', t = (i-1)*frameWin)
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
        rgb = colorsys.hsv_to_rgb(norm, 1, min(norm + .2, 1)) # hue and value both vary with amplitude
        # listConnections returns a list with unicode strings
        cmds.setAttr(shader + '.color', rgb[0], rgb[1], rgb[2], type='double3')
        cmds.setKeyframe(shader + '.color', at = 'color', t = i*frameWin)
        if i % tenPercent == 0:
            if not (curProg == 0 or curProg == 10):
                sys.stdout.write(str(curProg) + '0%...')
                curProg += 1
    print('100%')
    return sphere
'''

    for i in range(0, len(amp), 1000):
        fftPiece = numpy.fft.fft(amp[i:i+1000])
        idx = numpy.argmax(numpy.abs(fftPiece))
        print i/1000, abs(numpy.fft.fftfreq(len(fftPiece))[idx])*sampFreq

    exit()
    #plt.plot(abs(fftResult[:len(fftResult)/2]), 'r')
    plt.show()
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


    '''
    timeArray = numpy.arange(0, amp.shape[0], 1)
    timeArray = timeArray / sampFreq
    timeArray = timeArray * 1000
    '''

    # wholeFFT = numpy.fft.rfft(amp)
    # fftFreq = numpy.abs(numpy.fft.fftfreq(len(wholeFFT)))
    # wholeFFT = numpy.abs(wholeFFT[0:len(wholeFFT)/2])
    # fftFreq = fftFreq[:len(fftFreq)/2]
    # normalizeFactor = numpy.max(numpy.abs(wholeFFT))
    # print "Most prominent frequency has value " + str(normalizeFactor)
    #
    # numFreqs = 10;
    # freqsPerBox = len(wholeFFT)/numFreqs
    # #print "Number of frequencies:", numFreqs, "", "Total Frequencies:", len(wholeFFT)
    # objects = list()
    # framesPerKeyframe = 3
    # secsPerKeyframe = 3/24.
    # totalFrames = 24*amp.shape[0]/sampFreq
    # for i in range(numFreqs):
    #     objects.append(cmds.polyCube(n='VisBox')[0])
    #     #print "Keyframing object " + objects[i]
    #     cmds.xform(t=(2*i, 0, 0))
    #     beginFreq = 220*i
    #     endFreq = 220*(i+1)
    #     '''
    #     beginFreq = i*freqsPerBox/float(len(wholeFFT))
    #     endFreq = (i+1)*freqsPerBox/float(len(wholeFFT))
    #     '''
    #     #print "Frequencies " + str(beginFreq) + "-" + str(endFreq)
    #     print "===================="
    #     print "Keyframing Box " + objects[i] + " (Frequencies " + str(beginFreq) + " to " + str(endFreq) + ")"
    #     print "===================="
    #     for f in range(0, totalFrames, framesPerKeyframe):
    #         curSamp = f*amp.shape[0]/totalFrames
    #         endSamp = curSamp+(secsPerKeyframe*sampFreq)
    #         #print "Setting keyframe at frame: " + str(f)
    #         #print "Searching samples " + str(curSamp) + "-" + str(endSamp)
    #
    #         #fftPiece = numpy.fft.fft(amp[curSamp:endSamp])
    #         #fftPiece = numpy.abs(fftPiece[0:len(fftPiece)/2])/normalizeFactor
    #         #power = numpy.max(numpy.abs(fftPiece[beginFreq:endFreq]))/normalizeFactor
    #         power = getMax(amp[curSamp:endSamp], sampFreq, beginFreq, endFreq)/normalizeFactor
    #         print "Frame " + str(f) + " = " + str(power)
    #        # objects[i].scale(1, power*10, 1)
    #         #print "ScaleY is: " + str(abs(power))
    #         cmds.setKeyframe(objects[i], v=power, at='scaleY', t=f)
    #     print ""
    #         #if i==0:
    #            # plt.plot(fftPiece)
    #     # plt.show()
    #
    #
    #
    #
    #
    #     #fftPiece = numpy.fft.fft(amp[i*freqsPerBox:(i+1)*freqsPerBox])
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