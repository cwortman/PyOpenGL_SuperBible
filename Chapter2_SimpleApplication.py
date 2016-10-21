"""
PyOpenGL OpenGL SuperBible Chapter 2 Simple Application

First application that simply opens a OpenGL window and sets the
background color to red.

Author: Chase Wortman
"""

import sys
import numpy as np
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from OpenGL.GL import *


class MainWidget(QOpenGLWidget):
    def __init__(self):
        # noinspection PyArgumentList
        super().__init__()
        # Set focus to window
        self.setFocusPolicy(Qt.StrongFocus)
        # Start timer for widget updates
        self.startTimer(0)

    def timerEvent(self, event):
        # Update widget at each timer event
        self.update()

    def minimumSizeHint(self):
        # Minimum size the window will allow
        return QSize(100, 100)

    def sizeHint(self):
        # Default size of the window
        return QSize(800, 800)

    def paintGL(self):
        # Define float array for background color
        red = np.array([1.0, 0.0, 0.0, 1.0], 'f')
        # Set background color
        glClearBufferfv(GL_COLOR, 0, red)


class MainWindow(QMainWindow):
    def __init__(self):
        # noinspection PyArgumentList
        super().__init__()
        # Set window title name
        self.setWindowTitle('OpenGL Window')
        # Create MainWidget object which is derived from QWidget
        self.main_widget = MainWidget()
        # Define MainWidget as the CentralWidget for the MainWindow
        self.setCentralWidget(self.main_widget)
        # Show the MainWindow
        self.show()

if __name__ == '__main__':
    # Start Qt Application
    app = QApplication(sys.argv)
    # Create MainWindow object which is derived from QMainWindow
    window = MainWindow()
    # Center the MainWindow on the screen
    window.move((app.desktop().screenGeometry().width() - window.width()) / 2,
                (app.desktop().screenGeometry().height() - window.height()) / 2)
    # Exit application when app execution is finished
    sys.exit(app.exec_())
