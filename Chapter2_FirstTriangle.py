"""
PyOpenGL OpenGL SuperBible Chapter 2 First Triangle

Draws a triangle to the screen using vertices defined in the shader.

Author: Chase Wortman
"""

import sys
import numpy as np
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from OpenGL.GL import shaders
from OpenGL.GL import *


class MainWidget(QOpenGLWidget):
    def __init__(self):
        # noinspection PyArgumentList
        super().__init__()
        # Set focus to window
        self.setFocusPolicy(Qt.StrongFocus)
        # Start timer for widget updates
        self.startTimer(0)
        # Initialise shader program
        self.program = None

    def timerEvent(self, event):
        # Update widget at each timer event
        self.update()

    def minimumSizeHint(self):
        # Minimum size the window will allow
        return QSize(100, 100)

    def sizeHint(self):
        # Default size of the window
        return QSize(800, 800)

    def initializeGL(self):
        # Define vertex shader
        vertex_shader = shaders.compileShader("""
        #version 440 core

        void main(void)
        {
            // Declare a hard-coded array of positions
            const vec4 vertices[3] = vec4[3](vec4(0.25, -0.25, 0.5, 1.0),
                                           vec4(-0.25, -0.25, 0.5, 1.0),
                                           vec4(0.25, 0.25, 0.5, 1.0));
            // Index into our array using gl_VertexID
            gl_Position = vertices[gl_VertexID];
        }
        """, GL_VERTEX_SHADER)
        # Define fragment shader
        fragment_shader = shaders.compileShader("""
        #version 440 core

        out vec4 color;

        void main(void)
        {
            color = vec4(0.0, 0.8, 1.0, 1.0);
        }
        """, GL_FRAGMENT_SHADER)
        # Compile shaders into program
        self.program = shaders.compileProgram(vertex_shader, fragment_shader)
        # Cleanup shaders since they aren't needed anymore
        shaders.glDeleteShader(vertex_shader)
        shaders.glDeleteShader(fragment_shader)

    def paintGL(self):
        # Define float array for background color
        bg_color = np.array([0.0, 0.2, 0.0, 1.0], 'f')
        # Set background color
        glClearBufferfv(GL_COLOR, 0, bg_color)
        # Use program for rendering
        glUseProgram(self.program)
        # Draw triangle from vertices in the vertex shader
        glDrawArrays(GL_TRIANGLES, 0, 3)


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
