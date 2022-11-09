class terrain:
    def __init__(self, color=[0.2,0.6,1], height=0):
        self.color = color
        self.height = height

    def set_color(self, new_color):
        self.color = new_color
