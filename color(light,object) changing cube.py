# hexaspace computer graphics 13
# color(light,object) changing cube [normalP, glDrawArray()]
# keyboard [123w - camera], [asdf - light], [zxcv - object]
#################################################

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

gCamAng = 0.
gCamHeight = 1.
lightColor = (1.,1.,1.,1.)
objectColor = (1.,1.,1.,1.)

# vertex array로 큐브 그리는 함수
def drawCube_glDrawArray():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    # glNormalPointer : normal array로부터 위치와 데이터 포멧을 지정한다
    # glNormalPointer(type값유형, stride간격, pointer시작점)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    # glVertexPointer : vertex array로부터 위치와 데이터 포멧을 지정한다
    # glVertexPointer(size(3D points), type값유형, stride간격, pointer시작점)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    # glDrawArrays : 위 함수로부터 지정된 vertex array로부터 조각 랜더링한다.
    # glDrawArrays( mode조각 타입, first시작점, count 랜더링할 vertex 갯수)
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

def render():
    global gCamAng, gCamHeight, lightColor, objectColor
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()    # 초기화
    gluPerspective(45, 1, 1,10) # 원근

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()    # 초기화
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0) # 시점

    drawFrame() # 축

    # 조명
    glEnable(GL_LIGHTING)   # light on
    glEnable(GL_LIGHT0)     # light 0
    glEnable(GL_RESCALE_NORMAL)

    # glLightfv(light조명, pname조명속성 , param 색상RGBA 혹은 좌표xyzw)
    lightPos = (3.,4.,5.,1.)    # w=1: 가까운 빛, w=0 먼 빛(균일)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos) # 조명 위치
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)    # 주변 색 (보통 light color보다 10퍼 어둡게)
    # lightColor는 전역함수
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)        # 조명 색
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)       # 반사광

    # 물체
    # glMaterialfv(face유형(front or back), pname 유형, param 값)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)    # 하이라이트 색상(보통 흰색)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)    # 반사 지수 (0~128)
    # objectColor 전역함수
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor) # 물체 색상

    # 큐브 그리기
    glPushMatrix()
    drawCube_glDrawArray()
    glPopMatrix()

    glDisable(GL_LIGHTING)  # light off

# 키보드 입력 함수
def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, lightColor, objectColor
    if action==glfw.PRESS or action==glfw.REPEAT:
        # 카메라
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        # 조명
        elif key==glfw.KEY_A:
            lightColor = (1.,0.,0.,1.)  # 빨
        elif key==glfw.KEY_S:
            lightColor = (0.,1.,0.,1.)  # 초
        elif key==glfw.KEY_D:
            lightColor = (0.,0.,1.,1.)  # 파
        elif key==glfw.KEY_F:
            lightColor = (1.,1.,1.,1.)  # 흰
        # 물체
        elif key==glfw.KEY_Z:
            objectColor = (1.,0.,0.,1.) # 빨
        elif key==glfw.KEY_X:
            objectColor = (0.,1.,0.,1.) # 초
        elif key==glfw.KEY_C:
            objectColor = (0.,0.,1.,1.) # 파
        elif key==glfw.KEY_V:
            objectColor = (1.,1.,1.,1.) # 흰
# 축 그리기
def drawFrame():
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

# 큐브의 vertex array (normal, position)
def createVertexArraySeparate():
    varr = np.array([
            (0,0,1),         # v0 normal
            ( -1 ,  1 ,  1 ), # v0 position
            (0,0,1),         # v2 normal
            (  1 , -1 ,  1 ), # v2 position
            (0,0,1),         # v1 normal
            (  1 ,  1 ,  1 ), # v1 position

            (0,0,1),         # v0 normal
            ( -1 ,  1 ,  1 ), # v0 position
            (0,0,1),         # v3 normal
            ( -1 , -1 ,  1 ), # v3 position
            (0,0,1),         # v2 normal
            (  1 , -1 ,  1 ), # v2 position

            (0,0,-1),
            ( -1 ,  1 , -1 ), # v4
            (0,0,-1),
            (  1 ,  1 , -1 ), # v5
            (0,0,-1),
            (  1 , -1 , -1 ), # v6

            (0,0,-1),
            ( -1 ,  1 , -1 ), # v4
            (0,0,-1),
            (  1 , -1 , -1 ), # v6
            (0,0,-1),
            ( -1 , -1 , -1 ), # v7

            (0,1,0),
            ( -1 ,  1 ,  1 ), # v0
            (0,1,0),
            (  1 ,  1 ,  1 ), # v1
            (0,1,0),
            (  1 ,  1 , -1 ), # v5

            (0,1,0),
            ( -1 ,  1 ,  1 ), # v0
            (0,1,0),
            (  1 ,  1 , -1 ), # v5
            (0,1,0),
            ( -1 ,  1 , -1 ), # v4

            (0,-1,0),
            ( -1 , -1 ,  1 ), # v3
            (0,-1,0),
            (  1 , -1 , -1 ), # v6
            (0,-1,0),
            (  1 , -1 ,  1 ), # v2

            (0,-1,0),
            ( -1 , -1 ,  1 ), # v3
            (0,-1,0),
            ( -1 , -1 , -1 ), # v7
            (0,-1,0),
            (  1 , -1 , -1 ), # v6

            (1,0,0),
            (  1 ,  1 ,  1 ), # v1
            (1,0,0),
            (  1 , -1 ,  1 ), # v2
            (1,0,0),
            (  1 , -1 , -1 ), # v6

            (1,0,0),
            (  1 ,  1 ,  1 ), # v1
            (1,0,0),
            (  1 , -1 , -1 ), # v6
            (1,0,0),
            (  1 ,  1 , -1 ), # v5

            (-1,0,0),
            ( -1 ,  1 ,  1 ), # v0
            (-1,0,0),
            ( -1 , -1 , -1 ), # v7
            (-1,0,0),
            ( -1 , -1 ,  1 ), # v3

            (-1,0,0),
            ( -1 ,  1 ,  1 ), # v0
            (-1,0,0),
            ( -1 ,  1 , -1 ), # v4
            (-1,0,0),
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    return varr

gVertexArraySeparate = None
def main():
    global gVertexArraySeparate

    if not glfw.init():
        return
    window = glfw.create_window(480,480,'color(light,object) changing cube', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArraySeparate = createVertexArraySeparate()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
