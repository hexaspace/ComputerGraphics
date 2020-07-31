# hexaspace computer graphics 02
# dodecagon(reqular12-side polygon) primitive type of vertex
#################################################
import glfw
from OpenGL.GL import *

import numpy as np

#global val
PTYPE = [GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP, GL_TRIANGLES,
       GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP, GL_POLYGON]
#0:점, 1:선분(2개씩), 2:선분(연속), 3:루프(시작과 끝 반복), 4:삼각형(3개씩)
# 5:삼각형(연속된 3 vertex), 6:삼각형(모든 3vertex), 7:사각형(4개씩), 8:, 9:다각형
INDEX = 3   #초기 primitive type : 루프

# Draw a 12-sided polygon / 정12각형 그리기
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(PTYPE[INDEX])   #그리기 시작, primitive type을 전역변수(행렬과 index)로부터 받는다.

    a=np.arange(0, 360, 30) #행렬 a는 0~360을 30씩 건너뛰며 갖는 값들이다.
    for i in a:             #행렬 a값들을 한번씩 반복되며 각 요소는 변수 i이다.
        angle = i * np.pi / 180     #각도 degree i를 rad값으로 변환
        glVertex2f(np.cos(angle), np.sin(angle))    #(cos(angle),sin(angle))좌표에 2차원 점을 찍음

    glEnd()                 #그리기 끝

def key_callback(window, key, scancode, action, mods):  #키보드 입력을 받는 함수
    global INDEX    #전역변수 수정
    if action == glfw.PRESS:    #버튼이 눌렸을 때
        if key==glfw.KEY_0:     #키 값이 0 일 때
            INDEX = 0           #INDEX를 0으로 바꾼다.
        elif key==glfw.KEY_1:
            INDEX = 1
        elif key==glfw.KEY_2:
            INDEX = 2
        elif key==glfw.KEY_3:
            INDEX = 3
        elif key==glfw.KEY_4:
            INDEX = 4
        elif key==glfw.KEY_5:
            INDEX = 5
        elif key==glfw.KEY_6:
            INDEX = 6
        elif key==glfw.KEY_7:
            INDEX = 7
        elif key==glfw.KEY_8:
            INDEX = 8
        elif key==glfw.KEY_9:
            INDEX = 9

def main():
    # Initialize the library / 라이브러리 초기화
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context / 윈도우 생성, opengl설정
    window = glfw.create_window(480,480,"dodecagon primitive type", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window / 윈도우가 닫힐 때 까지 반복
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()