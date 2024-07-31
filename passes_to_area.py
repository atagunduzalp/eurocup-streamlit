import pandas as pd
from statsbombpy import sb
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np
import streamlit as st
from matplotlib import cm


def get_passes(match_id_list, player_name):
    print(player_name)
    print(match_id_list)

    all_passes = pd.DataFrame()

    for match in match_id_list:
        events = sb.events(match_id=match)
        # Filter for passes made by the player
        passes = events[(events['type'] == 'Pass') & (events['player'] == player_name)]
        # Filter for successful passes
        successful_passes = passes[passes['pass_outcome'].isna()]
        all_passes = pd.concat([all_passes, successful_passes])
        # match_passes_dict[match] = all_passes
    calculate_area_percentages(all_passes, player_name)
    return all_passes
    # return passes

def calculate_area_percentages(passes, player_name):
    # Divide the pitch into 12 equal areas (3 vertical x 4 horizontal)
    pitch_length = 120
    pitch_width = 80

    # Extract end locations of the passes
    pass_end_location = pd.DataFrame(passes['pass_end_location'].tolist(), index=passes.index,
                                     columns=['x_end', 'y_end'])
    passes = pd.concat([passes, pass_end_location], axis=1)

    # Determine which area each pass ends in
    bins_x = np.linspace(0, pitch_length, 4)  # 3 vertical divisions
    bins_y = np.linspace(0, pitch_width, 5)  # 4 horizontal divisions

    passes['area'] = pd.cut(passes['x_end'], bins_x, labels=False, include_lowest=True) + \
                     pd.cut(passes['y_end'], bins_y, labels=False, include_lowest=True) * 3

    # Calculate the percentage of passes in each area
    # area_counts = passes['area'].value_counts(normalize=True).sort_index() * 100

    area_counts = passes['area'].value_counts().sort_index()
    total_passes = area_counts.sum()
    area_percentages = area_counts / total_passes * 100

    plot_area_percentages(area_counts, area_percentages, bins_x, bins_y, player_name)
    return area_counts, bins_x, bins_y


def plot_area_percentages(area_counts, area_percentages, bins_x, bins_y, player_name):
    # Create a football pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white', stripe=False)
    fig, ax = pitch.draw(figsize=(12, 8))

    norm = plt.Normalize(area_percentages.min(), area_percentages.max())

    # Create a colormap (single color gradient)
    cmap = cm.coolwarm

    # Sort areas by percentage
    sorted_areas = area_counts.sort_values()

    # Identify best 3 and worst 3 areas
    best_3 = sorted_areas[-4:].index
    worst_3 = sorted_areas[:4].index

    # Plot areas and their percentages
    for i in range(3):
        for j in range(4):
            area_index = i + j * 3
            if area_index in area_percentages.index:
                percentage = area_percentages[area_index]
                count = area_counts[area_index]
                color = cmap(norm(percentage))
            else:
                percentage = 0.0
                count = 0
                color = 'none'

            x_left = bins_x[i]
            x_right = bins_x[i + 1]
            y_bottom = bins_y[j]
            y_top = bins_y[j + 1]
            x_center = (x_left + x_right) / 2
            y_center = (y_bottom + y_top) / 2

            # Draw the area rectangle with color
            rect = plt.Rectangle((x_left, y_bottom), x_right - x_left, y_top - y_bottom,
                                 linewidth=1, edgecolor='white', facecolor=color, linestyle='--', alpha=0.5)
            ax.add_patch(rect)

            # Annotate the percentage inside the rectangle

            pitch.annotate(f'{percentage:.1f}%\n({count})', xy=(x_center, y_center), ax=ax, fontsize=12, ha='center',
                           va='center', color='black', zorder=3)

            ax.annotate('Attack', xy=(50, 100), xytext=(50, 110),
                        arrowprops=dict(facecolor='red', shrink=0.05),
                        fontsize=12, ha='center')

    print('plt: ' +str(player_name))
    plt.title(f'Percentage of Passes Received in Each Area\n{player_name}'
              '→ Attack Direction', fontsize=16, ha='center', va='center')
    ax.annotate('', xy=(120, 40), xytext=(0, 40),
                arrowprops=dict(facecolor='red', shrink=0.05, width=2, headwidth=10, headlength=10),
                fontsize=12, ha='center', va='center', zorder=4)
    plt.tight_layout()

    plt.show()
    st.pyplot(plt.gcf())


# Example usage
# match_id = 3942382  # Replace with the match ID you are interested in
# player_name = 'Arda Güler'  # Replace with the player name you are interested in

# match_id_list  =[]
# all_matches = sb.matches(competition_id=55,
#                              season_id=282)
# team_matches = all_matches[(all_matches['home_team'] == 'Turkey') | (all_matches['away_team'] == 'Turkey')]
# for match_id in team_matches['match_id']:
#     match_id_list.append(match_id)
# passes = get_passes(match_id_list, player_name)
#
# area_counts, bins_x, bins_y = calculate_area_percentages(passes)
# plot_area_percentages(area_counts, bins_x, bins_y)


