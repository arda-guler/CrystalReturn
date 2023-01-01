import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import pywavefront

from math_utils import *
from ui import *
from vector3 import *
from poems import poem_list

floor_z_offset = 0
floor_x_offset = 0

shield_model = pywavefront.Wavefront("data/models/shield.obj", collect_faces=True)
speed_time_remaining = 0
shield_hexagon_step = 0
last_num_shields = 0

poem_line_countdown = 0
last_poem_line = 0
pline_x = 0
pline_y = 0

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
    global floor_x_offset, floor_z_offset, shield_hexagon_step

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

def drawObstaclesAndPowerups(comblist, current_palette):
    for o in comblist:

        main_color = o.color
        background_color = current_palette["background"]

        if o.pos.z < -300:
            alpha = min(max(     1-((-o.pos.z-300)/300)         , 0), 1)
            main_color = calcTransparentColor(background_color, main_color, alpha)

        if o.rot:
            drawModelGeneric(o.model,
                             [o.pos.x, o.pos.y, o.pos.z],
                             [1, o.rot.x, o.rot.y, o.rot.z],
                             [o.size.x, o.size.y, o.size.z],
                             main_color)
        else:
            drawModelGeneric(o.model,
                             [o.pos.x, o.pos.y, o.pos.z],
                             False,
                             [o.size.x, o.size.y, o.size.z],
                             main_color)

def drawMirage(mirage, current_palette):
    global shield_hexagon_step

    drawModelGeneric(mirage.model, [random.uniform(-1, 1) * shield_hexagon_step/500, random.uniform(-1, 1) * shield_hexagon_step/500, 0], [-mirage.bank, 0, 0, 1], False, mirage.get_color(), True, False)

    glPushMatrix()
    glTranslatef(0, 0, 0)
    glRotatef(-mirage.bank, 0, 0, 1)
    # do sparks
    spark_spread = 0.05
    if mirage.bank >= mirage.max_bank:
        
        glColor(current_palette["sparks"][0], current_palette["sparks"][1], current_palette["sparks"][2])
        for i in range(5):
            glPointSize(random.randint(2,4))
            glBegin(GL_POINTS)
            glVertex3f(5 + random.uniform(-spark_spread, spark_spread), -0.15 + random.uniform(-spark_spread, spark_spread), 0 + random.uniform(-spark_spread, spark_spread*36))
            glEnd()

    elif mirage.bank <= -mirage.max_bank:
        
        glColor(current_palette["sparks"][0], current_palette["sparks"][1], current_palette["sparks"][2])
        for i in range(5):
            glPointSize(random.randint(2,4))
            glBegin(GL_POINTS)
            glVertex3f(-5 + random.uniform(-spark_spread, spark_spread), -0.15 + random.uniform(-spark_spread, spark_spread), 0 + random.uniform(-spark_spread, spark_spread*36))
            glEnd()

    # do engine plume
    plume_spread = 0.25
    glColor(current_palette["plume"][0], current_palette["plume"][1], current_palette["plume"][2])
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

def drawSpeedArrows(cam, current_palette):
    global speed_time_remaining

    if not speed_time_remaining:
        return

    if speed_time_remaining < 0:
        speed_time_remaining = 0
        return

    state = int(speed_time_remaining*10 % 4)

    if state == 3:
        drawLine2D(6, 2, 5, 0, current_palette["powerup_speed"], cam)
        drawLine2D(6, -2, 5, 0, current_palette["powerup_speed"], cam)

        drawLine2D(-6, 2, -5, 0, current_palette["powerup_speed"], cam)
        drawLine2D(-6, -2, -5, 0, current_palette["powerup_speed"], cam)
        
    elif state == 2:
        drawLine2D(5, 2, 4, 0, current_palette["powerup_speed"], cam)
        drawLine2D(5, -2, 4, 0, current_palette["powerup_speed"], cam)

        drawLine2D(-5, 2, -4, 0, current_palette["powerup_speed"], cam)
        drawLine2D(-5, -2, -4, 0, current_palette["powerup_speed"], cam)
        
    elif state == 1:
        drawLine2D(4, 2, 3, 0, current_palette["powerup_speed"], cam)
        drawLine2D(4, -2, 3, 0, current_palette["powerup_speed"], cam)

        drawLine2D(-4, 2, -3, 0, current_palette["powerup_speed"], cam)
        drawLine2D(-4, -2, -3, 0, current_palette["powerup_speed"], cam)
        
def drawShieldHexagon(cam, current_palette):
    global shield_hexagon_step

    if not shield_hexagon_step:
        return

    hex_size = (1.1 - int(shield_hexagon_step % 50) * 0.025)
    
    drawLine2D(3*hex_size, 5.196*hex_size, -3*hex_size, 5.196*hex_size, current_palette["powerup_invulnerability"], cam)
    drawLine2D(3*hex_size, -5.196*hex_size, -3*hex_size, -5.196*hex_size, current_palette["powerup_invulnerability"], cam)
    drawLine2D(6*hex_size, 0, 3*hex_size, 5.196*hex_size, current_palette["powerup_invulnerability"], cam)
    drawLine2D(-6*hex_size, 0, -3*hex_size, 5.196*hex_size, current_palette["powerup_invulnerability"], cam)
    drawLine2D(6*hex_size, 0, 3*hex_size, -5.196*hex_size, current_palette["powerup_invulnerability"], cam)
    drawLine2D(-6*hex_size, 0, -3*hex_size, -5.196*hex_size, current_palette["powerup_invulnerability"], cam)

    shield_hexagon_step -= 1

def drawLuna(luna, cam, current_palette):

    glPointSize(15)

    if luna.height > 50:
        drawPoint2D(0, luna.height/150, luna.color, cam)
    elif luna.height > 0:
        background_color = current_palette["background"]
        alpha = luna.height/50
        color = calcTransparentColor(background_color, luna.color, alpha)
        drawPoint2D(0, luna.height/150, color, cam)
    else:
        pass

def drawModelGeneric(model, pos, rot, scale, color, line=True, poly=True):
    
    glPushMatrix()
    
    glTranslatef(pos[0], pos[1], pos[2])

    if rot:
        glRotatef(rot[0], rot[1], rot[2], rot[3])

    if scale:
        glScalef(scale[0], scale[1], scale[2])
        
    glColor(color[0], color[1], color[2])

    if poly and line:
        for mesh in model.mesh_list:
            glColor(color[0]-0.1, color[1]-0.1, color[2]-0.1)
            glPolygonMode(GL_FRONT, GL_FILL)
            glBegin(GL_POLYGON)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()

            glColor(color[0], color[1], color[2])
            glPolygonMode(GL_FRONT, GL_LINE)
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()
            
    elif poly:
        for mesh in model.mesh_list:
            glPolygonMode(GL_FRONT, GL_FILL)
            glBegin(GL_POLYGON)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()

    elif line:
        for mesh in model.mesh_list:
            glPolygonMode(GL_FRONT, GL_LINE)
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*model.vertices[vertex_i])
            glEnd()

    glPopMatrix()

def drawShieldCount(num_shields, score, current_palette):
    global shield_model

    rotation = (score % 500)/250 * 360

    if num_shields > 0:
        # shield 1
        drawModelGeneric(shield_model, [6,-2.5,-1], [rotation,0,1,0], False, current_palette["powerup_invulnerability"])
        
        if num_shields == 2:
            # shield 2
            drawModelGeneric(shield_model, [8,-2.5,-1], [rotation,0,1,0], False, current_palette["powerup_invulnerability"])

def drawAgilityArrows(mirage, cam, current_palette):
    
    if not mirage.agility_remaining:
        return

    if abs(mirage.bank) > 5:
        num_arrows = int((abs(mirage.bank) - 5)/5)
        
        # arrows to left
        if mirage.bank < 0:
            y_pos = -3
            x_pos = -3

            for i in range(num_arrows):
                # drawLine2D(x1, y1, x2, y2, color, camera)
                drawLine2D(x_pos, y_pos, x_pos + 0.5, y_pos + 0.5, current_palette["powerup_agility"], cam)
                drawLine2D(x_pos, y_pos, x_pos + 0.5, y_pos - 0.5, current_palette["powerup_agility"], cam)
                x_pos -= 1

        # arrows to right
        else:
            y_pos = -3
            x_pos = 3

            for i in range(num_arrows):
                # drawLine2D(x1, y1, x2, y2, color, camera)
                drawLine2D(x_pos, y_pos, x_pos - 0.5, y_pos + 0.5, current_palette["powerup_agility"], cam)
                drawLine2D(x_pos, y_pos, x_pos - 0.5, y_pos - 0.5, current_palette["powerup_agility"], cam)
                x_pos += 1

def drawPaletteChangeStr(palette_change_str, current_palette, cam):
    render_AN(palette_change_str, current_palette["mirage"], [2, 3], cam, 0.075)

def drawPoem(p_index, p_line, dt, cam):
    global poem_line_countdown, pline_y, pline_x
    
    p = poem_list[p_index]
    p_line_max = len(p)

    if p_line_max <= p_line or p_line < 0:
        return

    if poem_line_countdown < 0:
        poem_line_countdown = 0
        y_limit_top = 2.5
        y_limit_bottom = -2.75
        x_limit_left = -5.5
        x_limit_right = 5.5

        pline_y = random.uniform(y_limit_bottom, y_limit_top)
        pline_x = random.uniform(x_limit_left, x_limit_right)
        
        return
    
    if poem_line_countdown:
        current_line = p[p_line]
        poem_line_countdown -= dt

        str_len = len(current_line)

        if str_len < 31:
            str_graphics_size = str_len * 0.075 * 1.75
        else:
            str_graphics_size = str_len * 0.06 * 1.75
        
        if str_len < 31:
            #render_AN(current_line, [1,0,0], [-5, 3], cam, 0.075)
            render_AN(current_line, [1,0,0], [max(pline_x - str_graphics_size, -5.5), pline_y], cam, 0.075)
        else:
            #render_AN(current_line, [1,0,0], [-5, 2.5], cam, 0.06)
            render_AN(current_line, [1,0,0], [max(pline_x - str_graphics_size, -5.5), pline_y], cam, 0.06)

def drawScene(cam, mirage, floor, obstacles, powerups, luna, dt, score, num_shields,
              poem_index, poem_line, current_palette, palette_change_str):
    
    global speed_time_remaining, last_num_shields, shield_hexagon_step, last_poem_line, poem_line_countdown
    speed_time_remaining = mirage.boost_remaining
    if num_shields < last_num_shields:
        shield_hexagon_step = 300

    last_num_shields = num_shields

    if not last_poem_line == poem_line:
        poem_line_countdown = 10
        last_poem_line = poem_line
    
    comblist = obstacles + powerups
    comblist.sort(key=lambda x: mag([-x.pos.x - cam.pos.x, -x.pos.y - cam.pos.y, -x.pos.z - cam.pos.z]), reverse=True)

    drawLuna(luna, cam, current_palette)
    drawLine2D(-35, 0, 35, 0, floor.color, cam) # draw a horizon
    drawGround(floor, mirage, dt)
    drawObstaclesAndPowerups(comblist, current_palette)
    drawMirage(mirage, current_palette)
    drawShieldCount(num_shields, score, current_palette)
    drawScoreCounter(-3, 4, cam, score, [1,0,0])
    drawSpeedArrows(cam, current_palette)
    drawShieldHexagon(cam, current_palette)
    drawAgilityArrows(mirage, cam, current_palette)
    if palette_change_str:
        drawPaletteChangeStr(palette_change_str, current_palette, cam)
    drawPoem(poem_index, poem_line, dt, cam)
    #drawOrigin()

