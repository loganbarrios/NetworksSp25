import os
import networkx as nx
import matplotlib.pyplot as plt

def read_edgelist(file):
    adjacency_list = {} #first step to network creation from dataframe
    current_node = 1
    current_adjacencies = []
    with open(file) as f:
        while True:
            edge = f.readline().split() #split the line by whitespace
            #Move to next file
            if not edge:
                if current_adjacencies:
                    adjacency_list[current_node] = current_adjacencies
                break
            #Only numbers in edge list
            if len(edge) != 2 or not edge[0].isdigit() or not edge[1].isdigit():
                continue
            #building next node
            if int(edge[1]) == current_node:
                current_adjacencies.append(int(edge[0]))
            else:
                adjacency_list[current_node] = current_adjacencies #adding to adjacency list
                #building next node's list
                current_node = int(edge[1])
                current_adjacencies = [int(edge[0])]
    
    return adjacency_list

data_dir = "facebook100txt" #Directory containing data files
mean_degrees = [] #Creation of list to store mean degrees

#Process each file in the directory
for file in os.listdir(data_dir):
    #Exclude attribute and readme files
    if file.endswith(".txt") and "_attr" not in file and "readme" not in file:
        file_path = os.path.join(data_dir, file)

        adjacency_list = read_edgelist(file_path) #Read the adjacency list

        #Graph with edges
        G = nx.Graph()
        for node, neighbors in adjacency_list.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)

        #Mean degree calculation (part 1 of question)
        degrees = [deg for _, deg in G.degree()]
        if len(degrees) == 0:
            print(f"Graph for {file} has no nodes. Skipping...")
            continue
        
        mean_degree = sum(degrees) / len(degrees)
        mean_degrees.append(mean_degree)

#Histogram of mean degrees (part 2 of question)
bin_width = 5
bins = range(0, int(max(mean_degrees)) + bin_width, bin_width)

plt.figure(figsize=(10, 6))
plt.hist(mean_degrees, bins=bins, edgecolor='black', alpha=0.75)
plt.title("Network Connectiveness in the Facebook100 Dataset", fontsize=14)
plt.xlabel("Mean Degree in University Facebook Connections", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#Range of mean degrees for commenting on results (part 3)
print(f"Range of mean degrees: {min(mean_degrees):.2f} to {max(mean_degrees):.2f}")
