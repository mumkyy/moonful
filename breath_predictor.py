import math

class User:

    def __init__(self,state):
        self.state = state

    def get_state(self):
        #self.state = gs()
        return self.r_state()
    
    def r_state(self):
        return self.state

    def suggest(self,btech):
        btechs = ['Pursed lip breathing',
                'Diaphragmatic breathing'
                'Focus breathing'
                'Lion breathing'
                'Alternate nostril breathing'
                'Equal breathing'
                'Resonanant breathing'
                'Sitali breathing'
                'Deep breathing'
                'Bhramari breathing']
        
        ostate = [1,1,10,1,4,1,1,1,1,10]
        nstate = self.get_state()
        reward = 5.0-0.36*(abs(math.dist(nstate,ostate)))
        return reward, 0

    def save(self):
        pass
