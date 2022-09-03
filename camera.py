import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from math_utils import *
from vector3 import *

class camera():
    def __init__(self, name, pos, orient, active):
        self.name = name
        self.pos = pos
        self.orient = orient
        self.active = active
        
    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos

    def set_pos(self, new_pos):
        req_trans = new_pos - self.pos
        glTranslate(req_trans.x, req_trans.y, req_trans.z)
        self.pos = new_pos

    def move(self, movement):
        
        glTranslate((movement.x * self.orient[0][0]) + (movement.y * self.orient[1][0]) + (movement.z * self.orient[2][0]),
                    (movement.x * self.orient[0][1]) + (movement.y * self.orient[1][1]) + (movement.z * self.orient[2][1]),
                    (movement.x * self.orient[0][2]) + (movement.y * self.orient[1][2]) + (movement.z * self.orient[2][2]))
        
        self.pos = vec3(self.pos.x + (movement.x * self.orient[0][0]) + (movement.y * self.orient[1][0]) + (movement.z * self.orient[2][0]),
                        self.pos.y + (movement.x * self.orient[0][1]) + (movement.y * self.orient[1][1]) + (movement.z * self.orient[2][1]),
                        self.pos.z + (movement.x * self.orient[0][2]) + (movement.y * self.orient[1][2]) + (movement.z * self.orient[2][2]))

    def get_orient(self):
        return self.orient
    
    def get_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def rotate(self, rotation):

        about_pos = self.pos
        
        glTranslate(-about_pos.x, -about_pos.y, -about_pos.z)
        glRotate(-rotation.x, self.orient[0][0], self.orient[0][1], self.orient[0][2])
        glTranslate(about_pos.x, about_pos.y, about_pos.z)

        glTranslate(-about_pos.x, -about_pos.y, -about_pos.z)
        glRotate(-rotation.y, self.orient[1][0], self.orient[1][1], self.orient[1][2])
        glTranslate(about_pos.x, about_pos.y, about_pos.z)

        glTranslate(-about_pos.x, -about_pos.y, -about_pos.z)
        glRotate(-rotation.z, self.orient[2][0], self.orient[2][1], self.orient[2][2])
        glTranslate(about_pos.x, about_pos.y, about_pos.z)

        self.orient = rotate_matrix(self.orient, rotation)
