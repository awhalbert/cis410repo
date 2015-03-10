from nimble import cmds

class Drop:

    FRAME_STEP = 8

    def __init__(self, numFrames):
        self.frameHit = 0
        self.size = 1
        self.offset = 0
        self.posX = self.posY = self.posZ = 0
        self.numFrames = numFrames
        self.name = "unnamed"

    def setPosition(self, x, y, z):
        self.posX = x
        self.posY = y
        self.posZ = z

    def render(self):
        if(self.name == "unnamed"):
            self.name = cmds.polyCube(n='VisDrop')[0]

        frameStart = max(0, self.frameHit-3)
        cmds.xform(t=(self.offset, self.posY+10, self.posZ))
        cmds.setKeyframe(self.name, v=self.posY+10, at='translateY', t=frameStart*Drop.FRAME_STEP)
        cmds.setKeyframe(self.name, v=self.posY, at='translateY', t=self.frameHit*Drop.FRAME_STEP)

    def getNumberOfFrames(self):
        return self.numFrames/Drop.FRAME_STEP