# hexa computer graphics 03
# transformed triangle(keyboard wesdxcr1)

import glfw
from OpenGL.GL import *
import numpy as np

#global variable / 전역변수- 행렬, 지금까지의 삼각형 변형값 축적
gComposedM = np.array([[1., 0., 0.],
                        [0., 1., 0.],
                        [0., 0., 1.]])

def render():
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
    # draw triangle / 삼각형 그리기
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv((gComposedM @ np.array([.0, .5, 1.]))[:-1])
    glVertex2fv((gComposedM @ np.array([.0, .0, 1.]))[:-1])
    glVertex2fv((gComposedM @ np.array([.5, .0, 1.]))[:-1])
    glEnd()

#key down function / 키보드 키 입력 함수
def key_callback(window, key, scancode, action, mods):
    global gComposedM   #전역변수 수정 시 필요
    th = np.radians(10) # degree 10 을 radian 10 으로 변환
    if action == glfw.PRESS or action == glfw.REPEAT: #눌렀거나 눌러져있을 때
    # 1 : reset     전역행렬을 np.identity(3)로 초기화
        if key==glfw.KEY_1:
            gComposedM = np.array([[1., 0., 0],
                                   [0., 1., 0.],
                                   [0., 0., 1.]])
    #  W : scale 0.9 in x   / x방향 0.9배로 scale 감소(x값들이 0.9배)
        elif key==glfw.KEY_W:
            gComposedM = np.array([[.9, 0., 0],
                                   [0., 1., 0.],
                                   [0., 0., 1.]]) @ gComposedM
    # E: scale 1.1 in x   / x방향 1.1배로 scale 증가(x값들이 1.1배)
        elif key==glfw.KEY_E:
            gComposedM = np.array([[1.1, 0., 0],
                                   [0., 1., 0.],
                                   [0., 0., 1.]]) @ gComposedM
    # S : rotate 10 deg ccw / 반시계방향으로 10도 회전
        elif key==glfw.KEY_S:
            gComposedM = np.array([[np.cos(th), -np.sin(th), 0],
                                   [np.sin(th), np.cos(th), 0.],
                                   [0., 0., 1.]]) @ gComposedM
    # D: rotate 10 deg cw / 시계방향으로 10도 회전
        elif key==glfw.KEY_D:
            gComposedM = np.array([[np.cos(th), np.sin(th), 0],
                                   [-np.sin(th), np.cos(th), 0.],
                                   [0., 0., 1.]]) @ gComposedM
    # X : shear -0.1 in x / x축으로 -0.1값만큼 shear(y값에 비례하여 변형 증가)
        elif key==glfw.KEY_X:
            gComposedM = np.array([[1., -0.1, 0],
                                   [0., 1., 0.],
                                   [0., 0., 1.]]) @ gComposedM
    # C : shear 0.1 in x / x축으로 0.1값만큼 shear(y값에 비례하여 변형 증가)
        elif key==glfw.KEY_C:
            gComposedM = np.array([[1., 0.1, 0],
                                   [0., 1., 0.],
                                   [0., 0., 1.]]) @ gComposedM
    # R : reflection across x / x축기준으로 반전
        elif key==glfw.KEY_R:
            gComposedM = np.array([[1., 0., 0],
                                   [0., -1., 0.],
                                   [0., 0., 1.]]) @ gComposedM


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"transformed triangle-keyboard", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()