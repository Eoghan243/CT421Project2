import networkx as nx
import random
import matplotlib.pyplot as plt

def decentralised_graph_colouring(graph, colours, max_iterations=100):
    colour_map = {}

    # Randomly assign colours to each node
    for node in graph.nodes():
        colour_map[node] = random.choice(colours)

    # Count initial conflicts
    conflicts = count_conflicts(graph, colour_map)
    conflict_history = [conflicts]  # Store conflicts

    iteration = 0
    while conflicts > 0 and iteration < max_iterations:
        node = random.choice(list(graph.nodes()))  # Select a random node
        neighbours = list(graph.neighbors(node))  # Get neighbours of the node
        neighbour_colours = [colour_map[n] for n in neighbours]  # Get colours of neighbours

        # Find available colours that minimise conflicts
        available_colours = [c for c in colours if c not in neighbour_colours]

        if available_colours:
            new_colour = min(available_colours, key=lambda x: neighbour_colours.count(x))
            colour_map[node] = new_colour
            conflicts = count_conflicts(graph, colour_map)
            conflict_history.append(conflicts)  # Update conflict history
        else:
            break  
        
        iteration += 1

    return colour_map, conflict_history

def count_conflicts(graph, colour_map):
    conflicts = 0
    for edge in graph.edges():
        if colour_map[edge[0]] == colour_map[edge[1]]:
            conflicts += 1
    return conflicts

def generate_topology(topology, num_nodes, num_edges):
    if topology == "random":
        return nx.gnm_random_graph(num_nodes, num_edges)
    elif topology == "scale-free":
        return nx.barabasi_albert_graph(num_nodes, int(num_edges * 2 / num_nodes))
    elif topology == "small-world":
        return nx.watts_strogatz_graph(num_nodes, k=4, p=0.1)
    else:
        raise ValueError("Invalid topology specified")

if __name__ == "__main__":
    num_nodes = 20
    num_edges = 40
    colours = ['red', 'yellow', 'blue', 'green', 'pink'] 
    network_topologies = ["random", "small-world", "scale-free"]
    topology_names = ["Random", "Small-World", "Scale-Free"]

    plt.figure(figsize=(15, 5))
    conflict_histories = []

    for i, topology in enumerate(network_topologies):
        try:
            # Generate graph with selected topology
            graph = generate_topology(topology, num_nodes, num_edges)

           
            pos = nx.spring_layout(graph)

            # Apply decentralised graph colouring algorithm
            initial_colour_map, _ = decentralised_graph_colouring(graph, colours)
            final_colour_map, _ = decentralised_graph_colouring(graph, colours)

            # Print colour map of nodes
            print(f"Colour Map for {topology} Topology:")
            print("Initial Colour Map:", initial_colour_map)
            print("Final Colour Map:", final_colour_map)

            # Convert final colour map list to a dictionary
            final_colour_map_dict = {node: colour for node, colour in zip(graph.nodes(), final_colour_map)}

            plt.subplot(2, 3, i + 1)
            nx.draw(graph, pos, node_color=list(initial_colour_map.values()), with_labels=True, node_size=500)
            plt.title(f'Initial Color Map for {topology} Topology')

            plt.subplot(2, 3, i + 4)
            nx.draw(graph, pos, node_color=list(final_colour_map_dict.values()), with_labels=True, node_size=500)
            plt.title(f'Final Color Map for {topology} Topology')

            # Apply decentralised graph colouring algorithm to get conflict history
            _, conflict_history = decentralised_graph_colouring(graph, colours)
            conflict_histories.append(conflict_history)

        except ValueError as e:
            print(e)

    plt.tight_layout()
    plt.show()

    # Plot combined conflict history
    plt.figure(figsize=(10, 6))
    colours = ['blue', 'red', 'green']
    plt.title('Convergence of Decentralised Graph Colouring Algorithm')
    max_iterations = max(len(history) for history in conflict_histories)
    for i, history in enumerate(conflict_histories):
        normalised_history = [history[j] if j < len(history) else history[-1] for j in range(max_iterations)]
        plt.plot(range(len(normalised_history)), normalised_history, label=topology_names[i], color=colours[i])
    
    plt.xlabel('Iterations')
    plt.ylabel('Number of Conflicts')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()