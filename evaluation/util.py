import preRun
import constants as cst

def count_channel_reused (node_list):
    #### Section comptage de lien et de réutilisation

    # Elimination des doublons type (1,5) et (5,1)
    to_remove = []
    global_coloring = dict()
    for node in node_list :
        global_coloring.update(node.coloring)
        
    for key in global_coloring.keys():
        if (key[1], key[0]) in to_remove or (key[0], key[1]) in to_remove:
            continue
        to_remove.append(key)

    for key in to_remove:
        del global_coloring[key]

    # Comptage
    global_counting = dict()
    for i in range(cst.NUM_CHANNELS):
        global_counting[i] = 0

    done = []  
    
    for key, value in global_coloring.items():
        
        
        ### searching for reuse of value in direct neighbor of key[0]
        for n in node_list[key[0]].in_Range_Nodes:

            ### we don't count our link
            if n.id == key[1]:
                continue
            for n_key, n_value in n.coloring.items():
                if (n_key) in done:
                    continue
                elif ((value == n_value)):
                   
                    
                    global_counting[value] += 1
                    done.append(n_key)
                    done.append((n_key[1],n_key[0]))
                    done.append(key)
                    done.append((key[1],key[0]))

           
            
                    
            
        ### searching for reuse in direct neighbor of key[1]
        for n in node_list[key[1]].in_Range_Nodes:
            if n.id == key[0]:
                continue
            for n_key, n_value in n.coloring.items():
                if (n_key) in done:
                    
                    continue
                elif value == n_value:
                    
                    global_counting[value] += 1
                    done.append(n_key)
                    done.append((n_key[1],n_key[0]))
                    done.append(key)
                    done.append((key[1],key[0]))
            

    total_reused = 0

    for value in global_counting.values():
        total_reused += value
    
    return total_reused



def count_channel_reused_PU (nodes_list, SU_list, PU_list):
    to_remove = []
    global_coloring = dict()
    for node in SU_list :
        global_coloring.update(node.coloring)
        
    for key in global_coloring.keys():
        if (key[1], key[0]) in to_remove or (key[0], key[1]) in to_remove or nodes_list[key[1]] in PU_list:
            continue
        to_remove.append(key)

    for key in to_remove:
        del global_coloring[key]

    global_counting = dict()
    for i in range(cst.NUM_CHANNELS):
        global_counting[i] = 0

    done = []  


    for key, value in global_coloring.items():
        
        ### checking that the neighbor is not a PU self cannot be one since the dict is made out of the SU_list
        if (nodes_list[key[1]] in PU_list):
            continue
        ### searching for reuse in direct neighbor of key[0]
        for n in SU_list[key[0]].in_Range_Nodes:

            if n.id == key[1] or n in PU_list: 
                continue

            for n_key, n_value in n.coloring.items():

                if (n_key) in done or nodes_list[n_key[1]] in PU_list :
                    continue
                elif (value == n_value) :
                
                    global_counting[value] += 1
                    done.append(n_key)
                    done.append((n_key[1],n_key[0]))
                    done.append(key)
                    done.append((key[1],key[0]))
                
        
        ### searching for reuse in direct neighbor of key[1]
        for n in SU_list[key[1]].in_Range_Nodes:

            if n.id == key[0] or n in PU_list:
                continue

            for n_key, n_value in n.coloring.items():

                if (n_key) in done or nodes_list[n_key[1]] in PU_list :
                    continue
                elif value == n_value and (not(n_key in done)):

                    global_counting[value] += 1
                    done.append(n_key)
                    done.append((n_key[1],n_key[0]))
                    done.append(key)
                    done.append((key[1],key[0]))

    total_reused = 0

    for value in global_counting.values():
        total_reused += value
    
    return total_reused


def best_coloring(node_list, list_PU=None):
    PU_chans = []
    if list_PU != None :
        for pu in list_PU:
            PU_chans.append(pu.PU_channel)

    all_edges = get_all_edges(node_list)
    
    for c in range (cst.NUM_CHANNELS):
        MIS = []
        to_remove = []

        for edge in all_edges:

            if not(c in node_list[edge[0]].randomChan.keys()):
                continue
            if not(c in node_list[edge[1]].randomChan.keys()):          
                continue

            if edge in node_list[edge[0]].coloring.keys():
                continue
            if c in PU_chans:
                if is_chan_used(edge,c, node_list):
                    continue

            if edge in MIS:
                continue
            
            
            if len(MIS)==0:
                MIS.append(edge)
                to_remove.append(edge)
                continue 
            else:
                is_added = True
                for m in MIS:
                    #print(f"{edge} {m} are related ? {is_neighbor(edge,m, node_list)}")
                    if is_neighbor(edge,m, node_list):                
                        is_added = False

                if is_added:
                    if edge in all_edges :
                        to_remove.append(edge)
                    else:
                        continue
                    MIS.append(edge)
                    #print(f"added in MIS {edge}")
                        
            for r in to_remove:
                if r in all_edges:
                    all_edges.remove(r)
        
        #print("mis", MIS, c)
        # Color the edge from the MIS
        for m in MIS :
            node_list[m[0]].coloring[m[0],m[1]] = c
            node_list[m[1]].coloring[m[1],m[0]] = c

    ###Coloring the rest of the edges
    for n in node_list:
        for nn in n.in_Range_Nodes:
            if not((n.id, nn.id) in n.coloring):
                #print(f"{chans} for {n.id}")
                #print(f"coloring {(n.id,nn.id)} in {list(chans.keys())[0]}")
                
                chan = n.get_common_channel(nn)
                
                if len(chan) == 0:
                    continue

                {k: v for k, v in sorted(chan.items(), key=lambda item: item[1])}
                chan = list(chan)[0]    
            
                n.coloring[(n.id, nn.id)] = chan
                nn.coloring[(nn.id, n.id)] = chan
                
def local_count_chan(node, n_node):
    ret = dict()
    already = []
    for i in range(cst.NUM_CHANNELS):
        ret[i]=0
    for n in node.in_Range_Nodes:
        for key, val in n.coloring.items():
            if not(key in already):
                ret[val] += 1
                already.append(key)
                already.append((key[1], key[0]))

    for n in n_node.in_Range_Nodes:
        for key, val in n.coloring.items():
            if not(key in already):
                ret[val] += 1
                already.append(key)
                already.append((key[1], key[0]))
    return ret

def local_count_chan_solo(node):
    ret = dict()
    already = []
    for i in range(cst.NUM_CHANNELS):
        ret[i]=0
    for n in node.in_Range_Nodes:
        for key, val in n.coloring.items():
            if not(key in already):
                ret[val] += 1
                already.append(key)
                already.append((key[1], key[0]))
    return ret

def get_all_edges(node_list):
    ret = []
    for n in node_list :  
        for nn in n.in_Range_Nodes:
            if (n.id, nn.id) in ret or (nn.id,n.id) in ret:
                continue
            else :
                ret.append((n.id,nn.id))
    return ret

def is_neighbor(e,m, node_list):
    ### Checks if m is a direct/indirect neighbour
    e1 = node_list[e[0]]
    e2 = node_list[e[1]]

    m1 = node_list[m[0]]
    m2 = node_list[m[1]]

    if m == e:
        return True

    if m1 in e1.in_Range_Nodes:
        return True
    if m1 in e2.in_Range_Nodes:
        return True
    
    if m2 in e1.in_Range_Nodes:
        return True
    if m2 in e2.in_Range_Nodes:
        return True
    
    return False
    
def is_chan_used(e,c, node_list):
    ### Checks if m is a direct/indirect neighbour
    e1 = node_list[e[0]]
    e2 = node_list[e[1]]

    e1_local_dict=local_count_chan_solo(e1)
    e2_local_dict=local_count_chan_solo(e2)



    if c in e1_local_dict.keys():
        if e1_local_dict.get(c) > 0:
            return True

    if c in e2_local_dict.keys():
        if e2_local_dict.get(c) > 0:
            return True 

 
    return False

def PU_whithin_two_hops(node):
    for n in node.in_Range_Nodes:
        if n.isPU :
            return True
        for nn in n.in_Range_Nodes:
            if nn.isPU:
                return True
    return False

def count_coloring_proportion(node_list):
    edges = get_all_edges(node_list)
    
    for n in node_list:
        for key in n.coloring.keys():
            if key in edges:
                edges.remove(key)
    
    return len(edges)