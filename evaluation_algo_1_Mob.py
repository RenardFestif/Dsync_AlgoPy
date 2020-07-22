import nodes
import world
import constants as cst 
import time
from matplotlib import pyplot as plt 


f = open("result_complexity_calls_coloring1_Mob","w")

number_rounds = 100
size_x = 20
size_y= 20

### the higher is the mobbilit degree the more is the deplacment range
mobility_degree = [0, 1, 5, 10, 15, 20]

number_nodes=[10, 20 ,30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]


x_value=[[] for i in range(len(mobility_degree))]
y_value=[[] for i in range(len(mobility_degree))]


for mob in range(len(mobility_degree)) :
    # Iterate over the different configuration (Number of nodes)
    for x in number_nodes:

        # Create a new world for this configuration
        new_world = world.World(size_x,size_y)
        # Create the nodes
        nodes_list = [] 
        for i in range(x):
            newN = nodes.Nodes(i,False,new_world)
            nodes_list.append(newN)
            
        
        cmpt = 0

        for rnd in range(number_rounds): 
            ### Add mobility
            cmpt += nodes_list[0].complete_graph_coloring1(0)
            for node in nodes_list:
                for i in range(mobility_degree[mob]):
                    node.random_Move()
            
            
            

            
        average = cmpt/number_rounds
        f.write(f'{x} {mobility_degree[mob]} {average}\n')
        x_value[mob].append(x)
        y_value[mob].append(average)
        print(y_value)


f.close()

for i in range(len(mobility_degree)):
    plt.plot(x_value[i], y_value[i])
plt.xlabel(f'Number of nodes in a {size_x}x{size_y} sized world')
plt.ylabel(f'Number recursiv calls on an average of {number_rounds} rounds')
plt.show()