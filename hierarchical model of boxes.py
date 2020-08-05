# hexaspace computer graphics 11
# hierarchical model of boxes
#################################################
import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    # 현재 행렬 투사모드
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2, 2, -2, 2, -1, 1)
    # 현재 행렬 모델 뷰 모드
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    t = glfw.get_time()     #시간 t에 따라 움직임
    # [[기본 frame]]
    drawFrame()
    # [[blue base]] transformation
    glPushMatrix()                  # push
    glTranslatef(np.sin(t), 0, 0)   # {x축 움직임}

    # blue base and frame drawing
    glPushMatrix()                  # push push
    drawFrame()             # 좌표축
    glScalef(.2, .2, .2)    # (축소)
    glColor3ub(0, 0, 255)   # (파랑)
    drawBox()               # 박스
    glPopMatrix()                   # push (push pop)

    # [[red arm]] transformation
    glRotatef(t * (180 / np.pi), 0, 0, 1)   # {z축 회전}
    glTranslatef(.5, 0, .01)                # {이동}(보이기 위해 z축 0.01 움직임)

    # red arm and frame drawing
    glPushMatrix()                  # push (push pop) push
    drawFrame()             # 좌표축
    glScalef(.5, .1, .1)    # (스케일)
    glColor3ub(255, 0, 0)   # (빨강)
    drawBox()               # 박스
    glPopMatrix()                   # push (push pop) (push pop)

    # [[green arm]] transformation
    glTranslatef(0.5, 0, .01)   # {이동}
    glRotatef(t * (180 / np.pi), 0, 0, 1)   # {회전}
    # green arm and frame drawing
    glPushMatrix()                  # push (push pop) (push pop) push
    drawFrame()             # 좌표축
    glScalef(.2, .2, .2)    # (스케일)
    glColor3ub(0, 255, 0)   # (초록)
    drawBox()               # 박스
    glPopMatrix()                   # push (push pop) (push pop) (push pop)
    
    glPopMatrix()                   # {push (push pop) (push pop) (push pop) pop}


# 2x2 박스
def drawBox():
    glBegin(GL_QUADS)
    glVertex3fv(np.array([1,1,0.]))
    glVertex3fv(np.array([-1,1,0.]))
    glVertex3fv(np.array([-1,-1,0.]))
    glVertex3fv(np.array([1,-1,0.]))
    glEnd()

# draw coordinate: x in red, y in green, z in blue/ xyz축
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


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"hierarchical model of boxes", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
