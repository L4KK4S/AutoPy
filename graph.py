import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from automaton import Automaton


def graph(automaton):

    # Créer un graphe
    G = nx.DiGraph()

    # Ajouter des arêtes pondérées avec des attributs différents
    for transition in automaton.transitions:
        for charactere in transition:
            if charactere.isalpha():
                l = transition.split(charactere)
                l.append(charactere)
        for i in range(len(l)):
            if l[i] == "-2":
                l[i] = "I"
        G.add_edge(l[0], l[1], label=l[2])

    # Positionnement des nœuds
    pos = nx.spring_layout(G)

    # Coloration des nœuds

    active_states = automaton.states.copy()
    active_states = [state for state in active_states if state.get_value() in G.nodes()]
    if "I" in G.nodes():
        active_states.append(automaton.states[0])

    node_colors = [""] * len(G.nodes())
    for node in G.nodes():
        for i, state in enumerate(active_states):
            if state.get_value() == node or "I" == node:
                if state.is_initial and state.is_terminal:
                    node_colors[i] = 'violet'                    # etat initial et terminal
                elif state.is_initial:
                    node_colors[i]  = 'green'                    # etat initial
                elif state.is_terminal:
                    node_colors[i]  = 'red'                      # etat terminal
                else:
                    node_colors[i]  = 'blue'                     # etat normal

    # Dessiner les nœuds
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors)

    # Dessiner les arêtes
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, width=2)

    # Ajouter les étiquettes des relations sur les arêtes avec plusieurs attributs
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Ajouter les numéros sur les nœuds
    node_labels = {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    # Afficher le graphe
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    automaton1 = Automaton("bob.txt")
    automaton1.standardize()
    graph(automaton1)
