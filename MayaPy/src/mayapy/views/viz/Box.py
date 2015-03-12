from nimble import cmds
from math import cos, sin, radians, pi

class Box(object):
    """
    Author: Elliott Ewing
    """
    FRAME_STEP = 3 # how fine is our sampling? lower is finer
    AVG_WIN = 3 # but then how often do we actually keyframe? the larger this number the fewer keyed frames

    def __init__(self, numFrames):
        self.heights = [1 for x in range(numFrames/Box.FRAME_STEP)]
        self.posX = self.posY = self.posZ = 0
        self.numFrames = numFrames
        self.name = "unnamed"

    def getHeight(self, frame):
        return self.heights[frame]

    def setHeight(self, height, frame):
        self.heights[frame] = height

    def setPosition(self, x, y, z):
        self.posX = x
        self.posY = y
        self.posZ = z

    def render(self):
        if(self.name == "unnamed"):
            self.name = cmds.polyCube(n='VisBox')[0]
            cmds.xform(sp=[self.posX, -.5, self.posZ])
        cmds.xform(t=[self.posX, self.posY, self.posZ])
        for i in range(0, len(self.heights), Box.AVG_WIN):
            cmds.setKeyframe(self.name, v=self.avg([x for x in self.heights[i:i+Box.AVG_WIN]]), at='scaleY', t=i)

    def getNumberOfFrames(self):
        return self.numFrames/Box.FRAME_STEP

    def avg(self, listOfNumbers):
        accum = 0.
        for x in listOfNumbers:
            accum += x
        return accum/Box.AVG_WIN

class BoxOnSphere(Box):
    """
    Author: Aaron Halbert
    """
    SPHERE_STEP = 3

    def __init__(self, numFrames, sphere, index, numBoxes):
        super(BoxOnSphere, self).__init__(numFrames)
        self.sphere = sphere
        self.index = index
        self.numBoxes = numBoxes
        self.positions = [(0,0) for x in range(numFrames/BoxOnSphere.SPHERE_STEP)]
        self.widths = [(0,0) for x in range(numFrames/BoxOnSphere.SPHERE_STEP)]
        self.theta = (360/self.numBoxes) * self.index - 90
    def calculatePositions(self, frame, radii):
        r = (radii[frame] + .5)*.96 # we add .5 so the bottom of a box aligns with the surface of the sphere, not the middle of a box's original height
        # print('radius: ' + str(r) + ', frame: ' + str(frame))
        self.positions[frame] = (r * cos(radians(self.theta + 90)), r * sin(radians(self.theta + 90)))
        self.widths[frame] = ( 2 * pi * r ) / self.numBoxes
    def angleOnUnitCircle(self, theta):
        return (theta - 270)
    def getNumberOfFrames(self):
        return self.numFrames/BoxOnSphere.SPHERE_STEP
    def render(self):
        if(self.name == "unnamed"):
            self.name = cmds.polyCube(n='visBox')[0]
            cmds.xform(sp=[self.posX, -.5, self.posZ], ro=[0,0,self.theta])

        # this code will average the heights of a finer sampling into a coarser keyframing

        # for i in range(0, len(self.heights), BoxOnSphere.SPHERE_STEP): # i steps by SPHERE_STEP
        #     cmds.setKeyframe(self.name, v=self.avg([x for x in self.heights[i:i+BoxOnSphere.SPHERE_STEP]]), at='scaleY', t=i)
        #     # x[0] for x in self.positions[i:i+BoxOnSphere.SPHERE_STEP]
        #
        # for i in range(len(self.widths)):
        #     cmds.setKeyframe(self.name, v=self.positions[i][0], at='translateX', t=i*BoxOnSphere.SPHERE_STEP)
        #     cmds.setKeyframe(self.name, v=self.positions[i][1], at='translateY', t=i*BoxOnSphere.SPHERE_STEP)
        #     cmds.setKeyframe(self.name, v=self.widths[i], at='scaleX', t=i*BoxOnSphere.SPHERE_STEP)
        #     cmds.setKeyframe(self.name, v=self.widths[i], at='scaleZ', t=i*BoxOnSphere.SPHERE_STEP)


        # this code does no averaging -- the heights are sampled every 3 frame lengths
        for i in range(len(self.heights)):
            cmds.setKeyframe(self.name, v=self.heights[i], at='scaleY', t=i*BoxOnSphere.SPHERE_STEP)
            cmds.setKeyframe(self.name, v=self.positions[i][0], at='translateX', t=i*BoxOnSphere.SPHERE_STEP)
            cmds.setKeyframe(self.name, v=self.positions[i][1], at='translateY', t=i*BoxOnSphere.SPHERE_STEP)
            cmds.setKeyframe(self.name, v=self.widths[i], at='scaleX', t=i*BoxOnSphere.SPHERE_STEP)
            cmds.setKeyframe(self.name, v=self.widths[i], at='scaleZ', t=i*BoxOnSphere.SPHERE_STEP)