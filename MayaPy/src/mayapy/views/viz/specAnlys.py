import sys
import colorsys
import time

import numpy
import scipy.io.wavfile as wav

from nimble import cmds
from mayapy.views.viz.Scene import BoxOnSphereScene
from mayapy.views.viz.Scene import BoxScene
from mayapy.views.viz.Box import Box
from mayapy.views.viz.Box import BoxOnSphere

def main(fn, scaleFactor, heightFactor):
    startTime = time.time()
    # set up audio for playback in Maya
    # audioNode = cmds.sound( offset=10, file=filename)
    # gPlayBackSlider = maya.mel.eval( '$tmpVar=$gPlayBackSlider' )
    # cmds.timeControl( gPlayBackS lider, edit=True, sound=audioNode )


    # read audio faile into raw data
    filename = '../../resources/' + fn + '.wav'
    print('FILENAME: ' + filename)

    print "Reading file " + filename + "..."
    rate,data=wav.read(filename)
    lastFrame = int(len(data)/float(rate) * 24)
    cmds.playbackOptions( min='1', max=str(lastFrame))

    print "Creating Scenes..."
    scaleFactor = float(scaleFactor)
    heightFactor = float(heightFactor)
    sphere = bouncingBubble(data.T[0], rate, scaleFactor)
    # scene = BoxScene(data.T[0], rate, 0, int(1e4), (-9, .5, 0))
    scene = BoxOnSphereScene(data.T[0], rate, 0, int(1e4), sphere)

    print "Animating Scenes..."
    scene.animate(scaleFactor, heightFactor)


    # normalize data from -1 to 1
    norms = data / (2.**15)
    print "Length of audio:"
    print str(norms.shape[0]/rate) + ' Seconds'

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
    fftResult = numpy.fft.fft(amp) # calculate fft
    fftFreq = numpy.abs(numpy.fft.fftfreq(len(fftResult))*sampRate)

    fftResult = fftResult[:len(fftResult)/2]
    fftFreq = fftFreq[:len(fftFreq)/2]
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

def bouncingBubble(amp, sampFreq, scaleFactor):
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
    # scaleFactor = 10.0
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

def normalize(data, index):
    """
    Normalizes the value data[index] as a float between 0.0 and 1.0
    :param data: list of data to use for normalization
    :param index: index in data we wish to normalize among the set
    :return: the normalized value, a float between 0.0 and 1.0
    """
    return float(data[index] - min(data))/(max(data) - min(data))

def clearScene():
    cmds.select(all=True)
    cmds.delete()

if __name__ == '__main__':
    main()