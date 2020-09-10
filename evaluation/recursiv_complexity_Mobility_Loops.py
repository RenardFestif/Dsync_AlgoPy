import preRun as pr

import time

from matplotlib import pyplot as plt



import constants as cst
import nodes
import world

'''
Recursive calls evaluation of the coloring algorithm with random mobility of the nodes
size of the world 20x20
Number of nodes 250 (55% of the world is occupied)
Loops 20
Average over 10 simulations per Algo
3 Coloring algorithm
'''


f = open(pr.get_path("result_complexity_calls_MOBILITY_LOOPS"),"w")

number_Simulations = 10

size_x = 20
size_y= 20

num_Algo = 3

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
        

            if algo == 0 :
                for i in range(x):

                    for n in node_list:
                        n.random_Move()

                    for n in node_list :
                        n.sense_In_Range_Nodes()

                    for n in node_list:
                        n.check_links(node_list)

                    v += node_list[0].complete_graph_coloring1()
                    


                    
            elif algo == 1:
                for i in range(x):

                    for n in node_list:
                        n.random_Move()

                    for n in node_list :
                        n.sense_In_Range_Nodes()

                    for n in node_list:
                        n.check_links(node_list)

                    v += node_list[0].complete_graph_coloring2()
                   
            else :
                for i in range(x):

                    for n in node_list:
                        n.random_Move()

                    for n in node_list :
                        n.sense_In_Range_Nodes()

                    for n in node_list:
                        n.check_links(node_list)

                    v += node_list[0].complete_graph_coloring3()
                    
            
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
    else :
        title = "Random Allocation"
    plt.plot(x_value[i], y_value[i], label=title)

plt.xlabel(f'Number of random displacement')
plt.ylabel(f'Number recursiv calls')
plt.legend()
plt.show()
