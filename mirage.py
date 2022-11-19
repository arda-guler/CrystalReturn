import pywavefront
import math

from math_utils import *

class mirage:
    def __init__(self, model, speed, height=0, color=[1,0,0]):

        model_full_path = "data/models/" + model + ".obj"
        
        self.model = pywavefront.Wavefront(model_full_path, collect_faces=True)
        self.speed = speed
        self.original_speed = speed
        self.boost_speed = speed * 2
        self.height = height
        self.color = color
        self.bank = 0
        self.bankspeed = 57

        self.max_bank = 25
        self.accel = 50
        self.decel = 30

        self.boost_remaining = 0
        self.shields_remaining = 0
        self.agility_remaining = 0

    def get_color(self):
        return self.color

    def update_speed(self, dt):

        # slower than normal, accelerate
        if self.speed < self.original_speed - 0.2 and abs(self.bank) < self.max_bank:
            self.speed += self.accel * dt

        # exact match to original speed
        if self.boost_remaining == 0 and abs(self.speed - self.original_speed) < 0.2 and abs(self.bank) < self.max_bank:
            self.speed = self.original_speed

        # boost ended, slow down
        if self.boost_remaining == 0 and self.speed > self.original_speed:
            self.speed -= self.decel * dt

        # boost active, speed up
        if self.boost_remaining > 0 and self.speed < self.boost_speed:
            self.speed += self.accel * dt

        # boost active, exact match to boost speed
        if self.boost_remaining > 0 and self.speed > self.boost_speed:
            self.speed = self.boost_speed

        if self.boost_remaining > 0:
            self.boost_remaining -= dt

        if self.boost_remaining < 0:
            self.boost_remaining = 0

        if abs(self.bank) >= self.max_bank and self.speed > (self.original_speed/2):
            self.speed -= self.decel/5 * dt

    def update_bank(self, bank_cmd, dt):
        
        if self.agility_remaining > 0:
            self.agility_remaining -= dt

        if self.agility_remaining < 0:
            self.agility_remaining = 0
        
        if self.bank == 0 and bank_cmd == 0:
            return

        else:
            if bank_cmd == 0:
                
                self.bank += -sign(self.bank) * self.bankspeed * (27/42) * dt
                
                if abs(self.bank) < 0.5:
                    self.bank = 0

            elif bank_cmd == 1:
                if not self.bank >= self.max_bank:
                    self.bank += self.bankspeed * dt

                    if self.bank > self.max_bank:
                        self.bank = self.max_bank

            elif bank_cmd == -1:
                if not self.bank <= -self.max_bank:
                    self.bank -= self.bankspeed * dt

                    if self.bank < -self.max_bank:
                        self.bank = -self.max_bank

    def get_side_speed(self, dt):
        if self.agility_remaining and self.agility_remaining > 24:
            return (71 + ((117 - 71) * (25 - self.agility_remaining))) * math.radians(self.bank) * dt
        elif self.agility_remaining and self.agility_remaining < 1:
            return (71 + ((117 - 71) * (self.agility_remaining))) * math.radians(self.bank) * dt
        elif self.agility_remaining:
            return 117 * math.radians(self.bank) * dt
        else:
            return 71 * math.radians(self.bank) * dt

    def set_color(self, new_color):
        self.color = new_color

