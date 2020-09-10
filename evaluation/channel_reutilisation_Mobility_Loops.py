import preRun as pr

import time

from matplotlib import pyplot as plt



import constants as cst
import nodes
import world
import util


'''
Channel Reutilisation evaluation of the coloring algorithm with a random mobility
size of the world 20x20
Number of nodes set to 250
No PU
loop of mobility from 0 to 20 pace of 5
Average over 10 simulations per Algo
Free channels 11
3 distributed Coloring algorithm
1 centralized algorithm

Comparison with Centralized Must be done with a fixed channel assignation for each SU to be consistent 
newnode = node.Node(id,False,world,False/True, **False**)

Other usage, don't take into account the centralized algo and channel assignation random
newnode = node.Node(id,False,world,False/True, **False**)
'''

f = open(pr.get_path("result_channel_reutilisation_MOBILITY_NODE"),"w")





number_Simulations = 10
size_x = 20
size_y= 20

num_Algo = 4

pace_loops = 2
max_loops = 20
node_amount = 250

x_value=[[] for i in range(num_Algo)]
y_value=[[] for i in range(num_Algo)]


for algo in range(num_Algo):
    
    # Iterate over the different configuration (Number of nodes)
    for x in range(1,max_loops,pace_loops):

        all_visit=[]
        for sim in range(number_Simulations):
            # Create a new world for this configuration
            new_world = world.World(size_x,size_y)
            # Create the nodes
            node_list = [] 
            v = 0
            for i in range(node_amount):
                newN = nodes.Nodes(i,False,new_world)
                node_list.append(newN)
            for n in node_list :
                n.sense_In_Range_Nodes()
                        

            if algo == 0 :
                for i in range(x):

                    for n in node_list:
                        n.random_Move()

                    for n in node_list :
                        n.sense_In_Range_Nodes()

                    for n in node_list:
                        n.check_links(node_list)

                    node_list[0].complete_graph_coloring1()
                    v += util.count_channel_reused(node_list)

            elif algo == 1:
                for i in range(x):

                    for n in node_list:
                        n.random_Move()

                    for n in node_list :
                        n.sense_In_Range_Nodes()

                    for n in node_list:
                        n.check_links(node_list)

                    node_list[0].complete_graph_coloring2()
                    v += util.count_channel_reused(node_list)

            else :
                for i in range(x):

                    for n in node_list:
                        n.random_Move()

                    for n in node_list :
                        n.sense_In_Range_Nodes()

                    for n in node_list:
                        n.check_links(node_list)

                    node_list[0].complete_graph_coloring3()
                    v += util.count_channel_reused(node_list)
            
            all_visit.append(v/x)
            

            
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
        title = "Centralized algorithm"
    plt.plot(x_value[i], y_value[i], label=title)

plt.xlabel(f'Number of nodes in a {size_x}x{size_y} sized world')
plt.ylabel(f'Number identical adjacent channel')
plt.legend()
plt.show()

