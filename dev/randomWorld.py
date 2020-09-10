import preRun

import nodes
import world
import gui
import util
import constants as cst




node_list = []

new_world = world.World(6,6)



SU_list = []
PU_list = [] 
### SU
for i in range(20):
    newN = nodes.Nodes(i,False,new_world,False)
    node_list.append(newN)
    SU_list.append(newN)
# ### PU
# for i in range(8, 9):
#     newN = nodes.Nodes(i,False,new_world, True)
#     node_list.append(newN)
#     PU_list.append(newN)

# for pu in PU_list:
#     pu.set_PU_Color()


### Creating a GUI to display the node and the annimations
new_GUI = gui.GUI()
new_GUI.open_GUI()
### Setting the world into the GUI
new_GUI.set_World(new_world)
new_GUI.set_Nodes(node_list)

for n in node_list :
        n.sense_In_Range_Nodes()
# for pu in PU_list:
#     pu.set_PU_Color()



#util.best_coloring(node_list, PU_list)

v = node_list[0].complete_graph_coloring1()
count = util.count_channel_reused_PU(node_list, SU_list, PU_list)
reste = util.count_coloring_proportion(node_list)
alledges = len(util.get_all_edges(node_list))
print("count", count)
print("reste", reste)
print("all edges", alledges)
print("rec", v)

new_GUI.color_refresh(node_list)

print("-----------------------------------")
for n in node_list:

    tmp = n.get_used_channel() 
    
    id_list = []
    for v in n.in_Range_Nodes :
        id_list.append(v.id)

    print(n.id, n.randomChan, n.free_Channels)
#    print (f"forbidden channels : {n.get_forbidden_channels()}")
#    print (f"Final coloring for node {n.id} {n.coloring} ")
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


new_GUI.loop()