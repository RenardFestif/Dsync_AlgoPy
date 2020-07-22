import nodes
import world
import constants as cst 
import time
from matplotlib import pyplot as plt 


f = open("result_complexity_calls_coloring1","w")

number_Simulations = 10
size_x = 20
size_y= 20

number_nodes=[10, 20 ,30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
number_channels=[5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

x_value=[[] for i in range(len(number_channels))]
y_value=[[] for i in range(len(number_channels))]


for chan_Num in range(len(number_channels)):
    cst.NUM_CHANNELS = number_channels[chan_Num]
    # Iterate over the different configuration (Number of nodes)
    for x in number_nodes:

        all_visit=[]
        for sim in range(number_Simulations):
            # Create a new world for this configuration
            new_world = world.World(size_x,size_y)
            # Create the nodes
            nodes_list = [] 
            for i in range(x):
                newN = nodes.Nodes(i,False,new_world)
                nodes_list.append(newN)

            
        

        
            v = nodes_list[0].complete_graph_coloring1(0)
            
            all_visit.append(v)
            

            
        average = sum(all_visit)/len(all_visit)
        f.write(f'{x} {average}\n')
        x_value[chan_Num].append(x)
        y_value[chan_Num].append(average)
        print(y_value)
    

f.close()

for i in range(len(number_channels)):
    plt.plot(x_value[i], y_value[i])
plt.xlabel(f'Number of nodes in a {size_x}x{size_y} sized world')
plt.ylabel(f'Number recursiv calls')
plt.show()