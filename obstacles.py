import pywavefront

from vector3 import *

class rectangular_prism:
    def __init__(self, pos, rot, size, model, color=[0, 0.5, 1]):
        self.model = model
        self.pos = pos
        self.rot = rot
        self.size = size
        self.color = color

    def check_collision(self):
        if ((self.pos.x + self.size.x*2 > 0 and self.pos.x - self.size.x*2 < 0) and
            (self.pos.y + self.size.y*2 > 0 and self.pos.y - self.size.y*2 < 0) and
            (self.pos.z + self.size.z > 0 and self.pos.z - self.size.z < 0)):
            return True

        else:
            return False

    def update_pos(self, mirage, dt):
        self.pos.z += mirage.speed * dt
        self.pos.x -= mirage.get_side_speed(dt)

    def set_color(self, new_color):
        self.color = new_color
