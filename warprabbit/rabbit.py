import random
import os

class Rabbit(object):
    def __init__(self, config, card):
        self.card = card
        fname = ".countdown_"+str(self.card.id)
        self.config = config
        self.fname = os.path.join(self.config["data_folder"],fname)

    def warp(self,card):
        self.kill()
        
        # warp the rabbit to another location
        self.card = card
        self.card.add_attribute(self.config["rabbit_id"],1)
   
    def is_ready_to_warp(self):
        return self.warp_counter() <= 0

    def warp_counter(self):
        # if there is a countdown file, then read it
        if os.path.isfile(self.fname):
            with open(self.fname) as f:
                countdown = int(f.read())
        else:
            countdown = random.randint(self.config["min_stay"],self.config["max_stay"])
            self.set_warp_counter(countdown)
        return countdown

    def set_warp_counter(self,c):
        with open(self.fname,"w") as f:
            f.write(str(c))

    def decrease_counter(self):
        c = self.warp_counter() - 1
        self.set_warp_counter(c)
        return c

    def kill(self):
        # delete countdown file
        if os.path.isfile(self.fname):
            os.remove(self.fname)

        # remove rabbit from card
        self.card.remove_attribute(self.config["rabbit_id"])
