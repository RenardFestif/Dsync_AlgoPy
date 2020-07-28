'''
test.py
'''
import concurrent.futures

import world
import nodes
import time

import multiprocessing

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

### non concurrent 
#calls = nodes_list[0].complete_graph_coloring2()
#calls1 =nodes_list[1].complete_graph_coloring2()
#summ = calls + calls1


### Concurent 

with concurrent.futures.ProcessPoolExecutor() as executor:
    f1 = executor.submit(nodes_list[0].complete_graph_coloring1)
    f2 = executor.submit(nodes_list[1].complete_graph_coloring1)
    calls = f1.result()
    calls1 = f2.result()
    
summ = calls + calls1
new_GUI.color_refresh(nodes_list)

sum_tmp = 0
usage = dict()
for i in range (cst.NUM_CHANNELS) : 
    usage[i] =  0
for node in nodes_list:

    tmp = node.get_used_channel()

    
    for i in tmp.values():
        
        if i == 0 or i == 1.0:
            continue
        else :
            sum_tmp += i-1


### DISPLAY OF COLORING

print("-----------------------------------")
for n in nodes_list:

    tmp = n.get_used_channel()
    
    
    id_list = []
    for v in n.in_Range_Nodes :
        id_list.append(v.id)


    print (f"Final coloring for node {n.id} {n.coloring} completed in {calls} and {calls1} sum is equal to {summ} calls\n Transmission range : {n.transmission_Range}\n Neighbour : {id_list} \n channel usage : {n.free_Channels} \n channel usage in the range of {n.id}: {tmp.values()} \n re-utilisation = {sum_tmp} \n\n" )
    




new_GUI.loop()




