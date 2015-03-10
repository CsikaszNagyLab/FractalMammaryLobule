from PyQt4 import QtCore
from PyQt4.QtCore import Qt
import PyQt4.QtGui as qtgui
from model import rad_to_grad, grad_to_rad
from EditableLabel import EditableLabel
from LabelValueArray import LabelValueArray


class Parameters(qtgui.QFrame):
    def __init__(self, **kwargs):
        super(Parameters, self).__init__(**kwargs)

        def is_valid_int(text):
            try:
                int(text)
            except:
                return False
            return True

        def is_valid_float(text):
            try:
                float(text)
            except:
                return False
            return True

        self.setStyleSheet("margin:8px;spacing:1px;padding:0px")

        ext_layout = qtgui.QHBoxLayout()

        leftframe = qtgui.QFrame(self)
        param_frame = qtgui.QFrame(leftframe)
        self.__branching_angles = LabelValueArray("Branching Angles",
                                                  is_valid_int,
                                                  parent=leftframe)
        self.__branching_angles.setMinimumWidth(180)
        self.setLayout(ext_layout)
        ext_layout.addWidget(leftframe, alignment=Qt.AlignTop)
        layout = qtgui.QFormLayout()

        param_frame.setStyleSheet("margin:0px;spacing:0px;padding:0px")
        param_frame.setLayout(layout)
        leftframelayout = qtgui.QVBoxLayout()
        leftframe.setStyleSheet("margin:0px;spacing:0px;padding:0px")
        leftframe.setLayout(leftframelayout)
        leftframelayout.addWidget(param_frame)
        param_frame.setStyleSheet("margin:0px;spacing:0px;padding:0px")

        def change_branching_angle_count(c):
            self.__branching_angles.set_count(int(c))

        self.__n_levels = EditableLabel("", is_valid_int, parent=param_frame)
        layout.addRow("# &levels", self.__n_levels)
        self.__n_levels.text_changed(change_branching_angle_count)

        self.__initial_length = EditableLabel("", is_valid_float,
                                              parent=param_frame)
        layout.addRow("initial length", self.__initial_length)

        self.__length_ratio = EditableLabel("", is_valid_float,
                                            parent=param_frame)
        layout.addRow("length ratio", self.__length_ratio)

        self.__initial_radius = EditableLabel("", is_valid_float,
                                              parent=param_frame)
        layout.addRow("initial radius", self.__initial_radius)

        self.__radius_ratio = EditableLabel("", is_valid_float,
                                            parent=param_frame)
        layout.addRow("radius ratio", self.__radius_ratio)

        self.__rotation_angle = EditableLabel("", is_valid_int,
                                              parent=param_frame)
        layout.addRow("rotation angle", self.__rotation_angle)

        self.__stem_inclination = EditableLabel("", is_valid_int,
                                                parent=param_frame)
        layout.addRow("stem inclination", self.__stem_inclination)

        self.__stem_rotation = EditableLabel("", is_valid_int,
                                             parent=param_frame)
        layout.addRow("stem rotation", self.__stem_rotation)

        self.__tree_rotation = EditableLabel("", is_valid_int,
                                             parent=param_frame)
        layout.addRow("tree rotation", self.__tree_rotation)

        ext_layout.addWidget(self.__branching_angles)

        leftframelayout.addSpacing(20)
        self.__stacked_buttons = qtgui.QStackedWidget(parent=leftframe)
        leftframelayout.addWidget(self.__stacked_buttons)

        button = qtgui.QPushButton("Change model")
        self.__stacked_buttons.addWidget(button)
        button.clicked.connect(self.__raise_change)

        buttons_frame = qtgui.QFrame(parent=self.__stacked_buttons)
        buttons_frame.setStyleSheet("margin:0px;spacing:1px;padding:0px")
        buttons_layout = qtgui.QHBoxLayout()
        buttons_frame.setLayout(buttons_layout)
        self.__stacked_buttons.addWidget(buttons_frame)

        button = qtgui.QPushButton("Confirm")
        buttons_layout.addWidget(button)
        button.clicked.connect(self.__raise_confirm)

        button = qtgui.QPushButton("Discard")
        buttons_layout.addWidget(button)
        button.clicked.connect(self.__raise_discard)

        cnframe = qtgui.QFrame(parent=leftframe)
        cnframelayout = qtgui.QFormLayout()
        cnframe.setLayout(cnframelayout)
        cnframelayout.setAlignment(Qt.AlignBottom)
        self.cut_numbers = qtgui.QLabel(parent=cnframe)
        cnframelayout.addRow("N. of cut ducts", self.cut_numbers)
        cnframe.setSizePolicy(qtgui.QSizePolicy.Maximum,
                              qtgui.QSizePolicy.Maximum)

        leftframelayout.addWidget(cnframe)

    def set_error(self, fieldname):
        getattr(self, "_parameters__" + fieldname).check()

    def edit(self):
        self.__n_levels.edit()
        self.__initial_length.edit()
        self.__length_ratio.edit()
        self.__initial_radius.edit()
        self.__radius_ratio.edit()
        self.__rotation_angle.edit()
        self.__stem_inclination.edit()
        self.__stem_rotation.edit()
        self.__tree_rotation.edit()
        self.__branching_angles.edit()

        self.__stacked_buttons.setCurrentIndex(1)

    def fix(self):
        self.__n_levels.fix()
        self.__initial_length.fix()
        self.__length_ratio.fix()
        self.__initial_radius.fix()
        self.__radius_ratio.fix()
        self.__rotation_angle.fix()
        self.__stem_inclination.fix()
        self.__stem_rotation.fix()
        self.__tree_rotation.fix()
        self.__branching_angles.fix()

        self.__stacked_buttons.setCurrentIndex(0)

    def __raise(self, signal):
        self.emit(QtCore.SIGNAL(signal))

    def __raise_change(self):
        self.__raise("changing()")

    def __raise_confirm(self):
        self.__raise("confirmed()")

    def __raise_discard(self):
        self.__raise("discarded()")

    def show_model(self, model):
        if model:
            self.__n_levels.set_text("%d" % model.n_levels)
            self.__initial_length.set_text("%.3g" % model.length)
            self.__length_ratio.set_text("%.3g" % model.length_ratio)
            self.__initial_radius.set_text("%.3g" % model.radius)
            self.__radius_ratio.set_text("%.3g" % model.radius_ratio)

            branching_angles = ["%d" % int(round(rad_to_grad(b)))
                                for b in model.beta[1::]]
            self.__branching_angles.set_values(branching_angles)

            incl_str = "%d" % int(round(rad_to_grad(model.beta[0])))
            self.__stem_inclination.set_text(incl_str)

            stem_rot_str = "%d" % int(round(rad_to_grad(model.stem_rotation)))
            self.__stem_rotation.set_text(stem_rot_str)

            tree_rot_str = "%d" % int(round(rad_to_grad(model.tree_rotation)))
            self.__tree_rotation.set_text(tree_rot_str)

            rot_angle_str = "%d" % int(round(rad_to_grad(model.alpha)))
            self.__rotation_angle.set_text(rot_angle_str)
        else:
            self.__n_levels.set_text("")
            self.__initial_length.set_text("")
            self.__length_ratio.set_text("")
            self.__initial_radius.set_text("")
            self.__radius_ratio.set_text("")
            self.__branching_angles.set_values([])
            self.__stem_inclination.set_text("")
            self.__stem_rotation.set_text("")
            self.__tree_rotation.set_text("")
            self.__rotation_angle.set_text("")

    n_levels = property(lambda self: int(self.__n_levels.text()))
    initial_length = property(lambda self: float(self.__initial_length.text()))
    length_ratio = property(lambda self: float(self.__length_ratio.text()))
    initial_radius = property(lambda self: float(self.__initial_radius.text()))
    radius_ratio = property(lambda self: float(self.__radius_ratio.text()))
    stem_inclination = property(lambda self: grad_to_rad(float(self.__stem_inclination.text())))
    stem_rotation = property(lambda self: grad_to_rad(float(self.__stem_rotation.text())))
    tree_rotation = property(lambda self: grad_to_rad(float(self.__tree_rotation.text())))
    branching_angles = property(lambda self: [
        grad_to_rad(float(x)) for x in self.__branching_angles.values])
    rotation_angle = property(lambda self: grad_to_rad(float(self.__rotation_angle.text())))
