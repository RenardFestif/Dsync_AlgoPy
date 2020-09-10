'''
world.py
'''
class World : 
    def __init__(self, x, y):
        self.size_X = x
        self.size_Y = y
        self.world = [[0 for j in range(y)] for i in range(x)] 
        for i in range (x):
            for j in range (y):
                self.world[i][j] = Case()
        
    
    def print_World(self):
        for i in range (self.size_X):
            for j in range (self.size_Y):
                print(self.world[i][j].is_Occupied)
            print('\n')
    

    '''
    Get the Case at position [x][y] 
    '''
    def get_Case(self,x,y):
        return self.world[x][y]     

    '''
    Getters on Attributes
    '''  
    def get_X(self):
        return self.size_X
    def get_Y(self):
        return self.get_Y  

    def reset(self):
        for i in range (self.size_X):
            for j in range (self.size_Y):
                self.world[i][j] = Case()
            


    


class Case : 

    def __init__(self):
        self.is_Occupied = False
        self.node = None

    def get_Node (self):
        return self.node