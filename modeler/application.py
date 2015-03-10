from PyQt4 import QtCore as QtCore
from PyQt4.QtGui import QApplication
from control import ModelControl
from model import DuctModel
from window import MainWindow

__author__ = 'tommaso'


class Application(QApplication):
    def __init__(self, argv, x, y):
        super(Application, self).__init__(argv)
        self.__model_control = None

        self.window = MainWindow()
        self.window.resize(x, y)
        self.window.model_view.GetRenderWindow().SetSize(x, y)
        self.window.model_view.setup()
        self.window.model_view.register()
        self.window.slider.setEnabled(False)
        self.window.model_view.setEnabled(False)
        QtCore.QObject.connect(self.window.parameters,
                               QtCore.SIGNAL('changing()'),
                               self.__edit_parameters)
        QtCore.QObject.connect(self.window.parameters,
                               QtCore.SIGNAL('confirmed()'),
                               self.__confirm_parameters)
        QtCore.QObject.connect(self.window.parameters,
                               QtCore.SIGNAL('discarded()'),
                               self.__discard_parameters)

    def __edit_parameters(self):
        self.window.parameters.edit()

    def __get_parameter(self, field):
        try:
            return getattr(self.window.parameters, field)
        except:
            self.window.parameters.set_error(field)
            return None

    def __get_parameter_list(self):
        ret = [self.__get_parameter("rotation_angle"),
               self.__get_parameter("branching_angles"),
               self.__get_parameter("initial_length"),
               self.__get_parameter("length_ratio"),
               self.__get_parameter("initial_radius"),
               self.__get_parameter("radius_ratio"),
               self.__get_parameter("n_levels"),
               self.__get_parameter("stem_inclination"),
               self.__get_parameter("stem_rotation"),
               self.__get_parameter("tree_rotation")]
        if any(r is None for r in ret):
            return None
        return ret

    def __confirm_parameters(self):
        args = self.__get_parameter_list()

        if args:
            model = DuctModel(*args)
            self.set_model(model)
            self.window.parameters.fix()

    def __discard_parameters(self):
        self.window.parameters.fix()
        model = self.__model_control.model if self.__model_control else None
        self.window.parameters.show_model(model)

    def exec_(self):
        self.window.show()
        super(Application, self).exec_()

    def reset_model(self):
        if self.__model_control:
            self.__model_control.disconnect()
            self.__model_control = None

    def set_model(self, model):
        self.reset_model()
        self.__model_control = ModelControl(self.window, model)
        self.window.parameters.show_model(model)
        self.window.model_view.GetRenderWindow().Render()
