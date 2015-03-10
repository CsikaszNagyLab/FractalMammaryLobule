from PyQt4.QtCore import Qt
import PyQt4.QtGui as qtgui


class EditableLabel(qtgui.QStackedWidget):
    def __init__(self, txt, is_valid=None, **kwargs):
        super(EditableLabel, self).__init__(**kwargs)
        self.setStyleSheet("margin:0px;spacing:0px;padding:0px")
        self.__label = qtgui.QLabel(txt)
        self.__label.setAlignment(Qt.AlignRight)
        self.__label.setStyleSheet("margin:0px;spacing:0px;padding:0px")
        self.__edit = qtgui.QLineEdit(txt)
        self.__edit.setAlignment(Qt.AlignRight)
        self.__edit.setStyleSheet(EditableLabel.valid_style)
        self.__edit.textChanged.connect(self.check)
        self.__edit.setStyleSheet("margin:0px;spacing:0px;padding:0px")
        self._textChanged = None
        self.addWidget(self.__label)
        self.addWidget(self.__edit)
        self.setCurrentIndex(0)
        self.isValid = is_valid

    valid_style = """QLineEdit { background-color: white;}"""
    invalid_style = """QLineEdit { background-color: red;}"""

    def text_changed(self, callback):
        self._textChanged = callback

    def check(self):
        style = EditableLabel.valid_style
        if self.isValid and not self.isValid(self.text()):
            style = EditableLabel.invalid_style
        elif self._textChanged:
            self._textChanged(self.text())
        self.__edit.setStyleSheet(style)

    def edit(self):
        if self.currentIndex() == 1:
            return
        self.__edit.setText(self.__label.text())
        self.setCurrentIndex(1)
        self.check()

    def fix(self):
        if self.currentIndex() == 0:
            return
        self.__label.setText(self.__edit.text())
        self.setCurrentIndex(0)

    def set_text(self, txt):
        self.currentWidget().setText(txt)

    def text(self):
        return self.currentWidget().text()
