from statsbombpy import sb
import pandas as pd
import streamlit as st

import pass_viz


def country_pass_to_xg_result():

    pd.set_option('display.max_columns', None)
    player_dict = {}
    player_pass_count_dict = {}
    xg_dict = {}
    country_selection = st.session_state.selection
    all_matches = sb.matches(competition_id=st.session_state.competition_id_input,
                             season_id=st.session_state.season_id_input)

    for match in all_matches['match_id']:
        events = sb.events(match_id=match)

        shots = events[events['type'] == 'Shot'][
            ['match_id', 'id', 'team', 'player', 'shot_statsbomb_xg', 'shot_key_pass_id', 'shot_outcome']]
        passes = events[events['type'] == 'Pass'][['id', 'player', 'location', 'pass_end_location']]

        pass_shot_merged_df = pd.merge(shots, passes, how='left', left_on=['shot_key_pass_id'],
                                       right_on=['id']).dropna()
        pass_to_create_xg = pass_shot_merged_df[
            ['match_id', 'team', 'player_y', 'shot_statsbomb_xg', 'shot_outcome', 'location',
             'pass_end_location']]

        if country_selection != 'all':
            pass_to_create_xg = pass_to_create_xg[pass_to_create_xg['team'] == country_selection]
        for player_name, xg in zip(pass_to_create_xg.player_y, pass_to_create_xg.shot_statsbomb_xg):
            if player_name in player_dict:
                player_dict[player_name]['xg'] = player_dict.get(player_name)['xg'] + xg
                player_dict[player_name]['pass_count'] += 1
            else:
                player_dict[player_name] = {}
                player_dict[player_name]['xg'] = xg
                player_dict[player_name]['pass_count'] = 1

    sorted_by_xg = dict(sorted(player_dict.items(), reverse=True, key=lambda x: (x[1]["xg"])))
    print(sorted_by_xg)
    sorted_by_xg_per_pass = dict(
        sorted(player_dict.items(), reverse=True, key=lambda x: (x[1]["xg"] / x[1]["pass_count"])))
    print(sorted_by_xg_per_pass)
    # st.write(sorted_by_xg_per_pass)
    pass_viz.draw_pass_xg(sorted_by_xg_per_pass)