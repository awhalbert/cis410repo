__author__ = 'aaronhalbert'
# VizWidget.py

from pyglass.widgets.PyGlassWidget import PyGlassWidget
from mayapy.views.viz import specAnlys

#___________________________________________________________________________________________________ Assignment2Widget
class VizWidget(PyGlassWidget):
    """A class for..."""
    #===================================================================================================
    #                                                                                       C L A S S

    #___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of Assignment2Widget."""
        super(VizWidget, self).__init__(parent, **kwargs)
        self.file = 'Sober'
        self.sfBox.setCurrentIndex(3)
        self.hfBox.setCurrentIndex(4)

        self.scaleFactor = float(str(self.sfBox.currentText()))
        print(self.scaleFactor)
        self.heightFactor = float(str(self.hfBox.currentText()[:2]))
        print(self.heightFactor)

        self.homeBtn.clicked.connect(self._handleReturnHome)
        self.genBtn.clicked.connect(self._handleGen)
        self.clearBtn.clicked.connect(self._handleClear)

        self.songBox.activated[str].connect(self._handleSong)
        self.sfBox.activated[str].connect(self._handleSF)
        self.hfBox.activated[str].connect(self._handleHF)


    #===================================================================================================
    #                                                                                 H A N D L E R S

    #___________________________________________________________________________________________________ _handleReturnHome
    def _handleReturnHome(self):
        self.mainWindow.setActiveWidget('home')

    def _handleSong(self, text):
        self.file = text

    def _handleGen(self):
        specAnlys.main(self.file, self.scaleFactor, self.heightFactor)

    def _handleSF(self, text):
        self.scaleFactor = float(text)
        print('new scalefactor: ' + str(self.scaleFactor))

    def _handleHF(self, text):
        self.heightFactor = float(text[:-2])
        print('new height factor: ' + str(self.heightFactor))

    def _handleClear(self):
        specAnlys.clearScene()