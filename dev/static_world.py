import preRun

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
                   
                    #print(n_key)
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

def count_channel_reused_PU (nodes_list, SU_list, PU_list):
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

                if (n_key) in done or nodes_list[n_key[1]] in PU_list :
                    continue
                elif (value == n_value) :
                
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

                if (n_key) in done or nodes_list[n_key[1]] in PU_list :
                    continue
                elif value == n_value and (not(n_key in done)):

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

# for i in range(9):
#     newN = nodes.Nodes(i,False, new_world, False)
#     node_list.append(newN)


SU_list = []
PU_list = [] 
### SU
for i in range(8):
    newN = nodes.Nodes(i,False,new_world,False)
    node_list.append(newN)
    SU_list.append(newN)
### PU
for i in range(8, 9):
    newN = nodes.Nodes(i,False,new_world, True)
    node_list.append(newN)
    PU_list.append(newN)

for pu in PU_list:
    pu.set_PU_Color()

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

for n in node_list :
        n.sense_In_Range_Nodes()
for pu in PU_list:
    pu.set_PU_Color()



util.best_coloring(node_list, PU_list)

#v = node_list[0].complete_graph_coloring2(PU_list)
count = util.count_channel_reused_PU(node_list, SU_list, PU_list)
reste = util.count_coloring_proportion(node_list)

print("count", count)
print("reste", reste)
#print ("rec", v)


new_GUI.color_refresh(node_list)



print("-----------------------------------")
for n in node_list:

    tmp = n.get_used_channel()
    
    
    id_list = []
    for v in n.in_Range_Nodes :
        id_list.append(v.id)

    print(n.id, n.randomChan)
    print (f"forbidden channels : {n.get_forbidden_channels()}")
    print (f"Final coloring for node {n.coloring}")
#     print (f"Transmission range : {n.transmission_Range}")
#     print (f"Neighbour : {id_list}")
#     if n.isPU:
#     print (f"Channel PU {n.PU_channel}")
#     print (f"channels : {n.sense_free_channels(PU_list)}")
#     print (f"channel usage in the range of {n.id}: {tmp}\n\n")
# print (f"re-utilisation = {count}" )


# m = node_list[0]
# e = (0, 3)
# print(m.PU_channel)
# print(util.is_chan_used(e,m.PU_channel,node_list))  
# print(util.PU_whithin_two_hops(m))


print("-----------------------------------")
n0 = node_list[0]
n3 = node_list[3]
print("Rchan 0", n0.randomChan, "Rchan 3", n3.randomChan)
print("Common channel 0 and 3", n0.get_common_channel(n3))

new_GUI.loop()