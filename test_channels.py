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

   
new_world = world.World(cst.WORLD_SIZE,cst.WORLD_SIZE)

nodes_list = []
PU_list = []
SU_list = []
### SU
for i in range(cst.NUM_NODES-cst.NUM_PU):
    newN = nodes.Nodes(i,False,new_world, False)
    nodes_list.append(newN)
    SU_list.append(newN)
### PU
for i in range(cst.NUM_NODES-cst.NUM_PU, cst.NUM_NODES):
    newN = nodes.Nodes(i,False,new_world, True)
    nodes_list.append(newN)
    PU_list.append(newN)

for n in nodes_list :
        n.sense_In_Range_Nodes()

for pu in PU_list:
    pu.set_PU_Color()



import gui

### Creating a GUI to display the node and the annimations
new_GUI = gui.GUI()
new_GUI.open_GUI()
### Setting the world into the GUI
new_GUI.set_World(new_world)
new_GUI.set_Nodes(nodes_list)


calls = SU_list[0].complete_graph_coloring3(PU_list)

new_GUI.color_refresh(nodes_list)

#### Section comptage de lien et de réutilisation
to_remove = []
global_coloring = dict()
for node in SU_list :
    global_coloring.update(node.coloring)
    
for key in global_coloring.keys():
    if (key[1], key[0]) in to_remove or (key[0], key[1]) in to_remove or nodes_list[key[1]] in PU_list:
        continue
    to_remove.append(key)

for key in to_remove:
    del global_coloring[key]

global_counting = dict()
for i in range(cst.NUM_CHANNELS):
    global_counting[i] = 0

done = []  
for key, value in global_coloring.items():
    
    ### checking that the neighbor is not a PU self cannot be one since the dict is made out of the SU_list
    if (nodes_list[key[1]] in PU_list):
        continue
    ### searching for reuse in direct neighbor of key[0]
    for n in SU_list[key[0]].in_Range_Nodes:
        if n.id == key[1] or n in PU_list: 
            continue
        for n_key, n_value in n.coloring.items():
            if nodes_list[n_key[1]] in PU_list :
                continue
            if ((value == n_value) and (not(n_key in done))):
                
                if SU_list[key[0]].is_in_range(SU_list[n_key[0]]) and SU_list[key[0]].is_in_range(SU_list[n_key[1]]) :
                    global_counting[value] += 1
                    done.append(n_key)
                    done.append((n_key[1],n_key[0]))
                    done.append(key)
                    done.append((key[1],key[0]))
                
        
    ### searching for reuse in direct neighbor of key[1]
    for n in SU_list[key[1]].in_Range_Nodes:
        if n.id == key[0] or n in PU_list:
            continue
        for n_key, n_value in n.coloring.items():
            if nodes_list[n_key[1]] in PU_list :
                continue
            if value == n_value and (not(n_key in done)):
                
                if SU_list[key[1]].is_in_range(SU_list[n_key[0]]) and SU_list[key[1]].is_in_range(SU_list[n_key[1]]):

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




