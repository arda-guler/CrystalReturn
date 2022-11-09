class Luna:
    def __init__(self, height, color=[0.8, 0.8, 0.8]):
        self.height = height
        self.color = color

    def update_height(self, speed, dt):
        self.height -= (150 - speed) * dt * 0.05

    def set_color(self, new_color):
        self.color = new_color
