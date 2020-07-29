import nodes
import world
import constants as cst 
import time
from matplotlib import pyplot as plt 



def count_channel_reused (nodes_list, SU_list, PU_list):
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

    total_reused = 0

    for value in global_counting.values():
        total_reused += value
    
    return total_reused


f = open("result_channel_reutilisation_NUMBER_PU","w")

number_Simulations = 10
size_x = 20
size_y= 20
num_nodes = 250

num_Algo = 3

pace_PU=5

x_value=[[] for i in range(num_Algo)]
y_value=[[] for i in range(num_Algo)]


for algo in range(num_Algo):
    
    # Iterate over the different configuration (Number of nodes)
    for x in range(1,200,pace_PU):

        all_visit=[]
        for sim in range(number_Simulations):
            # Create a new world for this configuration
            new_world = world.World(size_x,size_y)
            # Create the nodes
            nodes_list = []
            SU_list = []
            PU_list = [] 
            ### SU
            for i in range(num_nodes-x):
                newN = nodes.Nodes(i,False,new_world, False)
                nodes_list.append(newN)
                SU_list.append(newN)
            ### PU
            for i in range(num_nodes-x, num_nodes):
                newN = nodes.Nodes(i,False,new_world, True)
                nodes_list.append(newN)
                PU_list.append(newN)
            for n in nodes_list :
                n.sense_In_Range_Nodes()
                        

            if algo == 0 :
                nodes_list[0].complete_graph_coloring1()
                v = count_channel_reused(nodes_list, SU_list, PU_list)

            elif algo == 1:
                nodes_list[0].complete_graph_coloring2()
                v = count_channel_reused(nodes_list, SU_list, PU_list)
            else :
                nodes_list[0].complete_graph_coloring3()
                v = count_channel_reused(nodes_list, SU_list, PU_list)
            
            all_visit.append(v)
            

            
        average = sum(all_visit)/number_Simulations
        f.write(f'{algo} {x} {average}\n')
        x_value[algo].append(x)
        y_value[algo].append(average)
        print(y_value)
        
    

f.close()

for i in range(num_Algo):
    if i == 0 :
        title = "Distributed DSature"
    elif i == 1 :
        title = "Simple Color allocation"
    else :
        title = "Random Allocation"
    plt.plot(x_value[i], y_value[i], label=title)

plt.xlabel(f'Number of PU in a {size_x}x{size_y} sized world')
plt.ylabel(f'Number of identical adjacent channels')
plt.legend()
plt.show()

