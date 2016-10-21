"""
PyOpenGL OpenGL SuperBible Chapter 3 Passing Data

Passing data between shaders to draw a moving triangle on a color
changing background with movement and color defined outside of the shaders.

Author: Chase Wortman
"""

import sys
import time
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
        # Start time for use with calculations later
        self.start_time = time.time()
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

        // 'offset' and 'color' are input vertex attributes
        layout (location = 0) in vec4 offset;
        layout (location = 1) in vec4 color;

        // 'vs_color' is an output that will be sent to the next stage
        out vec4 vs_color;

        void main(void)
        {
            const vec4 vertices[3] = vec4[3](vec4(0.25, -0.25, 0.5, 1.0),
                                         vec4(-0.25, -0.25, 0.5, 1.0),
                                         vec4(0.25, 0.25, 0.5, 1.0));

            // Add 'offset' to our hard-coded vertex position
            gl_Position = vertices[gl_VertexID] + offset;

            // Output a fixed value for vs_color
            vs_color = color;
        }
        """, GL_VERTEX_SHADER)
        # Define fragment shader
        fragment_shader = shaders.compileShader("""
        #version 440 core

        // Input from the vertex shader
        in vec4 vs_color;

        // Output to the framebuffer
        out vec4 color;

        void main(void)
        {
            // Simply assign the color we were given by the vertex shader to our output
            color = vs_color;
        }
        """, GL_FRAGMENT_SHADER)
        # Compile shaders into program
        self.program = shaders.compileProgram(vertex_shader, fragment_shader)
        # Cleanup shaders since they aren't needed anymore
        shaders.glDeleteShader(vertex_shader)
        shaders.glDeleteShader(fragment_shader)

    def paintGL(self):
        # Get time in seconds since start
        time_now = time.time() - self.start_time
        # Define float arrays for background color, offset, and triangle color
        bg_color = np.array([np.sin(time_now) * 0.5 + 0.5, np.cos(time_now) * 0.5 + 0.5, 0.0, 1.0], 'f')
        offset = np.array([np.sin(time_now) * 0.5, np.cos(time_now) * 0.6, 0.0, 0.0], 'f')
        color = np.array([0.0, 0.0, 0.0, 0.0], 'f')
        # Set background color
        glClearBufferfv(GL_COLOR, 0, bg_color)
        # Use program for rendering
        glUseProgram(self.program)
        # Pass arrays to shader attributes
        glVertexAttrib4fv(0, offset)
        glVertexAttrib4fv(1, color)
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
