import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import streamlit as st


def key_passes_method(team_matches, player):
    # global player_passes
    player_passes = pd.DataFrame()
    for match in team_matches:
        events = sb.events(match_id=match)

        shots = events[events['type'] == 'Shot'][
            ['match_id', 'id', 'team', 'player', 'shot_statsbomb_xg',
             'shot_key_pass_id', 'shot_outcome']]
        passes = events[events['type'] == 'Pass'][['id', 'player', 'location',
                                                   'pass_end_location']]

        pass_shot_merged_df = pd.merge(shots, passes, how='left',
                                       left_on=['shot_key_pass_id'], right_on=['id']).dropna()
        pass_to_create_xg = pass_shot_merged_df[['match_id', 'team', 'player_y',
                                                 'shot_statsbomb_xg', 'shot_outcome', 'location',
                                                 'pass_end_location']]

        pass_to_create_xg = pass_to_create_xg[pass_to_create_xg['player_y'] == player]
        player_passes = player_passes._append(pass_to_create_xg, ignore_index=True)

    if player_passes.empty or not (player_passes['shot_outcome'] == 'Goal').any():
        st.error(f"No key passes that resulted in a shot were found for {player}.")
        return
    show_key_passes_on_the_pitch(player_passes, player)


def show_key_passes_on_the_pitch(player_passes, player_name):

    pitch = Pitch(line_color='white', pitch_color='#02540b', pad_top=20)
    fig, ax = pitch.draw(figsize=(10, 7))
    player_passes[['x', 'y']] = pd.DataFrame(player_passes.location.tolist(), index=player_passes.index)
    player_passes[['end_x', 'end_y']] = pd.DataFrame(player_passes.pass_end_location.tolist(),
                                                     index=player_passes.index)
    for i, thepass in player_passes.iterrows():
        x = thepass['location'][0]
        y = thepass['location'][1]
        # plot circle

        # Daire çizimi (başlangıç noktası)
        xg_value = thepass['shot_statsbomb_xg']
        circle_size = xg_value * 8  # Daire boyutunu xG değeri ile orantılı hale getiriyoruz
        passCircle = plt.Circle((x, y), circle_size, color="black", alpha=0.4)
        ax.add_patch(passCircle)

        dx = thepass['pass_end_location'][0] - x
        dy = thepass['pass_end_location'][1] - y
        # plot arrow

        pass_color = "yellow" if thepass['shot_outcome'] == 'Goal' else "red"
        passArrow = plt.Arrow(x, y, dx, dy, width=3 if pass_color == "yellow" else 1.3, color=pass_color)
        ax.add_patch(passArrow)

        plt.annotate(round(thepass['shot_statsbomb_xg'], 2), xy=(x, y), fontsize=10, color='white')

        # Asist veya gol bilgisini gösterme
        legend_elements = [
            Line2D([0], [0], color='yellow', lw=3, label='Goal'),
            Line2D([0], [0], color='red', lw=1, label='Shot')
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=12, frameon=False)

    ax.set_title(f"{player_name} passes to key areas", fontsize=24)
    fig.set_size_inches(12, 10)
    plt.show()
    st.pyplot(plt.gcf())

