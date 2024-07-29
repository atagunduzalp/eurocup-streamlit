from statsbombpy import sb
import pandas as pd
import streamlit as st
import pass_to_xg
import pass_viz
import pass_map
import all_passes_on_the_pitch
import passes_to_area


match_id_list = []
matches_dict = {}


# def league_infos():
    # st.text("Bundesliga 2015/2016 --> competition id: 9, season id:27")
    # st.text("La Liga 2015/2016 --> competition id: 11, season id:27")
    # st.text("Euro Cup 2024 --> competition id: 55, season id:282")
    # st.text("Copa America 2024 --> competition id: 223, season id:282")


def initialize_session_state():
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''
    if 'selection' not in st.session_state:
        st.session_state.selection = ''
    if 'player' not in st.session_state:
        st.session_state.player = ''


def user_input_form():
    with st.form("input_form"):
        league_list = ['Euro Cup 2024', 'Copa America 2024']

        league_selection = st.selectbox("Select a competition:", league_list)
        # competition_id_input = st.number_input("competition id: ", value=55)
        # season_id_input = st.number_input("season id: ", value=282)
        competition_submitted = st.form_submit_button("Submit competition")

    if competition_submitted:
        if league_selection == 'Euro Cup 2024':
            st.session_state.competition_id_input = 55
            st.session_state.season_id_input = 282
            st.session_state.step = 2
        elif league_selection == 'Euro Cup 2024':
            st.session_state.competition_id_input = 223
            st.session_state.season_id_input = 282
            st.session_state.step = 2
        st.rerun()


def select_team_form():
    all_matches = sb.matches(competition_id=st.session_state.competition_id_input,
                             season_id=st.session_state.season_id_input)
    team_set = set()
    home_teams = all_matches['home_team'].unique()
    team_set.add("All")
    for team in home_teams:
        team_set.add(team)
    away_teams = all_matches['away_team'].unique()
    for team in away_teams:
        team_set.add(team)

    with st.form(key='selection_form'):
        team_name = st.selectbox("Select an option:", sorted(team_set))
        submit_selection_button = st.form_submit_button("Submit Selection")
    if submit_selection_button:
        st.session_state.selection = team_name
        st.session_state.step = 3
        st.rerun()


# def select_player(competition_id, season_id, team):
def select_player(match_id_list):
    all_matches = sb.matches(competition_id=st.session_state.competition_id_input,
                             season_id=st.session_state.season_id_input)
    print(st.session_state.selection)
    team_matches = all_matches[(all_matches['home_team'] == st.session_state.selection) | (all_matches['away_team'] == st.session_state.selection)]
    for match in team_matches['match_id']:
        home_team = team_matches[team_matches['match_id'] == match]['home_team']
        away_team = team_matches[team_matches['match_id'] == match]['away_team']
        matches_dict[match] = home_team.iloc[0] + " - " + away_team.iloc[0]

        match_id_list.append(match)

    # all_matches = sb.matches(competition_id=competition_id, season_id=season_id)
    # team_matches = all_matches[(all_matches['home_team'] == team) | (
    #             all_matches['away_team'] == team)]

    player_set = set()
    for match in team_matches['match_id']:
        events = sb.events(match_id=match)
        team_events = events[events['team'] == st.session_state.selection]
        players = team_events['player'].unique()
        for player in players:
            if player not in player_set:
                player_set.add(player)
    print(player_set)
    with st.form(key='select_a_player_form'):
        # sorted_player_list = sorted(player_set)
        player_selection = st.selectbox("Select a player:", player_set)
        submit_selection_button = st.form_submit_button("Submit Selection")
    if submit_selection_button:
        st.session_state.player = player_selection
        st.session_state.step = 4
        st.rerun()

    return match_id_list, matches_dict


def reset_button():
    if st.button("Start Over"):
        st.session_state.step = 1
        st.session_state.user_input = ''
        st.session_state.selection = ''
        st.rerun()


def main(selection):
    # league_infos()

    if selection == "Pass to xG":
        st.title("Pass & Xg Creation Chart")
        initialize_session_state()
        if st.session_state.step == 1:
            user_input_form()
        elif st.session_state.step == 2:
            select_team_form()
        elif st.session_state.step == 3:

            st.write(f"You competition id: {st.session_state.competition_id_input}")
            st.write(f"You season id: {st.session_state.season_id_input}")
            st.write(f"You selected: {st.session_state.selection}")

            pass_to_xg.country_pass_to_xg_result()

    elif selection == "Player Passes":
        player_set = set()
        st.title("Player Passes")
        initialize_session_state()
        if st.session_state.step == 1:
            user_input_form()
        elif st.session_state.step == 2:
            select_team_form()
        elif st.session_state.step == 3:
            select_player(match_id_list)
        elif st.session_state.step == 4:
            st.write(f"You competition id: {st.session_state.competition_id_input}")
            st.write(f"You season id: {st.session_state.season_id_input}")
            st.write(f"You selected team: {st.session_state.selection}")
            st.write(f"You selected player: {st.session_state.player}")
            # all_passes_on_the_pitch.start(st.session_state.player, match_id_list, matches_dict)
            passes_to_area.get_passes(match_id_list, st.session_state.player)

    reset_button()


if __name__ == "__main__":
    main()
    # select_player(55, 282, 'Turkey')
