# hexaspace computer graphics 12
# triangular pyramid (삼각뿔) [indexed, glDrawElements()]
# keyboard 123w - camera
#################################################
import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *

gCamAng = 0
gCamHeight = 1.
gVertexArrayIndexed = None
gIndexArray = None

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( 0 , 0 , 0 ), # v0
            (1.5, 0 , 0 ), # v1
            ( 0 ,1.5, 0 ), # v2
            ( 0 , 0 ,1.5), # v3
            ], 'float32')   # array 값 유형
    iarr = np.array([       # index array (v,v,v) 반시계방향
            (0,1,2),    # 옆면(뒤)
            (0,2,3),    # 옆면(좌)
            (0,3,1),    # 밑면
            ])          # (선이 모두 생성되기 때문에 옆면(앞)은 불필요하다.)
    return varr, iarr

def render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()

    gluPerspective(45, 1, 1,10)     # 원근법
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)     #key 123w로 조정
    # xyz축
    drawFrame()
    # 흰색 삼각뿔 그리기
    glColor3ub(255, 255, 255)
    drawCube_glDrawElements()

# triangles index로 3d 그리는 함수
def drawCube_glDrawElements():
    # global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed  #creat~함수로 생성된 array값 받기
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    # glVertexPointer : vertex array로부터 위치와 데이터 포멧을 지정한다
    # glVertexPointer(size(3D points), type값유형(GL_FLOAT), stride간격(3 * varr.itemsize), pointer시작점( varr))
    glVertexPointer(3, GL_FLOAT, 3 * varr.itemsize, varr)
    # glDrawElements : index,vertex array로부터 조각(기초요소)를 랜더링한다.
    # glDrawElements(mode조각유형(GL_TRIANGLES), count인덱스갯수(iarr.size), type인덱스값유형(GL_UNSIGNED_INT), indices시작점(iarr))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():        # xyz축
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

def key_callback(window, key, scancode, action, mods):      # 회전(1,3), 높이(2,w)
    global gCamAng, gCamHeight
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1


def main():
    global gVertexArrayIndexed, gIndexArray

    if not glfw.init():
        return
    window = glfw.create_window(480,480,'triangular pyramid [indexed, glDrawElements()]', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback) # key받기
    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()   # 삼각뿔 index받기

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
