# Assignment4Widget.py

import shape, material
from nimble import cmds
from pyglass.widgets.PyGlassWidget import PyGlassWidget

#___________________________________________________________________________________________________ Assignment2Widget
class Assignment4Widget(PyGlassWidget):
    """A class for..."""
#===================================================================================================
#                                                                                       C L A S S
    barIndex = 1
    sphereIndex = 1
    ringIndex = 1
    recentCreation = '',0
#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of Assignment2Widget."""
        super(Assignment4Widget, self).__init__(parent, **kwargs)

        self.sceneBtn.clicked.connect(self._handleScene)
        self.homeBtn.clicked.connect(self._handleReturnHome)

        self.barBtn.clicked.connect(self._handleBar)
        self.sphereBtn.clicked.connect(self._handleSphere)
        self.ringBtn.clicked.connect(self._handleRing)

        self.goldBtn.clicked.connect(self._handleGold)
        self.plasticBtn.clicked.connect(self._handlePlastic)

    def createLight(self, name, translate, rotate):
        cmds.spotLight(n = name)
        cmds.xform(name, t=[translate[0],translate[1],translate[2]])
        cmds.rotate(rotate[0], rotate[1], rotate[2], name)
        cmds.setAttr(self.getShapeString(name) + '.intensity', 1.5)
        cmds.setAttr(self.getShapeString(name) + '.penumbraAngle', 5.)

    def getShapeString(self, name):
        return name[:-1] + 'Shape' + name[-1:]
#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleReturnHome
    def _handleReturnHome(self):
        self.mainWindow.setActiveWidget('home')

    def _handleScene(self):
        cmds.polyPlane(w=25,h=25)
        self.createLight('spotlight1', [3.5, 6, 3.5], [-120, -180, -45])
        self.createLight('spotlight2', [-3.5, 6, 3.5], [-120, -180, 45])
        self.createLight('spotlight3', [3.5, 6, -3.5], [-120, 0, -45])
        self.createLight('spotlight4', [-3.5, 6, -3.5], [-120, 0, 45])

    ## SHAPES
    def _handleBar(self):
        self.recentCreation = 'bar', self.barIndex
        shape.main(self.recentCreation[0], self.recentCreation[1])
        self.barIndex += 1

    def _handleSphere(self):
        self.recentCreation = 'sphere', self.sphereIndex
        shape.main(self.recentCreation[0], self.recentCreation[1])
        self.sphereIndex += 1

    def _handleRing(self):
        self.recentCreation = 'ring', self.ringIndex
        shape.main(self.recentCreation[0], self.recentCreation[1])
        self.ringIndex += 1

    ## MATERIALS
    def _handleGold(self):
        material.main(self.recentCreation[0] + str(self.recentCreation[1]), 'gold')

    def _handlePlastic(self):
        material.main(self.recentCreation[0] + str(self.recentCreation[1]), 'plastic')