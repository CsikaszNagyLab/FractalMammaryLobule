from PyQt4.QtCore import Qt
import PyQt4.QtGui as qtgui
from EditableLabel import EditableLabel


class LabelValueArray(qtgui.QGroupBox):
    def __init__(self, label_string, is_valid=None, **kwargs):
        super(LabelValueArray, self).__init__(label_string, **kwargs)
        self.elements = []
        self.labels = {}
        extlayout = qtgui.QVBoxLayout()
        scroll = qtgui.QScrollArea(parent=self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("margin:0px;spacing:0px;padding:0px")
        extlayout.addWidget(scroll)
        inframe = qtgui.QFrame(parent=scroll)
        inframe.setFrameStyle(0)
        scroll.setFrameStyle(0)
        inframe.setStyleSheet("margin:0px;spacing:0px;padding:0px")
        scroll.setWidget(inframe)

        self.layout = qtgui.QFormLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setStyleSheet("margin:6px;spacing:0px;padding:6px")
        self.setLayout(extlayout)
        inframe.setLayout(self.layout)
        self.set_values([])
        self.label_string = label_string
        self.isValid = is_valid
        self.is_editing = False

    def edit(self):
        self.is_editing = True
        for e in self.elements:
            if not e.isHidden():
                e.edit()

    def fix(self):
        self.is_editing = False
        for e in self.elements:
            if not e.isHidden():
                e.fix()

    def check(self):
        for e in self.elements:
            e.check()

    def set_count(self, c):
        prev_c = len(self.elements)
        v = self.values
        if prev_c > c:
            self.set_values(v[:c])
        elif prev_c < c:
            self.set_values(v + v[-1::] * (c - prev_c))

    def _create_element(self, value, i):
        el = EditableLabel("", self.isValid, parent=self)
        el.set_text(value)
        l = qtgui.QLabel("level #%d:" % i)
        self.layout.addRow(l, el)
        self.labels[el] = l
        if self.is_editing:
            el.edit()
        return el

    def _remove_element(self, element):
        element.setParent(None)
        label = self.labels.pop(element)
        if label is not None:
            label.deleteLater()
        element.deleteLater()
        # self.layout.removeWidget(element)

    def set_values(self, values):

        for e, v in zip(self.elements, values):
            e.set_text(v)

        for e in self.elements[len(values):]:
            self._remove_element(e)

        self.elements = self.elements[:len(values)]

        self.elements += [
            self._create_element(values[i], i)
            for i in range(len(self.elements), len(values))]

    values = property(lambda self: [e.text() for e in self.elements])
