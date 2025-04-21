import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def compute_log_likelihood(graph, partition, num_groups):
    #interaction counters between groups
    inter_group_links = {(g1, g2): 0 for g1 in range(1, num_groups + 1) for g2 in range(1, num_groups + 1)}
    
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            inter_group_links[(partition[node], partition[neighbor])] += 1

    group_degrees = {g: sum(inter_group_links[(g, other)] for other in range(1, num_groups + 1)) for g in range(1, num_groups + 1)}
    
    log_likelihood = sum(
        inter_group_links[(g1, g2)] * np.log(inter_group_links[(g1, g2)] / (group_degrees[g1] * group_degrees[g2]))
        for g1, g2 in inter_group_links if inter_group_links[(g1, g2)] > 0
    )
    
    return log_likelihood

def optimize_partition(graph, partition, num_groups, frozen_nodes):
    best_score = compute_log_likelihood(graph, partition, num_groups)
    optimal_move = None
    
    #non-frozen nodes
    movable_nodes = [node for node in graph if frozen_nodes[node] == 0]
    
    for node in movable_nodes:
        for new_group in [g for g in range(1, num_groups + 1) if g != partition[node]]:
            temp_partition = partition.copy()
            temp_partition[node] = new_group
            
            new_score = compute_log_likelihood(graph, temp_partition, num_groups)
            if new_score > best_score:
                best_score = new_score
                optimal_move = (node, new_group)
    
    return best_score, optimal_move

def visualize_graph(graph, partition, title, cmap):
    g_nx = nx.Graph(graph)
    layout = nx.spring_layout(g_nx)
    colors = [partition[node] for node in g_nx.nodes()]
    
    plt.figure(figsize=(3, 2), dpi=300)
    nx.draw(g_nx, with_labels=True, node_color=colors, cmap=cmap, font_color='white', pos=layout)
    plt.title(title)
    plt.show()

#example Graph
example_graph = {
    1: [2, 3, 6, 7, 8, 9],
    2: [1],
    3: [1, 4, 6],
    4: [3, 6],
    5: [6],
    6: [1, 3, 4, 5],
    7: [1],
    8: [1],
    9: [1],
}

#Define partitions
num_partitions = 3
while True:
    node_groups = {node: np.random.choice(range(1, num_partitions + 1)) for node in example_graph.keys()}
    if len(set(node_groups.values())) == num_partitions:
        break

#Define frozen nodes
frozen_nodes = {node: 0 for node in example_graph.keys()}
frozen_nodes[2] = 1

#initial partition 
visualize_graph(example_graph, node_groups, 'Initial Partition', cmap=plt.cm.viridis)

#partition optimization
likelihood, move = optimize_partition(example_graph, node_groups, num_partitions, frozen_nodes)
if move:
    node_groups[move[0]] = move[1]

#new partition
visualize_graph(example_graph, node_groups, 'Optimized Partition', cmap=plt.cm.plasma)
