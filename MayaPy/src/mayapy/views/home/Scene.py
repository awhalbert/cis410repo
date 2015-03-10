import numpy
import pylab as plt
from mayapy.views.home.Box import Box
from mayapy.views.home.Drop import Drop

class Scene(object):
    def __init__(self, waveform, sampleRate, freqMin, freqMax):
        '''
        :param waveform: The numpy array associated with the pressure waves in the music
        :param sampleRate: The sampling rate of the given waveform
        :param freqMin: The minimum frequency to represent in the scene
        :param freqMax: The maximum frequency to represent in the scene
        :return: N/A
        '''

        ### Initialize parameter values
        self.waveform = waveform
        self.sampleRate = sampleRate
        self.freqMin = freqMin
        self.freqMax = freqMax
        self.octavePerBox = .25

        # Initialize Calculated variables
        self.length = waveform.shape[0]
        self.numFrames = 24 * self.length/self.sampleRate
        self.numOctaves = 0
        curFreq = self.freqMax
        while curFreq > 32:
            pass
        #self.numObjects =

    def calculatePower(self, frame, frameStep, freqIndex):
        freqResolution = 2**5 * 2**(freqIndex/2.)
        numSamples = self.sampleRate/freqResolution # Calculate number of samples needed for freqResolution Hz per index
        samplesPerKeyframe = frameStep*self.sampleRate/24 # Calculate how many samples to step by between keyframes
        fftResult = numpy.fft.rfft(self.waveform[samplesPerKeyframe*frame:(samplesPerKeyframe*frame)+numSamples]) # Calculate fft (only real values) returns complex array
        print len(fftResult), freqResolution, freqIndex
        if(freqIndex == 0):
            return numpy.abs(fftResult[0])*1
        else:
            return numpy.abs(fftResult[1])*1
        #return 0#numpy.abs(fftResult[freqIndex]) # Return real interpretation of complex number at freqIndex (frequency slot requested)


class BoxScene(Scene):

    def __init__(self, waveform, sampleRate, freqMin, freqMax, (locX, locY, locZ)):
        super(self.__class__, self).__init__(waveform, sampleRate, freqMin, freqMax)

        ### Initialize default values
        self.numBoxes = 19

        ### Initialize calculatable values
        self.freqStep = (self.freqMax-self.freqMin)/self.numBoxes
        self.boxes = [Box(self.numFrames) for x in range(self.numBoxes)]
        for i in range(self.numBoxes):
            self.boxes[i].setPosition(i + locX, locY, locZ)

    def animate(self):

        samplesPerKeyframe = Box.FRAME_STEP*self.sampleRate/24
        timeStep = Box.FRAME_STEP*24

        #print numpy.max(self.fftFreq)
        for boxNum in range(len(self.boxes)):
            #heights = list()
            print "Calculating object ", boxNum
            for frame in range(self.boxes[boxNum].getNumberOfFrames()):
                height = self.calculatePower(frame, Box.FRAME_STEP, boxNum)
                self.boxes[boxNum].setHeight(height, frame)

        print "Calculating norms..."
        norm = 0
        for box in self.boxes:
            for frame in range(box.getNumberOfFrames()):
                norm = max(norm, box.getHeight(frame))

        for box in self.boxes:
            for frame in range(box.getNumberOfFrames()):
                box.setHeight(box.getHeight(frame)*10/norm, frame)

        for box in self.boxes:
            for frame in range(1, box.getNumberOfFrames()):
                box.setHeight(max(box.getHeight(frame), box.getHeight(frame-1)-.5), frame)

        for box in range(len(self.boxes)):
            print "Keyframing object ", box
            self.boxes[box].render()

class DropScene(Scene):

    def __init__(self, waveform, sampleRate, freqMin, freqMax, (locX, locY, locZ)):
        super(self.__class__, self).__init__(waveform, sampleRate, freqMin, freqMax)

        ### Initialize default values
        self.numDrops = self.numFrames/Drop.FRAME_STEP
        self.frameStep = 3

        ### Initialize calculatable values
        self.freqStep = (self.freqMax-self.freqMin)/self.numDrops
        self.drops = [Drop(self.numFrames) for x in range(self.numDrops)]
        for i in range(self.numDrops):
            self.drops[i].setPosition(i + locX, locY, locZ)

    def animate(self):

        samplesPerKeyframe = Drop.FRAME_STEP*self.sampleRate/24
        timeStep = Drop.FRAME_STEP*24

        for frame in range(self.numDrops):
            print frame
            self.drops[frame].frameHit = frame
            self.drops[frame].offset = self.getIndexOfMax(frame, 80)
        '''
        #print numpy.max(self.fftFreq)
        for boxNum in range(len(self.boxes)):
            #heights = list()
            print "Calculating object ", boxNum
            for frame in range(self.boxes[boxNum].getNumberOfFrames()):
                height = self.calculatePower(frame, Box.FRAME_STEP, boxNum, 80)
                self.boxes[boxNum].setHeight(height, frame)

        print "Calculating norms..."
        norm = 0
        for box in self.boxes:
            for frame in range(box.getNumberOfFrames()):
                norm = max(norm, box.getHeight(frame))

        for box in self.boxes:
            for frame in range(box.getNumberOfFrames()):
                box.setHeight(box.getHeight(frame)*10/norm, frame)
        '''
        for drop in range(len(self.drops)):
            print "Keyframing object ", drop
            self.drops[drop].render()

    def getIndexOfMax(self, frame, resolution):
        numSamples = self.sampleRate/resolution # Calculate number of samples needed for freqResolution Hz per index
        samplesPerKeyframe = Drop.FRAME_STEP*self.sampleRate/24 # Calculate how many samples to step by between keyframes
        fftResult = numpy.fft.rfft(self.waveform[samplesPerKeyframe*frame:(samplesPerKeyframe*frame)+numSamples]) # Calculate fft (only real values) returns complex array
        return numpy.argmax(numpy.abs(fftResult))

