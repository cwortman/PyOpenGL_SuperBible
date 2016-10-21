"""
PyOpenGL OpenGL SuperBible Chapter 3 Tessellation

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
        #version 440

        // 'offset' and 'color' are input vertex attributes
        layout(location = 0) in vec4 offset;
        layout(location = 1) in vec4 color;

        // 'vs_color' is an output that will be sent to the tessellation control shader
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

        # Define tessellation control shader
        tess_control_shader = shaders.compileShader("""
        #version 440

        layout(vertices = 3) out;

        // Input from vertex shader in array form
        in vec4 vs_color[];

        // Output to the tessellation evaluation shader in patch form
        patch out vec4 vc_color;

        void main(void)
        {
            // Only if I am invocation 0...
            if (gl_InvocationID == 0)
            {
                gl_TessLevelInner[0] = 5.0;
                gl_TessLevelOuter[0] = 5.0;
                gl_TessLevelOuter[1] = 5.0;
                gl_TessLevelOuter[2] = 5.0;
            }

            // Everybody copies their input to their output
            gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;

            // Pass color from vertex shader to tessellation evaluation shader
            vc_color = vs_color[gl_InvocationID];
        }
        """, GL_TESS_CONTROL_SHADER)

        # Define tessellation evaluation shader
        tess_eval_shader = shaders.compileShader("""
        #version 440

        layout(triangles, equal_spacing, cw) in;

        // Input from tessellation control shader in patch form
        patch in vec4 vc_color;

        // Output to fragment shader
        out vec4 ve_color;

        void main(void)
        {
            gl_Position = (gl_TessCoord.x * gl_in[0].gl_Position +
                           gl_TessCoord.y * gl_in[1].gl_Position +
                           gl_TessCoord.z * gl_in[2].gl_Position);

            // Pass color from tessellation control shader to fragment shader
            ve_color = vc_color;
        }
        """, GL_TESS_EVALUATION_SHADER)

        # Define fragment shader
        fragment_shader = shaders.compileShader("""
        #version 440

        // Input from tessellation evaluation shader
        in vec4 ve_color;

        // Output to the framebuffer
        out vec4 color;

        void main(void)
        {
            // Simply assign the color we were given by the tessellation evaluation shader to our output
            color = ve_color;
        }
        """, GL_FRAGMENT_SHADER)

        # Compile shaders into program
        self.program = shaders.compileProgram(vertex_shader, tess_control_shader, tess_eval_shader, fragment_shader)

        # Cleanup shaders since they aren't needed anymore
        shaders.glDeleteShader(vertex_shader)
        shaders.glDeleteShader(tess_control_shader)
        shaders.glDeleteShader(tess_eval_shader)
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

        # Draw patches from vertices in the vertex shader
        glDrawArrays(GL_PATCHES, 0, 3)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


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
