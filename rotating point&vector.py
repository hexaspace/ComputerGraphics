# hexa computer graphics 06
# rotating point&vector
#################################################

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def render(M):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
# draw cooridnate / xy축 그리기
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)
# draw point p  / point p 그리기
    glBegin(GL_POINTS)
# 3rd element of point array is 1 / 점을 표현하는 마지막 배열요소는 1
    glVertex2fv((M @ np.array([.5, 0.,1.]))[:-1] )
    glEnd()
# draw vector v / 백터 v 그리기
    glBegin(GL_LINES)
# your implementation
    #3rd element of vector array is 0 / 백터을 표현하는 마지막 배열요소는 0
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv((M @ np.array([.5, 0.,0.]))[:-1] )
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, 'rotating point&vector', None,None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        t = glfw.get_time()
        #rotate t in ccw / 시간 t의 rad만큼 반시계 회전
        R = np.array([[np.cos(t), -np.sin(t), 0.],
                      [np.sin(t), np.cos(t), 0.],
                      [0., 0., 1.]])
        #translate 0.5 in x / x축 방향 0.5 이동
        T = np.array([[1.,0.,.5],
                     [0.,1.,0.],
                     [0.,0.,1.]])
        #first traslate and second rotate / 이동 후 회전 (l to r in local) 백터곱
        render(R@T)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()