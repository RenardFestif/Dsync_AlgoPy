import multiprocessing
import nodes

def no_Topology_change(num_initiator, num_Nodes, nodes_liste):
    print ("------------------No Topology change------------------")
    print ("Computing Convergence time for an environment with", num_Nodes,"nodes and", num_initiator,"master nodes")

    processes = []

    for i in range (num_initiator):
        ### Since the nodes are posisionned randomly in the graph we can use i to retrieve a node from it
        print (i) 
        
        tmp_Node = nodes_liste[i]

        p = multiprocessing.Process(target=tmp_Node.complete_graph_coloring1)
        p.start()
        processes.append(p)

    