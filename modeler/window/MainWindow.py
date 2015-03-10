from PyQt4.QtCore import Qt
import PyQt4.QtGui as qtgui

from CutSlider import CutSlider
from Parameters import Parameters
from view.ModelView import ModelView


class MainWindow(qtgui.QMainWindow):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        top_frame = qtgui.QFrame()
        top_layout = qtgui.QHBoxLayout()
        self.setCentralWidget(top_frame)
        top_frame.setLayout(top_layout)
        self.parameters = Parameters()
        self.parameters.setFrameStyle(2)
        self.parameters.setFixedWidth(500)
        self.parameters.setMinimumHeight(700)

        render_frame = qtgui.QFrame()
        top_layout.addWidget(render_frame)
        top_layout.addWidget(self.parameters, alignment=Qt.AlignTop)
        self.parameters.setSizePolicy(qtgui.QSizePolicy.Minimum,
                                      qtgui.QSizePolicy.Maximum)

        render_layout = qtgui.QHBoxLayout()

        self.model_view = ModelView(parent=render_frame)
        render_layout.addWidget(self.model_view)
        self.slider = CutSlider()

        render_frame.setLayout(render_layout)
        render_layout.addWidget(self.slider)

        self.model_view.GetRenderWindow().Render()
