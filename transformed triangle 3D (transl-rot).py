# hexaspace computer graphics 07
# transformed triangle 3D space (transl-rot) global(translate,rotate, camera rotate[1,3])
#################################################
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.

def render(camAng):
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    # set the current matrix to the identity matrix / 현재 행렬을 identity로 초기화
    glLoadIdentity()
    # use orthogonal projection (multiply the current matrix by "projection" matrix)
    # 직교 투영 사용 (현재 행렬을 투영행렬에 곱한다.)
    # 2x2x2 육면체만큼만 현재 화면에 맞춘다.
    glOrtho(-1,1, -1,1, -1,1)
    gluLookAt(.1*np.sin(camAng),.1, .1*np.cos(camAng), 0,0,0, 0,1,0)

    # [draw global]
    # xy축 그리기
    drawFrame()
    # white triangle 흰 삼각형(g)그리기
    glColor3ub(255, 255, 255)
    drawTriangle()
    # [draw local] - order reverse / global입장에서 변형하기 때문에 순서를 반대로 한다.
    glTranslatef(.6, .0, 0) #x축 방향으로 0.6 이동
    glRotatef(30, 0, 0, 1)  # (angle,x,y,z)z축을 기준으로 30도 회전 (z축은 3d에서 화면에 수직한 방향)
    # xy축 그리기
    drawFrame()
    # blue triangle 파란 사각형(l)그리기
    glColor3ub(0, 0, 255)
    drawTriangle()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()

# 키보드 입력값을 받는 함수
def key_callback(window, key, scancode, action, mods):
    global gCamAng  #전역변수 쉉
    th = np.radians(10) # deg 10을 rad로 변형
    if action==glfw.PRESS or action==glfw.REPEAT:   #누르거나 누르고 있을 때
        # 카메라 회전
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)  # 10 rad 감소
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)   # 10 rad 증가


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, 'transformed triangle 3D space (transl-rot)', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gCamAng)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
