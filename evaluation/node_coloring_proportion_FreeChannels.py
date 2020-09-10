import preRun as pr

import time

from matplotlib import pyplot as plt



import constants as cst
import nodes
import world
import util

'''
Channel Reutilisation evaluation of the coloring algorithm according to the number of free available channels
size of the world 20x20
Number of nodes from 250
No PU
Average over 10 simulations per Algo
Free channels from 0 to 50 with pace set to 5
3 distributed Coloring algorithm
1 centralized algorithm

Comparison with Centralized Must be done with a fixed channel assignation for each SU to be consistent 
newnode = node.Node(id,False,world,False/True, **False**)

Other usage, don't take into account the centralized algo and channel assignation random
newnode = node.Node(id,False,world,False/True, **False**)
'''


f = open(pr.get_path("result_not_colored_link_FreeChannel"),"w")


number_Simulations = 10
size_x = 20
size_y= 20
num_nodes = 250

num_Algo = 4

pace_Chan=5
max_chan = 50

x_value=[[] for i in range(num_Algo)]
y_value=[[] for i in range(num_Algo)]


for algo in range(num_Algo):
    
    # Iterate over the different configuration (Number of nodes)
    for x in range(1,max_chan,pace_Chan):

        cst.NUM_CHANNELS = x

        all_visit=[]
        for sim in range(number_Simulations):
            # Create a new world for this configuration
            new_world = world.World(size_x,size_y)
            # Create the nodes
            nodes_list = []
       

            for i in range(num_nodes):
                newN = nodes.Nodes(i,False,new_world)
                nodes_list.append(newN)
                
           
            for n in nodes_list :
                n.sense_In_Range_Nodes()
                        
            
            if algo == 0 :
                nodes_list[0].complete_graph_coloring1()
                total = len(util.get_all_edges(nodes_list))
                v = util.count_coloring_proportion(nodes_list)
                
                
            elif algo == 1:
                nodes_list[0].complete_graph_coloring2()
                total = len(util.get_all_edges(nodes_list))
                v = util.count_coloring_proportion(nodes_list)
                
            elif algo == 2 :
                nodes_list[0].complete_graph_coloring3()
                total = len(util.get_all_edges(nodes_list))
                v = util.count_coloring_proportion(nodes_list)
                
            else :
                util.best_coloring(nodes_list)
                total = len(util.get_all_edges(nodes_list))
                v = util.count_coloring_proportion(nodes_list)
                

            all_visit.append(((total-v)/total)*100)
            

        print(total)   
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
        title = "Centralized Algorithm"

    plt.plot(x_value[i], y_value[i], label=title)

plt.xlabel(f'Number of free channel available')
plt.ylabel(f'Average number of colored links')
plt.legend()
plt.show()

