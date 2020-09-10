import preRun as pr

import time

from matplotlib import pyplot as plt



import constants as cst
import nodes
import world
import util

'''
Channel Reutilisation evaluation of the coloring algorithm according to the number of nodes in the nodes
size of the world 20x20
Number of nodes from 0 to 350
No PU
Average over 10 simulations per Algo
11 Free channels 
3 distributed Coloring algorithm
1 centralized algorithm

Comparison with Centralized Must be done with a fixed channel assignation for each SU to be consistent 
newnode = node.Node(id,False,world,False/True, **False**)

Other usage, don't take into account the centralized algo and channel assignation random
newnode = node.Node(id,False,world,False/True, **False**)
'''


f = open(pr.get_path("result_channel_reutilisatuin_NUM_NODES"),"w")





number_Simulations = 10
size_x = 20
size_y= 20

num_Algo = 4

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
                newN = nodes.Nodes(i,False,new_world, False, True)
                nodes_list.append(newN)
            for n in nodes_list :
                n.sense_In_Range_Nodes()
                        

            if algo == 0 :
                nodes_list[0].complete_graph_coloring1()
                v = util.count_channel_reused(nodes_list)

            elif algo == 1:
                nodes_list[0].complete_graph_coloring2()
                v = util.count_channel_reused(nodes_list)
            elif algo == 2 :
                nodes_list[0].complete_graph_coloring3()
                v = util.count_channel_reused(nodes_list)
            else :
                util.best_coloring(nodes_list)
                v = util.count_channel_reused(nodes_list)
            
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
    elif i == 2 :
        title = "Random Allocation"
    else : 
        title = "Centralized Coloring"
    plt.plot(x_value[i], y_value[i], label=title)

plt.xlabel(f'Number of nodes in a {size_x}x{size_y} sized world')
plt.ylabel(f'Number identical adjacent channel')
plt.legend()
plt.show()

