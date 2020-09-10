'''
nodes.py

'''

import constants as cst
import random
import world
import math

class Nodes:
    def __init__(self,id,is_Master,world,isPU=False, isChanRandom=True):
        self.id = id
        self.pos_X = 0
        self.pos_Y = 0

        ### Se referer à un fichier pour l'activité des PU
        self.isPU = isPU
        self.isPUOnline = True
        self.PU_channel = None

        ### Used to determine all the one hop neighbor
        self.transmission_Range = 0

        ### Here we make the difference between Master nodes and Reference nodes
        self.got_Time = is_Master
        self.is_Master = is_Master

        self.world = world

        self.randomChan_enabled = isChanRandom
        self.randomChan = dict()
        ### free channel key = channel value = amount of local usage of that color
        self.free_Channels = self.init_free_Channels()
        self.in_Range_Nodes = []


        ### Dictionnaire coloring {key = channel, val = voisin}
        self.coloring = dict()

        self.set_Positions()

        self.set_transmission_Range()




    def set_Positions_man(self, x, y):

        self.pos_X = x
        self.pos_Y = y

        self.world.get_Case(self.pos_X, self.pos_Y).is_Occupied = True
        self.world.get_Case(self.pos_X, self.pos_Y).node = self


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
        
        chan = dict()
        if self.randomChan_enabled:
            if len(self.randomChan) == 0:

                for i in range(cst.NUM_CHANNELS):
                    YesOrNo = random.choice([True,False])
                    if YesOrNo:
                        self.randomChan[i]=0
            chan = self.randomChan

        else :
            for i in range(cst.NUM_CHANNELS):
                chan[i]=0
        return chan


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
                    if (tmp_case.node.is_in_range(self)) :
                        self.in_Range_Nodes.append(tmp_case.get_Node())



    def sense_free_channels(self, list_PU=None):

        if list_PU == None or len(list_PU) == 0:
            return self.randomChan
        free_channels = dict()
        chan_to_remove = []

        for pu in list_PU:
            if pu.isPUOnline and self.is_in_range(pu) and pu.PU_channel != None:
                chan_to_remove.append(pu.PU_channel)
            ### check indirect neighbour
            for n in self.in_Range_Nodes :
                if n.is_in_range(pu):
                    chan_to_remove.append(pu.PU_channel)

        if self.randomChan_enabled:
            free_channels = self.randomChan
            for i in chan_to_remove:
                if i in free_channels.keys() :
                    del free_channels[i]
        else :
            for i in range(cst.NUM_CHANNELS):
                if i in chan_to_remove:
                    continue
                else:
                    free_channels[i] = 0

        
        return free_channels


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


    def  update_channels(self, list_PU=None):
        '''
        Indicates the usage degree of each color at a node
        '''

        ret = self.sense_free_channels(list_PU)

        

        # ### Channel used indirect neighbors
        # list_duo = []
        # for n in self.in_Range_Nodes :
        #     id_list = []
        #     for v in self.in_Range_Nodes :
        #         id_list.append(v.id)
        #     for chans in n.coloring.keys():
        #             if self.id in chans or chans in list_duo :
        #                 continue
        #             if n.coloring.get(chans) in ret :
        #                 ret[n.coloring.get(chans)] += 1
        #                 list_duo.append((chans[0], chans[1]))
        #                 list_duo.append((chans[1], chans[0]))
        ### Channel used by self
        for color in self.coloring.values():
                if color in ret :
                    ret[color] += 1


        self.free_Channels = {key: value for key, value in sorted(ret.items(), key=lambda item : item[1])}


    def get_used_channel(self) :
        ret = dict()
        for i in range(cst.NUM_CHANNELS):
            ret[i] = 0


        already_counted = []
        ### Channel used with direct neighbours and indirect
        for n in self.in_Range_Nodes :
            id_list = []
            for v in self.in_Range_Nodes :
                id_list.append(v.id)
            for chans in n.coloring.keys():

                    if (chans[0] in id_list and chans[1] in id_list and not((chans[0], chans[1] ) in already_counted)):
                        ret[n.coloring.get(chans)] += 1
                        already_counted.append((chans[0], chans[1]))
                        already_counted.append((chans[1], chans[0]))
        ### Channel used by self
        for color in self.coloring.values():
                ret[color] += 1


        return (ret)

    def check_links(self, node_liste):
        '''
        This Function checks if a link is broken
        '''

        key_to_remove = []
        for key in self.coloring.keys():
            neighbour_key = key[1]
            neighbour_node = node_liste[neighbour_key]
            ### checking that we are in range of that node
            if self.is_in_range(neighbour_node) and neighbour_node.is_in_range(self):
                continue
            else :
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

    def get_forbidden_channels(self):
        '''
        return a list of forbiden channel to use by self since some PU are within two hops emmiting
        '''
        forbidden_chan = []
        # 1hop
        for n in self.in_Range_Nodes:
            if n.isPU and n.isPUOnline:
                # Avoid redundency
                if n.PU_channel in forbidden_chan:
                    continue
                forbidden_chan.append(n.PU_channel)
            #2hop
            for nn in n.in_Range_Nodes:
                if nn.isPU and nn.isPUOnline:
                    if nn.PU_channel in forbidden_chan:
                        continue
                    forbidden_chan.append(nn.PU_channel)
        
        return forbidden_chan

    def is_colored(self, node):
        '''
        Return true if all the links of the node are colored
        '''
        for n in node.in_Range_Nodes :
            if not ((node.id, n.id) in node.coloring.keys()) : 
                return False
        return True

    def get_common_channel(self, node):
        '''
        return a dict with the common channels ordered by the number of use of it
        that are usable between self and the distant node
        '''

        ret = dict()

        self_forbidden_chan = self.get_forbidden_channels()
        neighbor_forbidden_chan = node.get_forbidden_channels()

        self_free_chan = self.randomChan
        neighbor_free_chan = node.randomChan

        # Remove Forbidden chan
        to_remove = []
        for key  in self_free_chan.keys():
            if key in self_forbidden_chan or key in neighbor_forbidden_chan:
                to_remove.append(key)
        
        for rem in to_remove:
            del self_free_chan[rem]
        
        to_remove = []
        for key  in neighbor_free_chan.keys():
            if key in self_forbidden_chan or key in neighbor_forbidden_chan:
                to_remove.append(key)
        
        for rem in to_remove:
            del neighbor_free_chan[rem]

        # common channel
        for key in neighbor_free_chan.keys():
            if key in self_free_chan.keys():
                ret[key] = 0
        
        ret = self.count_usage_common_channel(ret)
        ret = {key: value for key, value in sorted(ret.items(), key=lambda item : item[1])}
        return ret


    def count_usage_common_channel(self, common):
        ret = common
        done = []
        for key, value in self.coloring.items():
            if not key in done:
                if value in ret:
                    ret[value]+=1
                    done.append(key)
                    done.append((key[1],key[0]))
        for n in self.in_Range_Nodes:
            for key, value in n.coloring.items():
                if not key in done:
                    if value in ret:
                        ret[value]+=1
                        done.append(key)
                        done.append((key[1],key[0]))

        return ret






#################################################################################################################
### Function related to PU's
    def set_PU_Color(self):
        if not self.isPUOnline:
            return

        if self.PU_channel == None:
            rand_chan = random.randint(0,cst.NUM_CHANNELS-1)
            self.PU_channel = rand_chan

        for n in self.in_Range_Nodes:
            self.coloring[self.id, n.id]=self.PU_channel
            n.coloring[n.id, self.id] = self.PU_channel

#################################################################################################################
### Graph coloring algorithm
### 1 => Distributed DSature
### 2 => Easy coloring
### 3 => Random Coloring
    def complete_graph_coloring1(self, list_PU=None, calls=0):
        '''
        This function initiate the coloring
        '''
        if self.isPU:
            return calls

        calls = calls + 1

        to_color = []

        ### if no neighbor we skip
        if len(self.in_Range_Nodes)==0:
            #print("The node",self.id,'has no neighbour')
            return calls
        
       
        ### sort the sensed nodes according to the number of free channel
        self.in_Range_Nodes.sort(key=saturation_Degre_Compare, reverse=False)
        

        for neighbor_node in self.in_Range_Nodes:

            ### Nodes that have less free channels are prioritary
            if (len(neighbor_node.randomChan) < len(self.randomChan)):

                ### First check that the link is not already assigned if it is we just copy the color inside the nodes dictionary
                if (((self.id, neighbor_node.id) in self.coloring.keys()) and  len(self.coloring)>0 ):
                    #print(self.id, "color allocated", neighbor_node.coloring.get((neighbor_node.id, self.id)))
                    continue

                ### Otherwise since the node is prioritary we let him find the color of his neighbour then we know for sure
                ### that he had computed the color for the link with the current node so we do copy in inside the dictionnary
                ### Only if they have a common channel
                
                common_chan = self.get_common_channel(neighbor_node)
                if len(common_chan) > 0:
                    calls = neighbor_node.complete_graph_coloring1(list_PU, calls)


            
            else:

                ### First check that the link is not already assigned if it is we just copy the color inside the nodes dictionary and we pass
                ### since we know for sure that the "smaller" have completed their graph

                if (((self.id, neighbor_node.id) in self.coloring.keys()) and  len(self.coloring)>0):
                    #print( self.id, "color allocated", neighbor_node.coloring.get((neighbor_node.id, self.id)))

                    continue

                ### Common channel between self and neighbor
                self.update_channels(list_PU)
                neighbor_node.update_channels(list_PU)
                
                common_chan = self.get_common_channel(neighbor_node)
                
                ### If there is no common channel we just pass and put the equal node inside a to_color list
                if (len(common_chan)>0):
                    
                ### Else we assigne the common channel and put the equal node in the list
                ### use the less used

                # key_list = [k for (k, val) in tmp_chan.items() if val == 0]
                # iterator = 0
                # while (len (key_list)== 0):
                #     iterator += 1
                #     key_list = [k for (k, val) in tmp_chan.items() if val == iterator]  

                    color = list(common_chan.keys())[0]           

                    #color one way
                    self.coloring[self.id,neighbor_node.id] = color
                    #and the other
                    neighbor_node.coloring[neighbor_node.id, self.id] = color
                    to_color.append(neighbor_node)

        ### The only thing left to do is to to execute the function on the equal and higher nodes
        for n in to_color :
            calls = n.complete_graph_coloring1(list_PU, calls)
        return calls


    def complete_graph_coloring2(self, list_PU=None, calls=0):

        if self.isPU:
            return calls

        ### check that every color has been colored
        # length = 0
        # for n in self.in_Range_Nodes:
        #     if (self.id,n.id) in self.coloring.keys():
        #         length += 1
        # if length == len(self.in_Range_Nodes):
        #     return calls +1


        calls += 1
        if self.is_colored(self):
            return calls
        to_color = []

        ### set a color for each links of self
        for n in self.in_Range_Nodes:

            ### check that the link isn't already colored
            if (((n.id, self.id) in n.coloring.keys()) and  len(n.coloring)>0):
                #check that every link of the neighbor is colored other wise add it to to_color
                if self.is_colored(n):
                    continue
                    

            else :

                ### First check that the link is not already assigned if it is we just copy the color inside the nodes dictionary and we pass
                
                self.update_channels(list_PU)
                n.update_channels(list_PU)   

                common_chan = self.get_common_channel(n)
                # tmp_chan = self.free_Channels
                # for chan, value in n.free_Channels.items():
                #     if not(chan in self.free_Channels.keys()):
                #         continue
                #     if value <= self.free_Channels[chan]:
                #         continue
                #     tmp_chan[chan] += value
                # ### Common channel between self and neighbor
                # to_remove = []
                # for chan in self.free_Channels.keys():
                #     if not(chan in n.free_Channels.keys()):
                #         to_remove.append(chan)
                # for rem in to_remove:
                #     del tmp_chan[rem]

                
                
                ### If there is no common channel we just pass and put the equal node inside a to_color list
                if (len(common_chan)==0):
                    continue

                

                # key_list = [k for (k, val) in tmp_chan.items() if val == 0]
                # iterator = 0
                # while (len (key_list)== 0):
                #     iterator += 1
                #     key_list = [k for (k, val) in tmp_chan.items() if val == iterator]
                
                
                color = list(common_chan.keys())[0]    
                ### Coloring one way
                self.coloring[self.id,n.id] = color
                ### And the other
                n.coloring[n.id, self.id] = color

                to_color.append(n)


        for n in to_color :
            calls = n.complete_graph_coloring2(list_PU, calls)

        return calls



    def complete_graph_coloring3(self, list_PU=None, calls=0):
        ### 1st step Compute the MIS ( Maximal Independent Set )
        # MIS = self.get_MIS()

        ### check that every color has been colored
        length = 0
        for n in self.in_Range_Nodes:
            if (self.id,n.id) in self.coloring.keys():
                length += 1
        if length == len(self.in_Range_Nodes):
            return calls +1

        calls += 1
        to_color = []


        ### set a color for each links of self
        for node in self.in_Range_Nodes:

            ### check that the link isn't already colored
            if (((node.id, self.id) in node.coloring.keys()) and  len(node.coloring)>0):
                continue

            else :
                # print("checking channel used in the the range of the neighbour")
                self.update_channels(list_PU)
                node.update_channels(list_PU)

                common_chan = self.get_common_channel(node)
                ### First check that the link is not already assigned if it is we just copy the color inside the nodes dictionary and we pass
                ### since we know for sure that the "smaller" have completed their graph

                if (((self.id, node.id) in self.coloring.keys()) and  len(self.coloring)>0):
                    #print( self.id, "color allocated", neighbor_node.coloring.get((neighbor_node.id, self.id)))

                    continue

                ### Common channel between self and neighbor
                # to_remove = []
                # for chan in self.free_Channels.keys():
                #     if not(chan in self.free_Channels):
                #         continue
                #     if not(chan in node.free_Channels.keys()):
                #         to_remove.append(chan)
                # for rem in to_remove:
                #     del tmp_chan[rem]

                ### If there is no common channel we just pass and put the equal node inside a to_color list
                if (len(common_chan)==0):
                    #print("There is no common channel between", self.id,"and", neighbor_node.id,"/ The connection cannot be established")
                    #to_color.append(neighbor_node)

                    continue

                chann_list =list(common_chan.keys())
                chan_choice = random.choice(chann_list)
                self.coloring[self.id,node.id] = chan_choice
                node.coloring[node.id, self.id] = chan_choice

                self.update_channels()
                to_color.append(node)


        for node in to_color :
            calls = node.complete_graph_coloring3(list_PU, calls)



        return calls










def  saturation_Degre_Compare (Nodes):
    return len(Nodes.randomChan)

def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3



