import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def read_edgelist(file):
    adjacency_list = {}  
    current_node = 1
    current_adjacencies = []
    with open(file) as f:
        while True:
            edge = f.readline().split()
            if not edge:
                if current_adjacencies:
                    adjacency_list[current_node] = current_adjacencies
                break
            if len(edge) != 2 or not edge[0].isdigit() or not edge[1].isdigit():
                continue
            if int(edge[1]) == current_node:
                current_adjacencies.append(int(edge[0]))
            else:
                adjacency_list[current_node] = current_adjacencies 
                current_node = int(edge[1])
                current_adjacencies = [int(edge[0])]

    return adjacency_list

data_dir = "facebook100txt" 
mean_degrees = [] 
paradox_ratios = []
file_names = []

for file in os.listdir(data_dir):
    if file.endswith(".txt") and "_attr" not in file and "readme" not in file.lower():
        file_path = os.path.join(data_dir, file)

        adjacency_list = read_edgelist(file_path) 

        G = nx.Graph()
        for node, neighbors in adjacency_list.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)

        #Skip if the graph has no nodes
        if len(G.nodes) == 0:
            print(f"Graph for {file} has no nodes. Skipping...")
            continue

        degrees = dict(G.degree())
        mean_degree = np.mean(list(degrees.values())) 
        mean_degrees.append(mean_degree)
        file_names.append(file.replace('.txt', '')) 

        #mean squared degree
        mean_squared_degree = np.mean([deg ** 2 for deg in degrees.values()])

        #mean neighbor degree
        mean_neighbor_degree = mean_squared_degree / mean_degree

        #paradox ratio
        paradox_ratio = mean_neighbor_degree / mean_degree
        paradox_ratios.append(paradox_ratio)

plt.figure(figsize=(10, 6))
plt.scatter(mean_degrees, paradox_ratios, color='blue', alpha=0.7, label="Networks")

#No Paradox Line
plt.axhline(y=1, color='red', linestyle='--', label="No Paradox Line")

highlighted_universities = ["Reed", "Colgate", "Mississippi", "Virginia", "Berkeley"]
for i, name in enumerate(file_names):
    if any(uni in name for uni in highlighted_universities):
        plt.annotate(name, (mean_degrees[i], paradox_ratios[i]), fontsize=10, color='darkred')

plt.title("Friendship Paradox in FB100 Networks", fontsize=14)
plt.xlabel("Mean Degree (〈ku〉)", fontsize=12)
plt.ylabel("Paradox Ratio (〈kv〉 / 〈ku〉)", fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()
