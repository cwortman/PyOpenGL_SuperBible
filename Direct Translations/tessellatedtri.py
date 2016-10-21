"""
PyOpenGL OpenGL SuperBible Chapter 3 Tessellation

Tessellation control and tessellation evaulation shaders
that pass variables through from vertex shader to fragment shader
to draw a moving tessellated triangle on a color changing background.

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
        vs_source = """
        #version 440

        void main(void)
        {
            const vec4 vertices[] = vec4[](vec4(0.25, -0.25, 0.5, 1.0),
                                           vec4(-0.25, -0.25, 0.5, 1.0),
                                           vec4(0.25, 0.25, 0.5, 1.0));

            gl_Position = vertices[gl_VertexID];
        }
        """

        # Define tessellation control shader
        tcs_source = """
        #version 440

        layout(vertices = 3) out;

        void main(void)
        {
            if (gl_InvocationID == 0)
            {
                gl_TessLevelInner[0] = 5.0;
                gl_TessLevelOuter[0] = 5.0;
                gl_TessLevelOuter[1] = 5.0;
                gl_TessLevelOuter[2] = 5.0;
            }
            gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
        }
        """

        # Define tessellation evaluation shader
        tes_source = """
        #version 440

        layout(triangles, equal_spacing, cw) in;

        void main(void)
        {
            gl_Position = (gl_TessCoord.x * gl_in[0].gl_Position +
                           gl_TessCoord.y * gl_in[1].gl_Position +
                           gl_TessCoord.z * gl_in[2].gl_Position);
        }
        """

        # Define fragment shader
        fs_source = """
        #version 440

        out vec4 color;

        void main(void)
        {
            color = vec4(0.0, 0.8, 1.0, 1.0);
        }
        """

        self.program = glCreateProgram()
        vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vs, vs_source)
        glCompileShader(vs)

        tcs = glCreateShader(GL_TESS_CONTROL_SHADER)
        glShaderSource(tcs, tcs_source)
        glCompileShader(tcs)

        tes = glCreateShader(GL_TESS_EVALUATION_SHADER)
        glShaderSource(tes, tes_source)
        glCompileShader(tes)

        fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fs, fs_source)
        glCompileShader(fs)

        glAttachShader(self.program, vs)
        glAttachShader(self.program, tcs)
        glAttachShader(self.program, tes)
        glAttachShader(self.program, fs)

        glLinkProgram(self.program)

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def paintGL(self):
        green = np.array([0.0, 0.25, 0.0, 1.0], 'f')
        glClearBufferfv(GL_COLOR, 0, green)

        glUseProgram(self.program)
        glDrawArrays(GL_PATCHES, 0, 3)


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
