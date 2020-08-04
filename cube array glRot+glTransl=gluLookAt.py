# hexaspace computer graphics 10
# cube array glRot+glTransl=gluLookAt
#################################################
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# 한 변이 1인 정육면채 CUBE
def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

# CUBE ARRAY 그리기, PUSH,POP으로 현재행렬에 영향을 주지 않기
def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i,j,-k-1)
                glScalef(.5,.5,.5)
                drawUnitCube()
                glPopMatrix()

# XYZ축
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

def render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()

    # Ortho가 아닌 원근법이 적용된 Perspective를 사용
    gluPerspective(45, 1, 1, 10)

    # Replace this call with two glRotatef() calls and one glRotatef() call
    # gluLookAt 를 glRotatef, glRotatef 로 표현
    #gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)   (3,3,3)위치에서 (0,0,0)을 바라봄
    # (0,0,3)~(3,0,3)각도는 45도, (3,0,3)~(3,3,3)각도는 약 36.264도

    a=np.sqrt(3*3*3)    #정육면체의 대각선

    glTranslatef(0, 0, -a)  # z축으로 -a만큼 이동
    glRotatef(36.264, 1, 0, 0)  # x축을 기준으로 36.264도 회전 (yz평면을 타고 올라감)
    glRotatef(-45, 0, 1, 0)     # y축을 기준으로 45도 회전 (3,3,3으로 이동)
    #xyz축 그리기
    drawFrame()
    # 흰색 큐브 배열 그리기
    glColor3ub(255, 255, 255)
    drawCubeArray()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'cube array glRot+glTransl=gluLookAt', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
