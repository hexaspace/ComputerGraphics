# hexa computer graphics 05
# triangle movement(keyboard QEAD1)
#################################################

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

#global variable - list of input keys / 전역변수-인풋값 리스트

gkey=[]

def render():
    global gkey #전역변수 수정
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
 # draw cooridnates / XY축
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    glColor3ub(255, 255, 255)   #흰색으로 초기화

    for i in range(len(gkey)):              # order :r-to-l global frame /
                                            # 역순으로 적용, 최근에 누른 변형이 먼저 local로 적용되야함
        if gkey[len(gkey)-i-1]==2:          # input Q, translate -0.1 in x / x축방향 -0.1이동
            glTranslatef(-0.1, 0, 0)
        elif gkey[len(gkey)-i-1]==3:        # input E, translate 0.1 in x / x축방향 +0.1이동
            glTranslatef(0.1, 0, 0)
        elif gkey[len(gkey) - i - 1] == 4:  # input:A, rotate 10 in ccw / 반시계방향 10 회전
            glRotatef(10, 0, 0, 1)
        elif gkey[len(gkey)-i-1]==5:        # input:D, rotate -10 in ccw / 반시계방향 -10 회전
            glRotatef(-10,0,0,1)

    drawTriangle()  #삼각형 그리는 함수

def drawTriangle(): #고정된 삼각형 좌표
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global gkey #전역변수 수정
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:     #gkey(input list) is empty / gkey []로 초기화
            gkey= []
        elif key==glfw.KEY_Q:
            gkey= gkey + [2]        #리스트에 q를 나타내는 2 추가
        elif key==glfw.KEY_E:
            gkey= gkey + [3]        #리스트에 e를 나타내는 3 추가
        elif key==glfw.KEY_A:
            gkey= gkey + [4]        #리스트에 a를 나타내는 4 추가
        elif key==glfw.KEY_D:
            gkey= gkey + [5]        #리스트에 d를 나타내는 5 추가
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, 'triangle movement', None,None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()