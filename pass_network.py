import pandas as pd
from statsbombpy import sb
import matplotlib.pyplot as plt
import networkx as nx

from mplsoccer import Pitch
import numpy as np
from matplotlib.patches import FancyArrowPatch


def get_passes_from_player(match_id, player_name):
    # Load events for a match
    events = sb.events(match_id=match_id)

    # Filter for passes made by the player
    passes = events[(events['type'] == 'Pass') & (events['player'] == player_name)]

    # Filter for successful passes
    successful_passes = passes[passes['pass_outcome'].isna()]

    return successful_passes


def count_passes_by_recipient(passes):
    # Count the number of passes to each recipient
    pass_counts = passes['pass_recipient'].value_counts()
    return pass_counts


# def plot_pass_counts(pass_counts, player_name):
#     # Plot a bar chart of pass counts
#     plt.figure(figsize=(12, 8))
#     pass_counts.plot(kind='bar', color='red')
#     plt.title(f'Total Passes from {player_name} by Recipient')
#     plt.xlabel('Recipient Player')
#     plt.ylabel('Number of Passes')
#     plt.xticks(rotation=45, ha='right')
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
#     plt.tight_layout()
#     plt.show()


def plot_pass_network(pass_counts, player_name, bg_color='white'):
    # Create a directed graph for the pass network
    G = nx.DiGraph()

    # Add edges with weights (pass counts)
    for recipient, count in pass_counts.items():
        G.add_edge(player_name, recipient, weight=count)

    # Draw the graph
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))
    plt.gca().set_facecolor(bg_color)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=8, font_weight='bold',
            edge_color='red', width=[G[u][v]['weight'] / 2 for u, v in G.edges()])
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{d["weight"]}' for u, v, d in G.edges(data=True)},
                                 font_color='black')
    plt.title(f'Pass Network from {player_name}')
    plt.show()


# Example usage
match_id = 3942382  # Replace with the match ID you are interested in
player_name = 'Arda Güler'  # Replace with the player name you are interested in
passes = get_passes_from_player(match_id, player_name)
pass_counts = count_passes_by_recipient(passes)
# plot_pass_counts(pass_counts, player_name)
plot_pass_network(pass_counts, player_name,  bg_color='lightgreen')