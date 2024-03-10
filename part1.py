import networkx as nx
import random
import matplotlib.pyplot as plt

def decentralised_graph_colouring(graph, colours, max_iterations=100):
    colour_map = {}

    # Randomly assign colours to each node
    for node in graph.nodes():
        colour_map[node] = random.choice(colours)

    # Count initial conflicts
    initial_conflicts = count_conflicts(graph, colour_map)

    # Store initial colour map
    initial_colour_map = colour_map.copy()

    conflict_history = [initial_conflicts]  # Store conflicts
    iterations = 0

    while initial_conflicts > 0 and iterations < max_iterations:
        node = random.choice(list(graph.nodes()))  # Select a random node
        neighbours = list(graph.neighbors(node))  # Get neighbours of the node
        neighbour_colours = [colour_map[n] for n in neighbours]  # Get colours of neighbours

        # Find available colours that minimise conflicts
        available_colours = [c for c in colours if c not in neighbour_colours]

        if available_colours:
            new_colour = min(available_colours, key=lambda x: neighbour_colours.count(x))
            colour_map[node] = new_colour
            initial_conflicts = count_conflicts(graph, colour_map)
            conflict_history.append(initial_conflicts)  # Update conflict history
        else:
            break  
        
        iterations += 1

    return initial_colour_map, colour_map, conflict_history

def count_conflicts(graph, colour_map):
    conflicts = 0
    for edge in graph.edges():
        if colour_map[edge[0]] == colour_map[edge[1]]:
            conflicts += 1
    return conflicts

def plot_combined(graph, initial_colour_map, final_colour_map, conflict_history):
    plt.figure(figsize=(18, 6))

    # Generate layout for the graph
    pos = nx.spring_layout(graph)

    # Plot initial color map
    plt.subplot(1, 3, 1)
    node_colors_initial = [initial_colour_map[node] for node in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_color=node_colors_initial, node_size=500)
    plt.title('Initial Graph Colouring')

    # Plot final color map
    plt.subplot(1, 3, 2)
    node_colors_final = [final_colour_map[node] for node in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_color=node_colors_final, node_size=500)
    plt.title('Final Graph Colouring')

    # Plot conflict history
    plt.subplot(1, 3, 3)
    plt.plot(range(len(conflict_history)), conflict_history)
    plt.xlabel('Iterations')
    plt.ylabel('Number of Conflicts')
    plt.title('Convergence of Decentralised Graph Colouring Algorithm')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Generate random regular graph with 20 nodes and degree of 4
    graph = nx.random_regular_graph(4, 20)
    colours = ['red', 'yellow', 'blue', 'green', 'pink']  

    # Apply decentralised graph colouring algorithm
    initial_colour_map, final_colour_map, conflict_history = decentralised_graph_colouring(graph, colours)

    # Print initial and final colour maps
    print("Initial Colour Map:")
    print(initial_colour_map)
    print("\nFinal Colour Map:")
    print(final_colour_map)

    # Plot combined graph
    plot_combined(graph, initial_colour_map, final_colour_map, conflict_history)
