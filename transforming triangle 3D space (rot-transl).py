# hexaspace computer graphics 08
# transforming triangle 3D space (rot-transl) (global-translate[q,e],camera rotate[1,3], local-rotate y[a,d] x[w,s])
#################################################

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.    #초기 카메라 각도 0
gComposedM = np.identity(4) #초기 transform행렬 identity

def render(M, camAng):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    # 현재 행렬 identity 초기화
    glLoadIdentity()
    # use orthogonal projection / 직교투영(원근법을 적용 x)
    glOrtho(-1,1, -1,1, -1,1)
    # rotate "camera" position to see this 3D space better
    # 회전하는 카메라 위치를 잡으므로써 3d공간을 잘보게함
    # (카메라 위치 xyz , 타겟 위치 xyz, 위아래 방향)
    gluLookAt(.1*np.sin(camAng),.1, .1*np.cos(camAng), 0,0,0, 0,1,0)
    # draw coordinate: x in red, y in green, z in blue
    # 빨강x, 초록y, 파랑z축
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    # transform 행렬 (M)과 삼각형 좌표(마지막 1은 vector값)를 곱한 뒤 마지막값(1)을 뺀다.
    glVertex3fv((M @ np.array([.0,.5,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.0,.0,0.,1.]))[:-1])
    glVertex3fv((M @ np.array([.5,.0,0.,1.]))[:-1])
    glEnd()

# 키보드 입력값을 받는 함수
def key_callback(window, key, scancode, action, mods):
    global gCamAng, gComposedM  #전역변수 쉉
    th = np.radians(10) # deg 10을 rad로 변형
    if action==glfw.PRESS or action==glfw.REPEAT:   #누르거나 누르고 있을 때
        # 카메라 회전
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)  # 10 deg 감소
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)   # 10 deg 증가
        # 삼각형 이동
        # global기준(고정), X @ gComposedM 형태로 local시점에선 마지막에 이동이 적용됨
        elif key==glfw.KEY_Q:   # x축 방향으로 -0.1 이동
            gComposedM = np.array([[1.,0.,0.,-0.1],
                                    [0.,1.,0.,0.],
                                    [0.,0.,1.,0.],
                                    [0.,0.,0.,1.]]) @ gComposedM

        elif key==glfw.KEY_E:   # x축 방향으로 0.1 이동
            gComposedM = np.array([[1.,0.,0.,0.1],
                                    [0.,1.,0.,0.],
                                    [0.,0.,1.,0.],
                                    [0.,0.,0.,1.]]) @ gComposedM
        # 삼각형 회전
        # local기준(변형된 축에 적용), gComposedM @ X 형태로 local시점에선 먼저 회전이 적용됨

        elif key==glfw.KEY_A:   # y축 기준 -th 회전
            gComposedM = gComposedM @ np.array([[np.cos(-th), 0.,np.sin(-th),0.],
                                                [0.,          1.,         0.,0.],
                                                [-np.sin(-th),0.,np.cos(-th),0.],
                                                [0.,          0.,        0.,1.]])
        elif key==glfw.KEY_D:   # y축 기준 th 회전
            gComposedM = gComposedM @ np.array([[np.cos(th), 0.,np.sin(th),0.],
                                                [0.,         1.,        0.,0.],
                                                [-np.sin(th),0.,np.cos(th),0.],
                                                [0.,         0.,        0.,1.]])
        elif key==glfw.KEY_W:   # x축 기준 -th 회전
            gComposedM = gComposedM @ np.array([[1.,         0.,          0.,0.],
                                                [0.,np.cos(-th),-np.sin(-th),0.],
                                                [0.,np.sin(-th), np.cos(-th),0.],
                                                [0.,         0.,          0.,1.]])
        elif key==glfw.KEY_S:   # x축 기준 th 회전
            gComposedM = gComposedM @ np.array([[1.,        0.,         0.,0.],
                                                [0.,np.cos(th),-np.sin(th),0.],
                                                [0.,np.sin(th), np.cos(th),0.],
                                                [0.,        0.,         0.,1.]])
def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, 'transforming triangle 3D space (rot-transl)', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gComposedM, gCamAng)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
