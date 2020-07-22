'''
nodes.py

'''

import constants as cst
import random
import world
import math

class Nodes:
    def __init__(self,id,is_Master,world):
        self.id = id
        self.pos_X = 0
        self.pos_Y = 0

        ### Se referer à un fichier pour l'activité des PU
        self.isPU = False

        ### Used to determine all the one hop neighbor
        self.transmission_Range = 0

        ### Here we make the difference between Master nodes and Reference nodes
        self.got_Time = is_Master
        self.is_Master = is_Master

        self.world = world
        ### free channel key = channel value = amount of local usage of that color
        self.free_Channels = dict()
        self.in_Range_Nodes = []

        ### Dictionnaire coloring {key = channel, val = voisin}
        self.coloring = dict()

        self.set_Positions()
        
        self.set_transmission_Range()
        self.init_free_Channels()




    def set_Positions(self):

        '''
        Positions the nodes inside the world ramdomly
        '''

        max_X = self.world.size_X
        max_Y = self.world.size_Y

        self.pos_X = random.randrange(max_X)
        self.pos_Y = random.randrange(max_Y)


        while (self.world.get_Case(self.pos_X, self.pos_Y).is_Occupied):

            self.pos_X = random.randrange(max_X)
            self.pos_Y = random.randrange(max_Y)


        self.world.get_Case(self.pos_X, self.pos_Y).is_Occupied = True
        self.world.get_Case(self.pos_X, self.pos_Y).node = self


    def init_free_Channels(self):

        '''
        Sets the freeChannels 
        '''
        for i in range(cst.NUM_CHANNELS):
            self.free_Channels[i]=0
       

    def set_transmission_Range(self):

        '''
        Sets randomly the transmission range of a node
        Use the MAX_TRANSMISSION_RANGE constants as a maximum value of transmission range

        We also could use a normal distribution
        '''

        self.transmission_Range = random.randrange(1,cst.MAX_TRANSMISSION_RANGE+1)


    def sense_In_Range_Nodes(self):

        '''
        Sense the neighborhood of the node and detects it's direct neighbor (update the in_Range_Neighbor attribute)
        Build the graph
        '''
        ### Reset the variable
        self.in_Range_Nodes.clear()

        for i in range(self.pos_X-self.transmission_Range, self.pos_X+self.transmission_Range+1):
            for j in range(self.pos_Y-self.transmission_Range, self.pos_Y+self.transmission_Range+1):
                ### We check that we don't go over the limit of the world

                if (i<0 or i>=self.world.size_X or j<0 or j>=self.world.size_Y):
                    continue
                ### We skip our position

                if (i==self.pos_X and j==self.pos_Y):
                    continue
                tmp_case = self.world.get_Case(i,j)
                

                if(tmp_case.is_Occupied):

                    ### Finaly check that the node is able to respond, meaning that his range reaches us also
                    min_tmp_x = tmp_case.node.pos_X - tmp_case.node.transmission_Range
                    max_tmp_x = tmp_case.node.pos_X + tmp_case.node.transmission_Range

                    min_tmp_y = tmp_case.node.pos_Y - tmp_case.node.transmission_Range
                    max_tmp_y = tmp_case.node.pos_Y + tmp_case.node.transmission_Range

                    if (self.pos_X in range(min_tmp_x, max_tmp_x+1) and self.pos_Y in range(min_tmp_y, max_tmp_y+1)):
                        self.in_Range_Nodes.append(tmp_case.get_Node())
    

    def random_Move(self):

        '''
        Random One step changing of position of the node
        '''

        moving_possibility = [[-1,0],[-1,-1],[0,-1],[-1,1],[1,0],[1,1],[0,1],[1,-1],[0,0]]
        to_remove = []
        random.seed()

        ### Removing out of bound possibilities
        for d in moving_possibility:

            tmp_X = self.pos_X+d[0]
            tmp_Y = self.pos_Y+d[1]

            if (tmp_X<0 or tmp_X>= self.world.size_X or tmp_Y<0 or tmp_Y>= self.world.size_Y):
                to_remove.append(d)



        for d in to_remove:
            moving_possibility.remove(d)


        displacement = random.choice(moving_possibility)



        ### We check that the next position is not taken already
        while (self.world.get_Case(self.pos_X+displacement[0], self.pos_Y+displacement[1]).is_Occupied ):

            if (displacement == [0,0]):
                return

            moving_possibility.remove(displacement)
            displacement = random.choice(moving_possibility)




        ### Changing the position of the node and setting the booleans

        self.world.get_Case(self.pos_X, self.pos_Y).is_Occupied = False
        self.world.get_Case(self.pos_X+displacement[0], self.pos_Y+displacement[1]).is_Occupied = True

        self.world.get_Case(self.pos_X, self.pos_Y).node = None
        self.world.get_Case(self.pos_X+displacement[0], self.pos_Y+displacement[1]).node = self

        self.pos_X = self.pos_X+displacement[0]
        self.pos_Y = self.pos_Y+displacement[1]


    def update_channels(self, neighbour=None):
        '''
        Indicates the usage degree of each color at a node
        '''

        # if neighbour != None :
        #     for indirect_neighbour in neighbour.in_Range_Nodes :
        #         for key in indirect_neighbour.coloring.keys():
        #             self.free_Channels[indirect_neighbour.coloring.get(key)] += 1
        # else :
        #     for color in self.coloring.values():
        #         self.free_Channels[color] += 1

        ret = dict()
        for i in range(cst.NUM_CHANNELS):
            ret[i] = 0

        ### Channel used with direct neighbours and indirect
        list_duo = []
        for n in self.in_Range_Nodes :
            id_list = []
            for v in self.in_Range_Nodes :
                id_list.append(v.id)
            
            for chans in n.coloring.keys():
                    
                    if (chans[0] in id_list and chans[1] in id_list and chans not in list_duo ): 
                        ret[n.coloring.get(chans)] += 1
                        ### to not count again the link we add the reverted link in list_duo
                        reverse = (chans[1], chans[0])
                        list_duo.append(reverse)
        ### Channel used by self                
        for color in self.coloring.values():
                ret[color] += 1
        
        self.free_Channels = ret
            

        self.free_Channels = {key: value for key, value in sorted(self.free_Channels.items(), key=lambda item : item[1])}
        
    
    def get_used_channel(self) :
        ret = dict()
        for i in range(cst.NUM_CHANNELS):
            ret[i] = 0

        ### Channel used with direct neighbours and indirect
        for n in self.in_Range_Nodes :
            id_list = []
            for v in self.in_Range_Nodes :
                id_list.append(v.id)
            for chans in n.coloring.keys():

                    if (chans[0] in id_list and chans[1] in id_list ): 
                        ret[n.coloring.get(chans)] += 1/2
        ### Channel used by self                
        for color in self.coloring.values():
                ret[color] += 1
        
        
        return ret
            
       


        
#################################################################################################################    
### Graph coloring algorithm 
### 1 => Distributed DSature
### 2 => Easy coloring
    def complete_graph_coloring1(self, calls=0):
        '''
        This function initiate the coloring
        '''

        
        ### Variable used for the Performance analysis
        calls = calls + 1

        #print('calls = ', calls)

        self.coloring.clear()
        to_color = []


        ### we first sens the neighborhood
        self.sense_In_Range_Nodes()
        
        ### if no neighbor we skip
        if len(self.in_Range_Nodes)==0:
            #print("The node",self.id,'has no neighbour')
            return calls


        ### sort the sensed nodes according to the number of free channel
        self.in_Range_Nodes.sort(key=saturation_Degre_Compare, reverse=False)

        ### We retrieve informations from these neighbor such as SNR agree on free channel compute and compare the degree of priority
        ### We imagine a CCC
        for neighbor_node in self.in_Range_Nodes:
            ### First of all we need to know wheter we are prioritary to choose a channel
            ### So we do compare the number of free channel to the one hop neighbor
            ### We can imagine something like a YOU_FIRST message
            ### Here we just check that if we have more channel, all neighbor that have less have compute their coloring
            ### If they have the same amout of available channel We ..... must find a way


            ### Implement SNR comparison
            ### we imagine that the SNR is related to the distance to the nodes
            ### first Compute the relative distance between the two nodes
            ### we use this formula d = sqrt((pow(x2-x1,2)+pow(y2-y1,2)))
            ### Signal power indicates the quality of the signal at a position, the higher the better and the closer (T_range/dist)
            #signal_power = self.transmission_Range/round(math.sqrt((pow(neighbor_node.pos_X-self.pos_X,2)+pow(neighbor_node.pos_Y-self.pos_Y,2))))

            ### Nodes that have less free channels are prioritary 
            if (len(neighbor_node.free_Channels) < len(self.free_Channels)):
                
                ### First check that the link is not already assigned if it is we just copy the color inside the nodes dictionary
                if (((neighbor_node.id, self.id) in neighbor_node.coloring.keys()) and  len(neighbor_node.coloring)>0 ):
                    #print(self.id, "color allocated", neighbor_node.coloring.get((neighbor_node.id, self.id)))
                    self.coloring[self.id, neighbor_node.id] = neighbor_node.coloring.get((neighbor_node.id, self.id))
                    self.update_channels()
                    continue 

                ### Otherwise since the node is prioritary we let him find the color of his neighbour then we know for sure 
                ### that he had computed the color for the link with the current node so we do copy in inside the dictionnary 
                calls = neighbor_node.complete_graph_coloring1(calls)

                self.coloring[self.id, neighbor_node.id] = neighbor_node.coloring.get((neighbor_node.id, self.id))
                self.update_channels()

            ### Other possibility is that the current node have the same amount of available channel than the neighbour
            else:
                 
                ### First check that the link is not already assigned if it is we just copy the color inside the nodes dictionary and we pass
                ### since we know for sure that the "smaller" have completed their graph        
                if (((neighbor_node.id, self.id) in neighbor_node.coloring.keys()) and  len(neighbor_node.coloring)>0):
                    #print( self.id, "color allocated", neighbor_node.coloring.get((neighbor_node.id, self.id)))
                    self.coloring[self.id, neighbor_node.id] = neighbor_node.coloring.get((neighbor_node.id, self.id))
                    self.update_channels()
                    continue               

               

                common_channel = list(set(neighbor_node.free_Channels).intersection(self.free_Channels))
                
                ### If there is no common channel we just pass and put the equal node inside a to_color list
                if (len(common_channel)==0):
                    #print("There is no common channel between", self.id,"and", neighbor_node.id,"/ The connection cannot be established")
                    #to_color.append(neighbor_node)
                    continue
                ### Else we assigne the common channel and put the equal node in the list

                ### use the less used 
                #channel_choice = random.choice(common_channel)

                ### IMPORTANT PART

                key_list = [k for (k, val) in self.free_Channels.items() if val == 0]
                iterator = 0
                while (len (key_list)== 0):
                    iterator += 1
                    key_list = [k for (k, val) in self.free_Channels.items() if val == iterator]

            
                
                self.coloring[self.id,neighbor_node.id] = key_list[0]
                self.update_channels()

                to_color.append(neighbor_node)
           
        ### The only thing left to do is to to execute the function on the equal and higher nodes 
        for n in to_color :            
            calls = n.complete_graph_coloring1(calls)
            
        return calls
    

    def complete_graph_coloring2(self):
        ### 1st step Compute the MIS ( Maximal Independent Set )
        # MIS = self.get_MIS()

        

        to_color = []
       

        ### set a color for each links of self
        for node in self.in_Range_Nodes:
            
            ### check that the link isn't already colored 
            if (((node.id, self.id) in node.coloring.keys()) and  len(node.coloring)>0):
                #print( self.id, "color allocated", neighbor_node.coloring.get((neighbor_node.id, self.id)))
                self.coloring[self.id, node.id] = node.coloring.get((node.id, self.id))
                
                
                continue               

            else :
                # print("checking channel used in the the range of the neighbour")
                self.update_channels()
               
                key_list = [k for (k, val) in self.free_Channels.items() if val == 0]
                iterator = 0
                while (len (key_list)== 0):
                    iterator += 1
                    key_list = [k for (k, val) in self.free_Channels.items() if val == iterator]
                     
                self.coloring[self.id,node.id] = key_list[0]
                
                
                to_color.append(node)
                
        
        for node in to_color : 
            node.complete_graph_coloring2()
                
                
    def complete_graph_coloring3(self):
        ### 1st step Compute the MIS ( Maximal Independent Set )
        # MIS = self.get_MIS()

        

        to_color = []
       

        ### set a color for each links of self
        for node in self.in_Range_Nodes:
            
            ### check that the link isn't already colored 
            if (((node.id, self.id) in node.coloring.keys()) and  len(node.coloring)>0):
                #print( self.id, "color allocated", neighbor_node.coloring.get((neighbor_node.id, self.id)))
                self.coloring[self.id, node.id] = node.coloring.get((node.id, self.id))
                
                self.update_channels()
                continue               

            else :
                # print("checking channel used in the the range of the neighbour")
                

                chann_list = [k for k in self.free_Channels.keys()]
                     
                self.coloring[self.id,node.id] = random.choice(chann_list)
                
                self.update_channels()
                to_color.append(node)
                
        
        for node in to_color : 
            node.complete_graph_coloring2()
                
    def check_links(self, node_liste):

        key_to_remove = []
        for key in self.coloring.keys():
            neighbour_key = key[1]
            neighbour_node = node_liste[neighbour_key]
            ### checking that we are in range of that node 
            if not(self.is_in_range(neighbour_node)):
                key_to_remove.append(key)

        for key in key_to_remove:
            del self.coloring[key]                
       

    def is_in_range(self, dist_node):
        dist_posX = dist_node.pos_X
        dist_posY = dist_node.pos_Y
        dist_range = dist_node.transmission_Range 

        ### Test one way
        if (not(self.pos_X in range(dist_posX-dist_range, dist_posX+dist_range+1) and self.pos_Y in range(dist_posY-dist_range, dist_posY+dist_range+1))):
            
            return False

        ### Test the other way 
        if (not(dist_posX in range (self.pos_X-self.transmission_Range, self.pos_X+self.transmission_Range+1) and dist_posY in range(self.pos_Y-self.transmission_Range, self.pos_Y+self.transmission_Range+1))):
            
            return False
        return True

        
     



               



def  saturation_Degre_Compare (Nodes):
    return len(Nodes.free_Channels)

def intersection(lst1, lst2):  
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3 



