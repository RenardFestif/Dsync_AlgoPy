import nodes
import world
import constants as cst 
import time
from matplotlib import pyplot as plt 


f = open("result_complexity_calls_coloring1","w")

number_Simulations = 10
size_x = 20
size_y= 20

number_nodes=[11, 20 ,30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
num_PU=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

x_value=[[] for i in range(len(number_PU))]
y_value=[[] for i in range(len(number_PU))]


for PU_Num in range(len(number_PU)):
    cst.NUM_CHANNELS = number_PU[PU_Num]
    # Iterate over the different configuration (Number of nodes)
    for x in number_nodes:

        all_visit=[]
        for sim in range(number_Simulations):
            # Create a new world for this configuration
            new_world = world.World(size_x,size_y)
            # Create the nodes
            nodes_list = [] 
            SU_list = []
            PU_list = []
            for i in range(x-PU_Num):
                newN = nodes.Nodes(i,False,new_world)
                nodes_list.append(newN)
                SU_list.append(newN)
            for i in range(cst.NUM_NODES-cst.NUM_PU, cst.NUM_NODES):
                newN = nodes.Nodes(i,False,new_world,True)
                PU_list.append(newN) 
                nodes_list.append(newN) 

            for n in nodes_list :
                n.sense_In_Range_Nodes()
        

        
            v = SU_list[0].complete_graph_coloring1(PU_list)
            
            all_visit.append(v)
            

            
        average = sum(all_visit)/len(all_visit)
        f.write(f'{x} {average}\n')
        x_value[PU_Num].append(x)
        y_value[PU_Num].append(average)
        print(y_value)
    

f.close()

for i in range(len(number_PU)):
    plt.plot(x_value[i], y_value[i], label=f"With {number_PU[i]}")
plt.xlabel(f'Number of nodes in a {size_x}x{size_y} sized world')
plt.ylabel(f'Number recursiv calls')
plt.show()