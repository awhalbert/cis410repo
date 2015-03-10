from nimble import cmds

class Box:

    FRAME_STEP = 3

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
        cmds.xform(t=(self.posX, self.posY, self.posZ))
        for i in range(len(self.heights)):
            cmds.setKeyframe(self.name, v=self.heights[i], at='scaleY', t=i*Box.FRAME_STEP)

    def getNumberOfFrames(self):
        return self.numFrames/Box.FRAME_STEP