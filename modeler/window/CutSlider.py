from PyQt4.QtCore import Qt
from PyQt4.QtGui import QSlider


class CutSlider(QSlider):
    def __init__(self):
        super(CutSlider, self).__init__(Qt.Vertical)
        self.setGeometry(10, 10, 200, 30)
        self.setFocusPolicy(Qt.NoFocus)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setTracking(False)
