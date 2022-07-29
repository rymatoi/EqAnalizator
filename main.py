import sys
from PySide2 import QtCore, QtGui, QtWidgets

from PySide2.QtWidgets import QMenu, QMenuBar, QTabWidget, QAction, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, \
    QLineEdit, QPushButton, QMessageBox

from process_word import process_word


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.vlayout = QVBoxLayout()

        self.hlayout_1 = QHBoxLayout()
        self.label_in = QLabel("Входной файл:")
        self.line_edit_in = QLineEdit()
        self.choose_in = QPushButton("Выбрать..", clicked=self.open_in)
        self.hlayout_1.addWidget(self.label_in)
        self.hlayout_1.addWidget(self.line_edit_in)
        self.hlayout_1.addWidget(self.choose_in)

        self.hlayout_2 = QHBoxLayout()
        self.label_out = QLabel("Выходной файл:")
        self.line_edit_out = QLineEdit()
        self.choose_out = QPushButton("Выбрать..", clicked=self.open_out)
        self.hlayout_2.addWidget(self.label_out)
        self.hlayout_2.addWidget(self.line_edit_out)
        self.hlayout_2.addWidget(self.choose_out)

        self.hlayout_3 = QHBoxLayout()
        self.convert_button = QPushButton("Преобразовать формулы", clicked=self.convert)
        self.close_button = QPushButton("Закрыть", clicked=self.close)
        self.hlayout_3.addWidget(self.convert_button)
        self.hlayout_3.addWidget(self.close_button)

        self.vlayout.addLayout(self.hlayout_1)
        self.vlayout.addLayout(self.hlayout_2)
        self.vlayout.addLayout(self.hlayout_3)

        self.setLayout(self.vlayout)

        self.showNormal()

    def open_in(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open file', None, "WORD (*.docx)")
        if path:
            self.line_edit_in.setText(path)

    def open_out(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Open file', None, "WORD (*.docx)")
        if path:
            self.line_edit_out.setText(path)

    def convert(self):
        if self.line_edit_in.text() and self.line_edit_out.text():
            try:
                process_word(self.line_edit_in.text(), self.line_edit_out.text())
                self.dialog_successful('Преобразование прошло успешно!')

            except Exception as e:
                self.dialog_critical(str(e))

    def dialog_successful(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Information)
        dlg.show()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
