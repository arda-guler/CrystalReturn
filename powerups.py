import pywavefront

class speed_boost:
    def __init__(self, pos, size, model="powerup"):

        model_full_path = "data/models/" + model + ".obj"

        self.model = pywavefront.Wavefront(model_full_path, collect_faces=True)
        self.pos = pos
        self.size = size
        self.color = [0, 0.8, 0]

        self.powerup_type = "speed_boost"

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

class invulnerability:
    def __init__(self, pos, size, model="shield"):

        model_full_path = "data/models/" + model + ".obj"

        self.model = pywavefront.Wavefront(model_full_path, collect_faces=True)
        self.pos = pos
        self.size = size
        self.color = [1, 0, 1]

        self.powerup_type = "invulnerability"

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
        
