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
nodes_list = [] 
for i in range(cst.NUM_NODES):
    newN = nodes.Nodes(i,False,new_world)
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



nodes_list[0].complete_graph_coloring2()
new_GUI.color_refresh(nodes_list)


### DISPLAY OF COLORING

print("-----------------------------------")
for n in nodes_list:

    tmp = n.get_used_channel()
    
    
    id_list = []
    for v in n.in_Range_Nodes :
        id_list.append(v.id)


    print (f"Final coloring for node {n.id} {n.coloring}\n Transmission range : {n.transmission_Range}\n Neighbour : {id_list} \n channel usage : {n.free_Channels} \n channel usage in the range of {n.id}: {tmp.values()} \n\n" )
    




new_GUI.loop()




