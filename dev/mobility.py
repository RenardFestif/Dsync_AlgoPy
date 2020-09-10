import preRun
import time 

import nodes
import world
import gui
import util

import constants as cst

def count_channel_reused (node_list):
    #### Section comptage de lien et de réutilisation

    # Elimination des doublons type (1,5) et (5,1)
    to_remove = []
    global_coloring = dict()
    for node in node_list :
        global_coloring.update(node.coloring)
        
    for key in global_coloring.keys():
        if (key[1], key[0]) in to_remove or (key[0], key[1]) in to_remove:
            continue
        to_remove.append(key)

    for key in to_remove:
        del global_coloring[key]

    # Comptage
    global_counting = dict()
    for i in range(cst.NUM_CHANNELS):
        global_counting[i] = 0

    done = []  
    #print(global_coloring)
    for key, value in global_coloring.items():
        
        
        ### searching for reuse of value in direct neighbor of key[0]
        for n in node_list[key[0]].in_Range_Nodes:

            ### we don't count our link
            if n.id == key[1]:
                continue
            for n_key, n_value in n.coloring.items():
                if (n_key) in done:
                    continue
                elif ((value == n_value)):
                   
                    print(n_key)
                    global_counting[value] += 1
                    done.append(n_key)
                    done.append((n_key[1],n_key[0]))
                    done.append(key)
                    done.append((key[1],key[0]))

           
            
                    
            
        ### searching for reuse in direct neighbor of key[1]
        for n in node_list[key[1]].in_Range_Nodes:
            if n.id == key[0]:
                continue
            for n_key, n_value in n.coloring.items():
                if (n_key) in done:
                    
                    continue
                elif value == n_value:
                    
                    global_counting[value] += 1
                    done.append(n_key)
                    done.append((n_key[1],n_key[0]))
                    done.append(key)
                    done.append((key[1],key[0]))
            

    total_reused = 0

    for value in global_counting.values():
        total_reused += value
    
    return total_reused


# 5*5 world 9 nodes Range 1
#    0 1 2 3 4
#   ############
# 0 #    1 2 8 #
# 1 #  0     4 #
# 2 #    3     #
# 3 #  6   7   #      
# 4 #    5     #
#   ############

node_list = []

new_world = world.World(5,5)

for i in range(9):
    newN = nodes.Nodes(i,False, new_world, False, False)
    node_list.append(newN)
new_world.reset()
node_list[0].set_Positions_man(1,1)
node_list[1].set_Positions_man(2,0)
node_list[2].set_Positions_man(3,0)
node_list[3].set_Positions_man(2,2)
node_list[4].set_Positions_man(4,1)
node_list[5].set_Positions_man(2,4)
node_list[6].set_Positions_man(1,3)
node_list[7].set_Positions_man(3,3)
node_list[8].set_Positions_man(4,0)


### Creating a GUI to display the node and the annimations
new_GUI = gui.GUI()
new_GUI.open_GUI()
### Setting the world into the GUI
new_GUI.set_World(new_world)
new_GUI.set_Nodes(node_list)


count = 0
for i in range(1):

    for n in node_list:
        n.random_Move()

    for n in node_list :
        n.sense_In_Range_Nodes()

    for n in node_list:
        n.check_links(node_list)

    rec = node_list[0].complete_graph_coloring1()
    new_GUI.color_refresh(node_list)
    
    new_GUI.refresh(node_list)
    to_add = count_channel_reused(node_list) 
   
        
    count += to_add


    time.sleep(1)

    
    


    
 # print(f"Reutilisation loop #{i} {to_add}")
    # for n in node_list:
    #     id_list = []
    #     for v in n.in_Range_Nodes :
    #         id_list.append(v.id)
    #     tmp = n.get_used_channel()
    #     print (f"Final coloring for node {n.id} {n.coloring} ")
    #     print (f"Neighbour : {id_list}")
    #     print (f"channel usage in the range of {n.id}: {tmp}\n\n")
    
    




# print("-----------------------------------")
# for n in node_list:

#     tmp = n.get_used_channel()
    
    
#     id_list = []
#     for v in n.in_Range_Nodes :
#         id_list.append(v.id)


#     print (f"Final coloring for node {n.id} {n.coloring} ")
#     print (f"Transmission range : {n.transmission_Range}")
#     print (f"Neighbour : {id_list}")
#     print (f"channels : {n.free_Channels}")
#     print (f"channel usage in the range of {n.id}: {tmp}\n\n")
# print (f"re-utilisation = {count}" )
# print (f"finished in {rec} calls")

    
print(util.get_all_edges(node_list))


new_GUI.loop()

for n in node_list:
    n.sense_In_Range_Nodes()
