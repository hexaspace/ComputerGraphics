# hexa computer graphics 04
# rotating triangle 2d
#################################################


import glfw
from OpenGL.GL import *
import numpy as np

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # x축과 y측
    glBegin(GL_LINES)   #선 gl_line 옵션으로 그리기
    glColor3ub(255, 0, 0)   #색상 빨강
    glVertex2fv(np.array([0.,0.]))  #2차원 (2fv)
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)   #색상 초록
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # 삼각형 그리기
    glBegin(GL_TRIANGLES)   #선 gl_triangles 옵션으로 그리기
    glColor3ub(255, 255, 255) #색상 흰색
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )  # 2차원
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )  # 초기 (0,0),(0,0.5),(0.5,0)의 삼각형을 행렬곱을 사용하여 transform시킨다.
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )  # 각 점(point이기 때문에 마지막 값이 1)을 곱한 뒤 마지막 값을 제거한다.([:-1])
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"rotating_triangle", None,None) #480*480 윈도우 사이즈
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    # glfw.swap_interval : glfw.swap_buffer()를 호출하기 전 기다리기 위해 새로고침하는 screen의 수, 반복문의 시간간격을 조절한다.
    # 만약 모니터 refresh가 60Hz라면, while루프는 매 1/60초마다 반복된다.
    glfw.swap_interval(1)

    while not glfw.window_should_close(window): #윈도우가 닫힐 때 까지
        glfw.poll_events()
        t = glfw.get_time() # t=시간
        # rotate t rad / t rad 각도로 회전
        th = t
        R = np.array([[np.cos(th), -np.sin(th), 0.],
                      [np.sin(th), np.cos(th), 0.],
                      [0., 0., 1.]])

        # translate by (.5, 0.) / (0.5, 0)만큼 이동
        T = np.array([[1., 0., .5],
                      [0., 1., 0.],
                      [0., 0., 1.]])
        #first translate and second rotate  / 순서 : 이동 후 회전 (global 기준)

        render(R @ T)

        glfw.swap_buffers(window)   # 스왑 버퍼

    glfw.terminate()    #종료

if __name__ == "__main__":
    main()