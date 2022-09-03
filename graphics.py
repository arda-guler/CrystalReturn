import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

from math_utils import *
from ui import *
from vector3 import *

floor_z_offset = 0
floor_x_offset = 0

def calcTransparentColor(background_color, main_color, alpha=0.5):
    delta_r = background_color[0] - main_color[0]
    delta_g = background_color[1] - main_color[1]
    delta_b = background_color[2] - main_color[2]

    return [main_color[0] + delta_r * (1-alpha), main_color[1] + delta_g * (1-alpha), main_color[2] + delta_b * (1-alpha)]

def drawOrigin():
    glBegin(GL_LINES)
    glColor(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(100,0,0)
    glColor(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,100,0)
    glColor(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,100)
    glEnd()

def drawPoints(points):

    for p in points:
        glColor(p.color[0], p.color[1], p.color[2])
        
        glPushMatrix()
        glTranslatef(p.pos.x, p.pos.y, p.pos.z)

        glBegin(GL_POINTS)
        glVertex3f(0, 0, 0)
        glEnd()

        glPopMatrix()

def drawPoint2D(x, y, color, camera):
    glPushMatrix()

    glTranslate(-camera.pos.x,
                -camera.pos.y,
                -camera.pos.z)
    
    glColor(color[0], color[1], color[2])

    glBegin(GL_POINTS)

    x1 = x * 100
    y1 = y * 100

    glVertex3f((x1) * camera.get_orient()[0][0] + (y1) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x1) * camera.get_orient()[0][1] + (y1) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x1) * camera.get_orient()[0][2] + (y1) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])

    glEnd()
    
    glPopMatrix()

def drawLine2D(x1, y1, x2, y2, color, camera):
    glPushMatrix()
    glTranslate(-camera.pos.x,
                -camera.pos.y,
                -camera.pos.z)
    
    glColor(color[0], color[1], color[2])
    
    glBegin(GL_LINES)

    x1 = x1 * 100
    y1 = y1 * 100
    x2 = x2 * 100
    y2 = y2 * 100
    glVertex3f((x1) * camera.get_orient()[0][0] + (y1) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x1) * camera.get_orient()[0][1] + (y1) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x1) * camera.get_orient()[0][2] + (y1) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])
    
    glVertex3f((x2) * camera.get_orient()[0][0] + (y2) * camera.get_orient()[1][0] + (-1000) * camera.get_orient()[2][0],
               (x2) * camera.get_orient()[0][1] + (y2) * camera.get_orient()[1][1] + (-1000) * camera.get_orient()[2][1],
               (x2) * camera.get_orient()[0][2] + (y2) * camera.get_orient()[1][2] + (-1000) * camera.get_orient()[2][2])
    glEnd()
    glPopMatrix()

def drawRectangle2D(x1, y1, x2, y2, color, camera):
    drawLine2D(x1, y1, x2, y1, color, camera)
    drawLine2D(x1, y1, x1, y2, color, camera)
    drawLine2D(x2, y1, x2, y2, color, camera)
    drawLine2D(x1, y2, x2, y2, color, camera)

def drawScoreCounter(x1, y1, camera, score, colorScore, text_size=0.075):
    render_AN("SCORE: " + str(round(score,1)), colorScore, [x1, y1], camera, text_size)

def drawGround(floor, mirage, dt, size=250, divisions=20):
    global floor_x_offset, floor_z_offset

    y_floor = floor.height
    glColor(floor.color[0], floor.color[1], floor.color[2])

    glBegin(GL_LINES)
    
    for xi in range(divisions + 1):
        glVertex3f(2* xi * (size/divisions) - size + floor_x_offset, y_floor, -size)
        glVertex3f(2* xi * (size/divisions) - size + floor_x_offset, y_floor, +size)

    for zi in range(divisions + 1):
        glVertex3f(-size, y_floor, 2* zi * (size/divisions) - size + floor_z_offset)
        glVertex3f(+size, y_floor, 2* zi * (size/divisions) - size + floor_z_offset)

    glEnd()

    floor_x_offset -= mirage.get_side_speed(dt)
    floor_z_offset += mirage.speed * dt
    floor_x_offset = floor_x_offset % (2 * (size/divisions))
    floor_z_offset = floor_z_offset % (2 * (size/divisions))

def drawForces(forces):
    
    for f in forces:
        glPushMatrix()

        scaler = 0.2
        start_position = f.point.pos
        end_position = f.point.pos + f.force
        f_vector = f.force * scaler
        
        f_dir = f_vector.normalized()
        arrowhead_start = f.force * scaler * 0.8

        if not f_dir.cross(vec3(1,0,0)) == vec3(0,0,0):
            arrowhead_vector1 = f_dir.cross(vec3(1,0,0))
        else:
            arrowhead_vector1 = f_dir.cross(vec3(0,1,0))

        arrowhead_vector2 = arrowhead_vector1.cross(f_dir)

        arrowhead_vector1 = arrowhead_vector1 * f.force.mag() * scaler * 0.1
        arrowhead_vector2 = arrowhead_vector2 * f.force.mag() * scaler * 0.1
            
        arrowhead_pt1 = arrowhead_start + arrowhead_vector1
        arrowhead_pt2 = arrowhead_start - arrowhead_vector1

        arrowhead_pt3 = arrowhead_start + arrowhead_vector2
        arrowhead_pt4 = arrowhead_start - arrowhead_vector2
        
        glTranslate(start_position.x, start_position.y, start_position.z)
        glColor(1,0,1)

        glBegin(GL_LINES)

        glVertex3f(0,0,0)
        glVertex3f(f_vector.x, f_vector.y, f_vector.z)

        glVertex3f(arrowhead_pt1.x, arrowhead_pt1.y, arrowhead_pt1.z)
        glVertex3f(arrowhead_pt3.x, arrowhead_pt3.y, arrowhead_pt3.z)

        glVertex3f(arrowhead_pt2.x, arrowhead_pt2.y, arrowhead_pt2.z)
        glVertex3f(arrowhead_pt4.x, arrowhead_pt4.y, arrowhead_pt4.z)

        glVertex3f(arrowhead_pt2.x, arrowhead_pt2.y, arrowhead_pt2.z)
        glVertex3f(arrowhead_pt3.x, arrowhead_pt3.y, arrowhead_pt3.z)

        glVertex3f(arrowhead_pt1.x, arrowhead_pt1.y, arrowhead_pt1.z)
        glVertex3f(arrowhead_pt4.x, arrowhead_pt4.y, arrowhead_pt4.z)

        glVertex3f(arrowhead_pt1.x, arrowhead_pt1.y, arrowhead_pt1.z)
        glVertex3f(f_vector.x, f_vector.y, f_vector.z)

        glVertex3f(arrowhead_pt2.x, arrowhead_pt2.y, arrowhead_pt2.z)
        glVertex3f(f_vector.x, f_vector.y, f_vector.z)

        glVertex3f(arrowhead_pt3.x, arrowhead_pt3.y, arrowhead_pt3.z)
        glVertex3f(f_vector.x, f_vector.y, f_vector.z)

        glVertex3f(arrowhead_pt4.x, arrowhead_pt4.y, arrowhead_pt4.z)
        glVertex3f(f_vector.x, f_vector.y, f_vector.z)

        glEnd()

        glPopMatrix()

def drawCursors(cursors, camera):

    for cursor in cursors:
        if cursor.visible:
            glPushMatrix()

            glTranslate(cursor.pos.x,
                        cursor.pos.y,
                        cursor.pos.z)
            
            glColor(cursor.color[0], cursor.color[1], cursor.color[2])

            glBegin(GL_LINES)

            glVertex3f(2,0,0)
            glVertex3f(-2,0,0)

            glVertex3f(0,2,0)
            glVertex3f(0,-2,0)

            glVertex3f(0,0,2)
            glVertex3f(0,0,-2)

            glEnd()
            
            glPopMatrix()

def drawObstaclesAndPowerups(comblist):
    for o in comblist:
        
        glPushMatrix()

        glTranslatef(o.pos.x, o.pos.y, o.pos.z)
        glScalef(o.size.x, o.size.y, o.size.z)

        main_color = o.color
        background_color = [0.1, 0.1, 0.25]

        if o.pos.z < -300:
            alpha = min(max(     1-((-o.pos.z-300)/300)         , 0), 1)
            main_color = calcTransparentColor(background_color, main_color, alpha)

        for mesh in o.model.mesh_list:
            glColor(main_color[0], main_color[1], main_color[2])
            glPolygonMode(GL_FRONT, GL_FILL)
            glBegin(GL_POLYGON)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*o.model.vertices[vertex_i])
            glEnd()

            glColor(main_color[0] + 0.1, main_color[1] + 0.1, main_color[2] + 0.1)
            glPolygonMode(GL_FRONT, GL_LINE)
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*o.model.vertices[vertex_i])
            glEnd()

        glPopMatrix()

def drawMirage(mirage):
    
    # here we go
    glPushMatrix()

    # put us in correct position
    glTranslatef(0, 0, 0)
    glRotatef(-mirage.bank, 0, 0, 1)

    # actually render model now
    for mesh in mirage.model.mesh_list:
##        glColor(mirage.get_color()[0]/1.25, mirage.get_color()[1]/1.25, mirage.get_color()[2]/1.25)
##        glPolygonMode(GL_FRONT, GL_FILL)
##        glBegin(GL_POLYGON)
##        for face in mesh.faces:
##            for vertex_i in face:
##                glVertex3f(*mirage.model.vertices[vertex_i])
##        glEnd()

        glColor(mirage.get_color()[0], mirage.get_color()[1], mirage.get_color()[2])
        glPolygonMode(GL_FRONT, GL_LINE)
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                glVertex3f(*mirage.model.vertices[vertex_i])
        glEnd()

    # do sparks
    spark_spread = 0.05
    if mirage.bank >= mirage.max_bank:
        
        glColor(0, 1, 1)
        for i in range(5):
            glPointSize(random.randint(2,4))
            glBegin(GL_POINTS)
            glVertex3f(5 + random.uniform(-spark_spread, spark_spread), -0.15 + random.uniform(-spark_spread, spark_spread), 0 + random.uniform(-spark_spread, spark_spread*36))
            glEnd()

    elif mirage.bank <= -mirage.max_bank:
        
        glColor(0, 1, 1)
        for i in range(5):
            glPointSize(random.randint(2,4))
            glBegin(GL_POINTS)
            glVertex3f(-5 + random.uniform(-spark_spread, spark_spread), -0.15 + random.uniform(-spark_spread, spark_spread), 0 + random.uniform(-spark_spread, spark_spread*36))
            glEnd()

    # do engine plume
    plume_spread = 0.25
    glColor(1, 0, 1)
    for i in range(max(15 * int(mirage.speed/50), 15)):
        glPointSize(random.randint(8,10))
        glBegin(GL_POINTS)
        glVertex3f(-2 + random.uniform(-plume_spread*3, plume_spread*3), 0 + random.uniform(-plume_spread*0.2, plume_spread*0.2), 1 + random.uniform(-plume_spread, plume_spread*45))
        glEnd()

    for i in range(max(15 * int(mirage.speed/50), 15)):
        glPointSize(random.randint(8,10))
        glBegin(GL_POINTS)
        glVertex3f(2 + random.uniform(-plume_spread*3, plume_spread*3), 0 + random.uniform(-plume_spread*0.2, plume_spread*0.2), 1 + random.uniform(-plume_spread, plume_spread*45))
        glEnd()
        
    # now get out
    glPopMatrix()

def drawLuna(luna, cam):

    glPointSize(10)
    drawPoint2D(0, luna.height/150, luna.color, cam)

def drawScene(cam, mirage, floor, obstacles, powerups, luna, dt, score):
    comblist = obstacles + powerups
    comblist.sort(key=lambda x: mag([-x.pos.x - cam.pos.x, -x.pos.y - cam.pos.y, -x.pos.z - cam.pos.z]), reverse=True)

    drawLine2D(-35, 0, 35, 0, floor.color, cam) # draw a horizon
    drawLuna(luna, cam)
    drawGround(floor, mirage, dt)
    drawObstaclesAndPowerups(comblist)
    drawMirage(mirage)
    drawScoreCounter(-3, 4, cam, score, [1,0,0])
    #drawOrigin()

