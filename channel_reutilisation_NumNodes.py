import nodes
import world
import constants as cst 
import time
from matplotlib import pyplot as plt 



def count_channel_reused (nodes_list):
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

    total_reused = 0

    for value in global_counting.values():
        total_reused += value
    
    return total_reused


f = open("result_channel_reutilisation_NUMBER_NODES","w")

number_Simulations = 10
size_x = 20
size_y= 20

num_Algo = 3

pace_nodes = 10
max_nodes = 350

x_value=[[] for i in range(num_Algo)]
y_value=[[] for i in range(num_Algo)]


for algo in range(num_Algo):
    
    # Iterate over the different configuration (Number of nodes)
    for x in range(10,max_nodes,pace_nodes):

        all_visit=[]
        for sim in range(number_Simulations):
            # Create a new world for this configuration
            new_world = world.World(size_x,size_y)
            # Create the nodes
            nodes_list = [] 
            for i in range(x):
                newN = nodes.Nodes(i,False,new_world)
                nodes_list.append(newN)
            for n in nodes_list :
                n.sense_In_Range_Nodes()
                        

            if algo == 0 :
                nodes_list[0].complete_graph_coloring1()
                v = count_channel_reused(nodes_list)

            elif algo == 1:
                nodes_list[0].complete_graph_coloring2()
                v = count_channel_reused(nodes_list)
            else :
                nodes_list[0].complete_graph_coloring3()
                v = count_channel_reused(nodes_list)
            
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

plt.xlabel(f'Number of nodes in a {size_x}x{size_y} sized world')
plt.ylabel(f'Number identical adjacent channel')
plt.legend()
plt.show()

