import nodes
import world
import constants as cst 
import time
from matplotlib import pyplot as plt 


f = open("result_channel_repartition ","w")

number_Simulations = 30
size_x = 20
size_y= 20

number_nodes=[10, 20 ,30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]

x_value=[]
y_value=[]

# Iterate over the different configuration (Number of nodes)
for x in number_nodes:

    channel_rep=[]
    
    #initialisation
    for c in range(cst.NUM_CHANNELS):
        channel_rep.append(0)
    

    for sim in range(number_Simulations):
        # Create a new world for this configuration
        new_world = world.World(size_x,size_y)
        # Create the nodes
        nodes_list = [] 
        for i in range(x):
            newN = nodes.Nodes(i,False,new_world)
            nodes_list.append(newN)

        nodes_list[0].complete_graph_coloring1(0)

        
        for n in nodes_list :
            
            for colors in n.coloring.values():
                # Strange behaviour here if not stated
                if colors == None :
                    continue
                channel_rep[colors] +=1

        
    
    # Computing the average over the simulations and divide by 2 to omit the repetitions due to the dictionary architecture
    for i in range(len(channel_rep)):
        channel_rep[i] = channel_rep[i]/2
        # channel_rep[i] = channel_rep[i]/number_Simulations
        

    
    f.write(f'{x} {channel_rep}\n')
    
    y_value.append(channel_rep)
    
    
for i in range(cst.NUM_CHANNELS):
    x_value.append(i)
        
        

f.close()

for i in range(cst.NUM_CHANNELS):
    plt.plot(x_value, y_value[i])
plt.xlabel(f'Number of nodes in a {size_x}x{size_y} sized world')
plt.ylabel(f'Channel reppartition')
plt.show()