import numpy as np
import time
from agentspace import Agent, space

from pyicubsim import iCubHead

class LookAroundAgent(Agent):

    def __init__(self, namePoints, nameSupress):
        self.namePoints = namePoints
        self.nameSupress = nameSupress
        super().__init__()

    def init(self):
        self.head = iCubHead()
        self.head.set(joint2 = 0.0, joint0 = 0.0, joint1 = 0.0)
        time.sleep(1.0)
        space.attach_trigger(self.namePoints,self)

    def senseSelectAct(self):
    
        if space(default=False)[self.nameSupress]:
            return
    
        points = space[self.namePoints]
        if points is None:
            return
            
        point = points[2]
        if point is None:
            return
        
        x, y = point
        
        head_y, _, head_x = self.head.get()[:3]
        
        reset_x, reset_y = False, False
        if np.abs(head_x) > 40:
            if np.random.rand() > 0.95:
                reset_x = True
        else:
            if np.random.rand() > 0.995:
                reset_x = True
        if head_y > 20: #15
            if np.random.rand() > 0.95:
                reset_y = True
        else:
            if np.abs(head_x) > 5:
                if np.random.rand() > 0.995:
                    reset_y = True
        
        if reset_x:
            delta_degrees_x = -head_x
            #print("RESET X")
        else:
            delta_degrees_x = 2*30*(0.5-x) - head_x
        if reset_y:
            delta_degrees_y = -head_y - 25
            #print("RESET Y")
        else:
            delta_degrees_y = 2*30*(0.5-y) - head_y
        
        angular_speed = 0.04
        limit = 2.0 
        
        if np.abs(delta_degrees_x) > limit:
            self.head.set(joint2 = head_x + delta_degrees_x)
        if np.abs(delta_degrees_y) > limit:
            self.head.set(joint0 = head_y + delta_degrees_y)

        time.sleep(max(np.abs(delta_degrees_x),np.abs(delta_degrees_y))/(1000*angular_speed))
