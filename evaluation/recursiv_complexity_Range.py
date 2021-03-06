import preRun as pr

import time

from matplotlib import pyplot as plt



import constants as cst
import nodes
import world


'''
Reccursiv call evaluation of the coloring algorithm with node randomly placed
size of the world 20x20
Number of nodes 250
No PU
Range from 1 to 5
Average over 10 simulations per Algo
11 Free channels 
Assignation could be random or fixed
3 distributed Coloring algorithm
'''


f = open(pr.get_path("result_complexity_calls_RANGE"),"w")

number_Simulations = 10
size_x = 20
size_y= 20

num_Algo = 3

number_nodes=250
max_Range = 6

x_value=[[] for i in range(num_Algo)]
y_value=[[] for i in range(num_Algo)]


for algo in range(num_Algo):
    
    # Iterate over the different configuration (Number of nodes)
    for x in range(1,max_Range):
        cst.MAX_TRANSMISSION_RANGE = x
        all_visit=[]
        for sim in range(number_Simulations):
            # Create a new world for this configuration
            new_world = world.World(size_x,size_y)
            # Create the nodes
            nodes_list = [] 
            for i in range(number_nodes):
                newN = nodes.Nodes(i,False,new_world)
                nodes_list.append(newN)
            for n in nodes_list :
                n.sense_In_Range_Nodes()
        

            if algo == 0 :
                v = nodes_list[0].complete_graph_coloring1()
            elif algo == 1:
                v = nodes_list[0].complete_graph_coloring2()
            else :
                v = nodes_list[0].complete_graph_coloring3()
            
            all_visit.append(v)
            

            
        average = sum(all_visit)/number_Simulations
        f.write(f'{algo} {x} {average}\n')
        x_value[algo].append(x)
        y_value[algo].append(average)
        print (y_value)
        
    

f.close()

for i in range(num_Algo):
    if i == 0 :
        title = "Distributed DSature"
    elif i == 1 :
        title = "Simple Color allocation"
    else :
        title = "Random Allocation"
    plt.plot(x_value[i], y_value[i], label=title)

plt.xlabel(f'Maximum Transmission range of a node')
plt.ylabel(f'Number recursiv calls')
plt.legend()
plt.show()