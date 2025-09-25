import random
import os

class Rabbit(object):
    MIN_STAY = 20
    MAX_STAY = 60
    WARPFOLDER = ".warprabbit"
    def __init__(self, attribute_id, card):
        self.card = card
        self.attribute_id = attribute_id
        fname = ".countdown_"+str(self.card.id)
        self.fname = os.path.join(self.WARPFOLDER,fname)
        os.makedirs(self.WARPFOLDER,exist_ok=True)

    def warp(self,card):
        self.kill()
        
        # warp the rabbit to another location
        self.card = card
        self.card.add_attribute(self.attribute_id)
   
    def is_ready_to_warp(self):
        return self.warp_counter() <= 0

    def warp_counter(self):
        # if there is a countdown file, then read it
        if os.path.isfile(self.fname):
            with open(self.fname) as f:
                countdown = int(f.read())
        else:
            countdown = random.randint(self.MIN_STAY,self.MAX_STAY)
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
        self.card.remove_attribute(self.attribute_id)
