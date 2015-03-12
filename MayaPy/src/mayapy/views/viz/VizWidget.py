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
        self.song = self.songBox.currentText()
        self.songBox.activated[str].connect(self._handleActivated)
        self.genBtn.clicked.connect(self._handleGen)


#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleReturnHome

    def _handleActivated(self, text):
        self.song = text

    def _handleGen(self):
        specAnlys.main(self.song)
