import nodes
import world
import constants as cst 
import time
from matplotlib import pyplot as plt 
import multiprocessing

def coloring(nodes_id):
    nodes_list[nodes_id].complete_graph_coloring1()

f = open("result_complexity_coloring1","w")

number_init_node = 2
processes = []

number_Simulations = 10
size_x = 20
size_y= 20

number_nodes=[10, 20 ,30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]

x_value=[]
y_value=[]


# Iterate over the different configuration (Number of nodes)
for x in number_nodes:

    all_time=[]
    for  sim in range(number_Simulations):
        # Create a new world for this configuration
        new_world = world.World(size_x,size_y)
        # Create the nodes
        nodes_list = [] 
        for i in range(x):
            newN = nodes.Nodes(i,False,new_world)
            nodes_list.append(newN)

        ### Process
        for init_node in range(number_init_node):
            p = multiprocessing.Process(target=coloring, args=[init_node])

            # Timer start
            start = time.perf_counter()
            p.start()
            processes.append(p)
            # Timer end
            finish = time.perf_counter()
            print("sim on", x,"done", sim,"times")
            all_time.append(finish-start)
        for p in processes:
            p.join()

    print("sim on",x,"complete")
    average = sum(all_time)/len(all_time)
    f.write(f'{x} {average}\n')
    x_value.append(x)
    y_value.append(average)



f.close()


plt.plot(x_value, y_value)
plt.xlabel(f'Number of nodes in a {size_x}x{size_y} sized world')
plt.ylabel('Time of execution in seconds')
plt.show()


