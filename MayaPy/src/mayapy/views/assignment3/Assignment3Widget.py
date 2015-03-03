# Assignment3Widget.py

import bubbles
from pyglass.widgets.PyGlassWidget import PyGlassWidget

#___________________________________________________________________________________________________ Assignment2Widget
class Assignment3Widget(PyGlassWidget):
    """A class for..."""
#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of Assignment2Widget."""
        super(Assignment3Widget, self).__init__(parent, **kwargs)
        self.bubbleQuantity = 50

        self.homeBtn.clicked.connect(self._handleReturnHome)
        self.bubbles.clicked.connect(self._handleBubbles)

        self.numBubs.activated[str].connect(self._handleActivated)


#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleReturnHome
    def _handleReturnHome(self):
        self.mainWindow.setActiveWidget('home')

    def _handleBubbles(self):
        bubbles.main(self.bubbleQuantity, True)

    def _handleActivated(self, text):
        self.bubbleQuantity = int(text)