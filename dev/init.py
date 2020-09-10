'''
init.py
Entry point of the algorithm
'''

import constants as cst


'''
Phase 1 : Initialisation and making of the conflict graph
'''
### Generate a world
import world

new_world = world.World(4, 4)

### Generation of all the nodes and master nodes inside nodes_list
import nodes

nodes_list = []
num_master = cst.NUM_MASTER_NODES

for x in range (cst.NUM_NODES):
    if (num_master > 0):
        newN = nodes.Nodes(x,True,new_world)
        nodes_list.append(newN)
        num_master = num_master-1
        continue
    newN = nodes.Nodes(x,False,new_world)
    nodes_list.append(newN)

### Scouting for neighbor
# for n in nodes_list:
#     n.sense_In_Range_Nodes()

import gui
import time

### Creating a GUI to display the node and the annimations
new_GUI = gui.GUI()
new_GUI.open_GUI()
### Setting the world into the GUI
new_GUI.set_World(new_world)
new_GUI.set_Nodes(nodes_list)

# for n in nodes_list:
#     print ("id :", n.id, "range :", n.transmission_Range)

### Test for display
for i in range(500):
    time.sleep(cst.REFRESH)
    for n in nodes_list:
        n.random_Move()
        n.check_links(nodes_list)
        new_GUI.refresh(nodes_list)

    print(nodes_list[0].complete_graph_coloring1(0))
    new_GUI.color_node(n, nodes_list)


# found = False
# while (found == False):

# tmp = nodes_list[0].complete_graph_coloring1(0)
# print("Recur 1 :",tmp)
# nodes_list[0].random_Move()
# tmp = nodes_list[0].complete_graph_coloring1(0)
# print("recur 2 : ",tmp)
# new_GUI.color_refresh(nodes_list)

    # for n in nodes_list :
    #     for col in n.coloring.values():
    #         if col == None :
    #             found = True
    #             print ("Found")






# print("-----------------------------------")
# for n in nodes_list:
#     id_list = []
#     for v in n.in_Range_Nodes :
#         id_list.append(v.id)
#     print (f"Final coloring for node {n.id} {n.coloring}\n Transmission range : {n.transmission_Range}\n Neighbour : {id_list} \n\n" )




### Reference static graph avec 1 master node
#  import time

# start = time.perf_counter()
# nodes_list[0].complete_graph_coloring1()
# finish = time.perf_counter()
# print(finish-start)

# new_GUI.color_refresh( nodes_list)




# Etudié le temps requis avant un changement de topologie
# essayer de deduire des formules mathematiques

### FIRST IDEA :
# each time a node moves he starts a complete graph recoloring

### SECOND IDEA
# if a moving node get is getting out of the transmission rang he initiate a complete graph recoloring

### THIRD IDEA
# Local graph recoloring each time a node moves

### FOURTH IDEA
# Local graph  recoloring when a nodes gets out of range

### Introduction of PU


new_GUI.loop()

