import nodes
import world
import constants as cst
import time
from matplotlib import pyplot as plt


f = open("result_channel_usage","w")

number_Simulations = 10
size_x = 20
size_y= 20

num_algo = 3

number_nodes=[10, 20 ,30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]

x_value=[[] for i in range(num_algo)]
y_value=[[] for i in range(num_algo)]

# Iterate over the different configuration (Number of nodes)
for j in range(num_algo):
    for x in number_nodes:

        adjacent_tmp = 0


        for sim in range(number_Simulations):
            # Create a new world for this configuration
            new_world = world.World(size_x,size_y)
            # Create the nodes
            nodes_list = []
            for i in range(x):
                newN = nodes.Nodes(i,False,new_world)
                nodes_list.append(newN)

            if j == 0:
                nodes_list[0].complete_graph_coloring1()

            elif j == 1 :
                for n in nodes_list :
                    n.sense_In_Range_Nodes()

                nodes_list[0].complete_graph_coloring2()
            else :
                for n in nodes_list :
                    n.sense_In_Range_Nodes()

                nodes_list[0].complete_graph_coloring3()

            ### Compute the number of adjacent color

            sum_tmp = 0



            for node in nodes_list:

                tmp = node.get_used_channel()

                # for i in range(cst.NUM_CHANNELS):
                #     tmp[i] = 0

                # for chan in node.free_Channels.keys():

                #     tmp[chan] += node.free_Channels.get(chan)
                # for color in node.coloring.values():
                #     tmp[color] += 1
                
                for i in tmp.values():
                    
                    if i == 0 or i == 1.0:
                        continue
                    else :
                        sum_tmp += i
        

        adjacent_tmp = (sum_tmp / x) / number_Simulations

        f.write(f'{x} {adjacent_tmp}\n')

        y_value[j].append(adjacent_tmp)
        x_value[j].append(x)




f.close()

plt.plot(x_value[0], y_value[0], label='Distributed D-satur')
plt.plot(x_value[1], y_value[1], label='Simple Distributed Algo')
plt.plot(x_value[2], y_value[2], label='Random channel assignation')
plt.legend()
plt.xlabel(f'Number of nodes in a {size_x}x{size_y} sized world')
plt.ylabel(f'average number of channel re-used per node')
plt.show()