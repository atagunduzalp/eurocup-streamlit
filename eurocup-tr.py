from statsbombpy import sb
import pandas as pd
import streamlit as st

import pass_viz
import pass_map

# bundesliga

# all_matches = sb.matches(competition_id=9, season_id=27)

# la liga

# pass_map.draw_pass_picth('Neymar da Silva Santos Junior',all_matches)

def streamlit_version():
    st.text("Bundesliga 2015/2016 --> competition id: 9, season id:27")
    st.text("La Liga 2015/2016 --> competition id: 11, season id:27")
    st.text("Euro Cup 2024 --> competition id: 55, season id:282")
    with st.form("my_form"):
        competition_id_input = st.number_input("competition id: ", value=55)
        season_id_input = st.number_input("season id: ", value=282)
        submitted = st.form_submit_button("Submit")
        if submitted:
            analysis(competition_id_input, season_id_input)

def analysis(competition_id, season_id):
    all_matches = sb.matches(competition_id=competition_id, season_id=season_id)
    team_set = set()
    home_teams = all_matches['home_team'].unique()
    for team in home_teams:
        team_set.add(team)
    away_teams = all_matches['away_team'].unique()
    for team in away_teams:
        team_set.add(team)
    print(team_set)
    pd.set_option('display.max_columns', None)
    player_dict = {}
    player_pass_count_dict = {}
    xg_dict = {}

    turkey_matches = all_matches[(all_matches['home_team'] == 'Turkey') | (all_matches['away_team'] == 'Turkey')]
    # neymar_passes = pd.DataFrame()
    # print(len(barca_matches))
    # for match in barca_matches['match_id']:
    for match in turkey_matches['match_id']:
        events = sb.events(match_id=match)

        shots = events[events['type'] == 'Shot'][
            ['match_id', 'id', 'team', 'player', 'shot_statsbomb_xg', 'shot_key_pass_id', 'shot_outcome']]
        passes = events[events['type'] == 'Pass'][['id', 'player', 'location', 'pass_end_location']]

        pass_shot_merged_df = pd.merge(shots, passes, how='left', left_on=['shot_key_pass_id'],
                                       right_on=['id']).dropna()
        pass_to_create_xg = pass_shot_merged_df[
            ['match_id', 'team', 'player_y', 'shot_statsbomb_xg', 'shot_outcome', 'location',
             'pass_end_location']]
        pass_to_create_xg = pass_to_create_xg[pass_to_create_xg['team'] == 'Turkey']
        # player specific
        # pass_to_create_xg = pass_to_create_xg[pass_to_create_xg['player_y'] == 'Neymar da Silva Santos Junior']
        #
        for player_name, xg in zip(pass_to_create_xg.player_y, pass_to_create_xg.shot_statsbomb_xg):
            # print(player_name)
            # print(xg)
            if player_name in player_dict:
                player_dict[player_name]['xg'] = player_dict.get(player_name)['xg'] + xg
                player_dict[player_name]['pass_count'] += 1
            else:
                player_dict[player_name] = {}
                player_dict[player_name]['xg'] = xg
                player_dict[player_name]['pass_count'] = 1
        # neymar_passes = neymar_passes._append(pass_to_create_xg, ignore_index = True)

    # neymar_passes[['x', 'y']] = pd.DataFrame(neymar_passes.location.tolist(), index=neymar_passes.index)
    # neymar_passes[['end_x', 'end_y']] = pd.DataFrame(neymar_passes.pass_end_location.tolist(), index=neymar_passes.index)
    # pass_map.draw_player_pass_to_shot(neymar_passes)

    # sorted_dict = dict(sorted(player_dict.items(), reverse=True, key=lambda item: item[1]))
    # print(sorted_dict)
    #
    # player_pass_count_dict_sorted = dict(sorted(player_pass_count_dict.items(), reverse=True, key=lambda item: item[1]))
    # print(player_pass_count_dict_sorted)
    # print(player_pass_count_dict_sorted)

    # sorted_dict = dict(sorted(player_dict.items(), reverse=True, key=lambda item: item[1]))
    print(player_dict)
    # sorted_list_by_xg = sorted(player_dict, reverse=True, key=lambda x: (player_dict[x]['xg']))
    # print(sorted_list_by_xg)

    sorted_by_xg = dict(sorted(player_dict.items(), reverse=True, key=lambda x: (x[1]["xg"])))
    print(sorted_by_xg)
    sorted_by_xg_per_pass = dict(
        sorted(player_dict.items(), reverse=True, key=lambda x: (x[1]["xg"] / x[1]["pass_count"])))
    print(sorted_by_xg_per_pass)
    # st.write(sorted_by_xg_per_pass)
    pass_viz.draw_pass_xg(sorted_by_xg_per_pass)


if __name__ == '__main__':
    analysis(55, 282)
    # streamlit_version()





