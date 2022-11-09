import pywavefront

class powerup:
    def check_collision(self):
        if ((self.pos.x + self.size.x > 0 and self.pos.x - self.size.x < 0) and
            (self.pos.y + self.size.y > 0 and self.pos.y - self.size.y < 0) and
            (self.pos.z + self.size.z > 0 and self.pos.z - self.size.z < 0)):
            return True

        else:
            return False

    def update_pos(self, mirage, dt):
        self.pos.z += mirage.speed * dt
        self.pos.x -= mirage.get_side_speed(dt)

    def set_color(self, new_color):
        self.color = new_color

class speed_boost(powerup):
    def __init__(self, pos, size, model, color=[0, 0.8, 0]):
        self.model = model
        self.pos = pos
        self.rot = False
        self.size = size
        self.color = color

        self.powerup_type = "speed_boost"

class invulnerability(powerup):
    def __init__(self, pos, size, model, color=[1,0,1]):
        self.model = model
        self.pos = pos
        self.rot = False
        self.size = size
        self.color = color

        self.powerup_type = "invulnerability"

class agility(powerup):
    def __init__(self, pos, size, model, color=[0.8,0.8,0]):
        self.model = model
        self.pos = pos
        self.rot = False
        self.size = size
        self.color = color

        self.powerup_type = "agility"
        
