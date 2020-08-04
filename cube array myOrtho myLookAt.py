# hexaspace computer graphics 09
# cube array myOrtho myLookAt
##################################################
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# draw cube glVertex3f quads*4 / 4각형 6개로 육면제 그리기
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

# glTranslatef와 glScalef 를 push pop사이에 함으로써 현재행렬에 영향을 주지 않는다.
def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i,j,-k-1)
                glScalef(.5,.5,.5)
                drawUnitCube()
                glPopMatrix()

# xyz축
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


    myOrtho(-5,5,-5,5,-8,8)
    myLookAt(np.array([5,3,5]), np.array([1,1,-1]),np.array([0,1,0]))

    #Above two lines must behaves exactly same as the below two lines
    #위의 두 함수는 아래 두개와 같은 작동을 한다
    #glOrtho(-5,5,-5,5,-8,8)
    #gluLookAt(5,3,5 , 1,1,-1, 0,1,0)

    # xyz축 그리기
    drawFrame()
    # 흰색 큐브배열 그리기
    glColor3ub(255, 255, 255)
    drawCubeArray()

# glOrtho와 같은 작동을 하게 하는 함수
def myOrtho(left, right, bottom, top, near, far):                           # scale      translate
    moth=np.array([[2/(right-left),0,0,-(right+left)/(right-left)],         # lr평균 0 0 평균차이
                  [0, 2/(top-bottom),0,-(top+bottom)/(top-bottom)],         # 0 tb평균 0 평균차이
                  [0, 0, -2 / (far - near), -(far + near) / (far - near)],  # 0 0 fn평균 평균차이
                  [0, 0, 0, 1]])
    moth=moth.T   #glMultMatrixf는 .T역행렬을 해줘야한다.
    # 현재 행렬에 moth를 곱한다.
    glMultMatrixf(moth)

# eye point, look-at point, up vector --->> 카메라의 coordinates 백터 uvw, origin point(=eye)
def myLookAt(eye, at, up):
    w=(eye-at)/np.sqrt(np.dot(eye-at,eye-at))   # w는 물체->카메라위치의 unit 백터이다
    u=np.cross(up,w)/np.sqrt(np.dot(np.cross(up,w),np.cross(up,w))) #u는 w와 up을 외적(수직한 백터)의 unit
    v=np.cross(w,u) # v는 wu의 외적하여 unit함
    mlook=np.identity(4)    # global frame(object space)->local(world space)로 변환하는 matrix를 만드는 방법은
                            # m=[U,V,W,ORIGIN P]이다.
                            # 반대인 view space<-world space는 m^(-1) = [u1,u2,u3,-U`p1]이다.
                                                                    #  [v1,v2,v3,-V`p2]
                                                                    #  [w1,w2,w3,-W`p3]
    mlook[0, 0:3] = u
    mlook[1, 0:3] = v
    mlook[2, 0:3] = w
    mlook[0, 3] = -np.dot(u,eye)
    mlook[1, 3] = -np.dot(v, eye)
    mlook[2, 3] = -np.dot(w, eye)
    mlook=mlook.T   #glMultMatrixf는 .T역행렬을 해줘야한다.
    # 현재 행렬에 mlook을 곱한다.
    glMultMatrixf(mlook)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'cube array myOrtho myLookAt', None,None)
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
