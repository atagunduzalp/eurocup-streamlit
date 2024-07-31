import pandas as pd
from statsbombpy import sb
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from matplotlib.patches import FancyArrowPatch
import pass_map


match_passes_dict = {}

def get_player_pass_network(match_id_list, player_name):
    # Load events for a match
    all_passes = pd.DataFrame()

    for match in match_id_list:
        events = sb.events(match_id=match)
    # Filter for passes made by the player
        passes = events[(events['type'] == 'Pass') & (events['player'] == player_name)]
    # Filter for successful passes
        successful_passes = passes[passes['pass_outcome'].isna()]
        all_passes = pd.concat([all_passes, successful_passes])
        match_passes_dict[match] = all_passes

    # for match_id, match_passes in match_passes_dict.items():


    return all_passes


def plot_passes(match_passes, match_id):
    pitch = Pitch(line_color='black')
    fig, ax = plt.subplots(figsize=(10, 7))
    pitch.draw(ax=ax)

    # Plot arrows for each pass
    for idx, row in match_passes.iterrows():
        start_x, start_y = row['location']
        end_x, end_y = row['pass_end_location']
        pitch.arrows(start_x, start_y, end_x, end_y,
                     width=2, headwidth=5, headlength=5, color='blue', ax=ax)
        ax.text(end_x, end_y, row['pass_recipient'], fontsize=12, color='red')

    ax.set_title(f'Arda Güler Passes - Match {match_id}', fontsize=20)
    plt.show()

# Plot for each match separately
for match_id, match_passes in match_passes_dict.items():
    plot_passes(match_passes, match_id)


def plot_pass_network(passes):
    # Create a football pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white', stripe=False)
    fig, ax = pitch.draw(figsize=(10, 7))

    # Plot each pass with arrows and player names
    for i, row in passes.iterrows():
        x_start, y_start = row['location']
        x_end, y_end = row['pass_end_location']
        pass_recipient = row['pass_recipient']

        # Draw pass arrow
        arrow = FancyArrowPatch((x_start, y_start), (x_end, y_end), color='blue', arrowstyle='->', mutation_scale=10,
                                lw=2, zorder=1)
        ax.add_patch(arrow)

        # Draw start and end positions
        pitch.scatter(x_start, y_start, s=100, color='red', ax=ax, zorder=2)
        pitch.scatter(x_end, y_end, s=100, color='yellow', ax=ax, zorder=2)

        # Annotate recipient name at end position
        pitch.annotate(pass_recipient, xy=(x_end, y_end), ax=ax, fontsize=10, ha='center', va='center', color='black',
                       zorder=3)

    plt.title('Pass Network with Recipients')
    plt.show()
    st.pyplot(plt.gcf())


def start(player_name, match_id_list):
    # print("player name: " + str(player_name))
    # print("match id list: " + str(match_id_list))
    # print("ata")
    # match_id = 3942382  # Replace with the match ID you are interested in
    # player_name = 'Arda Güler'  # Replace with the player name you are interested in
    passes = get_player_pass_network(match_id_list, player_name)
    # plot_pass_network(passes)
    pass_map.draw_player_pass_to_shot(passes, {'3942382': 'austria'})

match_id_list  =[]
all_matches = sb.matches(competition_id=55,
                             season_id=282)
team_matches = all_matches[(all_matches['home_team'] == 'Turkey') | (all_matches['away_team'] == 'Turkey')]
for match_id in team_matches['match_id']:
    match_id_list.append(match_id)
# pass_list = ['3942382', '3930184']
start("Arda Güler", match_id_list)