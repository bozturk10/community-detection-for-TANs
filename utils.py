from graph_tool.all import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_edge_matrice(state):
    b = contiguous_map(state.get_blocks())
    state = state.copy(b=b)

    e = state.get_matrix()

    B = state.get_nonempty_B()

    return e.todense()[:B, :B]


def plot_edge_matrice(m):
    plt.figure(figsize=(400, 400),dpi=80)
    plt.matshow(m)
    plt.show()

    
def get_sbm_model_blocks(graph,state):
    blocks = state.get_blocks()
    mapping_dict = {blocks[i]: i for i in range(graph.num_edges())}
    b = state.get_blocks()
    group_list = []
    groups = []
    for v in graph.vertices():
        r = b[v]   # group membership of vertex 10
        group_list.append([graph.vp.name[v],r,*graph.get_total_degrees([v]),graph.vp.betw_centr[v]])
        groups.append(r)
    NGO_blocks = pd.DataFrame(group_list,columns=["NGO","block_id","degree","betw_centr"])
    
    return NGO_blocks

def get_modularity_communities():
    community1= set(open("../data/community1.txt").read().replace('"', '').split('\n'))
    community2= set(open("../data/community2.txt").read().replace('"', '').split('\n'))
    community3= set(open("../data/community3.txt").read().replace('"', '').split('\n'))
    community4= set(open("../data/community4.txt").read().replace('"', '').split('\n'))
    a=pd.DataFrame(list(community1))
    a["block_id"]="Place-based and faith-based"
    b=pd.DataFrame(list(community2))
    b["block_id"]="Textbook NGO community"
    c=pd.DataFrame(list(community3))
    c["block_id"]="Research and policy NGO"
    d=pd.DataFrame(list(community4))
    d["block_id"]="Environmental action NGO"
    modularity_blocks=pd.concat([a,b,c,d]).rename({0:"NGO"},axis=1).query("NGO!=''")
    
    return modularity_blocks