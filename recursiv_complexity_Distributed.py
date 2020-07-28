import nodes
import world
import constants as cst 
import time
from matplotlib import pyplot as plt 
import concurrent.futures


f = open("result_complexity_calls_DISTRIBUTED","w")

number_Simulations = 10
size_x = 20
size_y= 20

num_Algo = 3

number_nodes=250
num_Master_Node = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90]

x_value=[[] for i in range(num_Algo)]
y_value=[[] for i in range(num_Algo)]


for algo in range(num_Algo):
    
    # Iterate over the different configuration (Number of nodes)
    for init in num_Master_Node:
        
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
        
            list_calls = []

            if algo == 0 :
                if init == 1 :
                    list_calls.append(nodes_list[init].complete_graph_coloring1())
                    continue
                else : 
                    with concurrent.futures.ProcessPoolExecutor() as executor:
                        for i in range(init):
                            f = executor.submit(nodes_list[i].complete_graph_coloring1)
                            list_calls.append(f.result())

            elif algo == 1:
                if init == 1 :
                    list_calls.append(nodes_list[init].complete_graph_coloring2())   
                
                else :  
                    with concurrent.futures.ProcessPoolExecutor() as executor:
                        for i in range(init):
                            f = executor.submit(nodes_list[i].complete_graph_coloring2)
                            list_calls.append(f.result())
            else :
                if init == 1 :
                    list_calls.append(nodes_list[init].complete_graph_coloring3())   
                else :
                    with concurrent.futures.ProcessPoolExecutor() as executor:
                        for i in range(init):
                            f = executor.submit(nodes_list[i].complete_graph_coloring3)
                            list_calls.append(f.result())
            print (init, list_calls)
            all_visit.append(sum(list_calls))
            

            
        average = sum(all_visit)/number_Simulations
        f.write(f'{algo} {init} {average}\n')
        x_value[algo].append(init)
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

plt.xlabel(f'Number of nodes in a {size_x}x{size_y} sized world')
plt.ylabel(f'Number recursiv calls')
plt.legend()
plt.show()