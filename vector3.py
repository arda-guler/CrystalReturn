class vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, val):
        return vec3(self.x * val, self.y * val, self.z * val)

    def __truediv__(self, val):
        return vec3(self.x / val, self.y / val, self.z / val)

    def mag(self):
        return (self.x**2 + self.y**2 + self.z**2)**(0.5)

    def cross(self, other):
        return vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def dot(self, other):
        return vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def normalized(self):
        m = self.mag()
        if not m == 0:
            return vec3(self.x/m, self.y/m, self.z/m)
        else:
            return vec3(0,0,0)
