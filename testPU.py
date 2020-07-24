'''
test.py
'''

import multiprocessing
import world
import nodes
import time

import nodes
import world
import constants as cst 



channel_rep=[]

        # Create a new world for this configuration
new_world = world.World(cst.WORLD_SIZE,cst.WORLD_SIZE)
        # Create the nodes

### Complete node list for display
nodes_list = [] 
### Contains all PU users used to do the sensing 
PU_list = []
### Contains all SU
SU_list = []

### add ordinary node
for i in range(cst.NUM_NODES-cst.NUM_PU):
    newN = nodes.Nodes(i,False,new_world)
    SU_list.append(newN)
    nodes_list.append(newN)
### add PU's

for i in range(cst.NUM_NODES-cst.NUM_PU, cst.NUM_NODES):
    newN = nodes.Nodes(i,False,new_world,True)
    PU_list.append(newN) 
    nodes_list.append(newN) 
    

for n in nodes_list :
        n.sense_In_Range_Nodes()
        


import gui

### Creating a GUI to display the node and the annimations
new_GUI = gui.GUI()
new_GUI.open_GUI()
### Setting the world into the GUI
new_GUI.set_World(new_world)
new_GUI.set_Nodes(nodes_list)

### COLOR the PU's
for pu in PU_list:
    pu.set_PU_Color()

calls = SU_list[0].complete_graph_coloring1(None)
new_GUI.color_refresh(nodes_list)



### DISPLAY OF COLORING

print("-----------------------------------")
for n in nodes_list:

    tmp = n.get_used_channel()
    
    n.update_channels(PU_list)
    id_list = []
    for v in n.in_Range_Nodes :
        id_list.append(v.id)


    print (f"Final coloring for node {n.id} {n.coloring}\n Transmission range : {n.transmission_Range}\n Neighbour : {id_list} \n channel usage : {n.free_Channels}\n finished in {calls} calls\n\n" )
    




new_GUI.loop()




