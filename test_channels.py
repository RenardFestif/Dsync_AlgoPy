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


calls = nodes_list[0].complete_graph_coloring1()

new_GUI.color_refresh(nodes_list)

#### Section comptage de lien et de réutilisation
to_remove = []
global_coloring = dict()
for node in nodes_list :
    global_coloring.update(node.coloring)
    
for key in global_coloring.keys():
    if (key[1], key[0]) in to_remove or (key[0], key[1]) in to_remove:
        continue
    to_remove.append(key)

for key in to_remove:
    del global_coloring[key]

global_counting = dict()
for i in range(cst.NUM_CHANNELS):
    global_counting[i] = 0

done = []  
for key, value in global_coloring.items():
    
    
    ### searching for reuse in direct neighbor of key[0]
    for n in nodes_list[key[0]].in_Range_Nodes:
        if n.id == key[1]:
            continue
        for n_key, n_value in n.coloring.items():
            if ((value == n_value) and (not(n_key in done))):
                if nodes_list[key[0]].is_in_range(nodes_list[n_key[0]]) and nodes_list[key[0]].is_in_range(nodes_list[n_key[1]]) :
                    global_counting[value] += 1
                    done.append(n_key)
                    done.append((n_key[1],n_key[0]))
                    done.append(key)
                    done.append((key[1],key[0]))
                
        
    ### searching for reuse in direct neighbor of key[1]
    for n in nodes_list[key[1]].in_Range_Nodes:
        if n.id == key[0]:
            continue
        for n_key, n_value in n.coloring.items():
            if value == n_value and (not(n_key in done)):
                if nodes_list[key[1]].is_in_range(nodes_list[n_key[0]]) and nodes_list[key[1]].is_in_range(nodes_list[n_key[1]]):

                    global_counting[value] += 1
                    done.append(n_key)
                    done.append((n_key[1],n_key[0]))
                    done.append(key)
                    done.append((key[1],key[0]))


print (global_counting)


### DISPLAY OF COLORING

print("-----------------------------------")
for n in nodes_list:

    tmp = n.get_used_channel()
    
    
    id_list = []
    for v in n.in_Range_Nodes :
        id_list.append(v.id)


    print (f"Final coloring for node {n.id} {n.coloring}\n Transmission range : {n.transmission_Range}\n Neighbour : {id_list} \n\n" )
    




new_GUI.loop()




