from statsbombpy import sb
import streamlit as st
import passes_to_area, key_passes, pass_to_xg

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
    if 'match_id_list' not in st.session_state:
        st.session_state.match_id_list = []


def user_input_form():
    with st.form("input_form"):
        league_list = ['Euro Cup 2024', 'Copa America 2024']

        league_selection = st.selectbox("Select a competition:", league_list)
        competition_submitted = st.form_submit_button("Submit competition")

    if competition_submitted:
        comp_id, season_id = (55, 282) if league_selection == 'Euro Cup 2024' else (223, 282)
        st.session_state.competition_id_input = comp_id
        st.session_state.season_id_input = season_id
        st.session_state.step = 2
        st.rerun()


def select_team_form():
    all_matches = sb.matches(competition_id=st.session_state.competition_id_input,
                             season_id=st.session_state.season_id_input)
    team_set = set(all_matches['home_team'].unique()) | set(all_matches['away_team'].unique())

    with st.form(key='selection_form'):
        team_name = st.selectbox("Select an option:", sorted(team_set))
        submit_selection_button = st.form_submit_button("Submit Selection")
    if submit_selection_button:
        st.session_state.selection = team_name
        st.session_state.step = 3
        st.rerun()


def select_player():
    all_matches = sb.matches(competition_id=st.session_state.competition_id_input,
                             season_id=st.session_state.season_id_input)
    team_matches = all_matches[(all_matches['home_team'] == st.session_state.selection) | (
                all_matches['away_team'] == st.session_state.selection)]

    player_set = set()
    for match_id in team_matches['match_id']:
        events = sb.events(match_id=match_id)
        team_events = events[events['team'] == st.session_state.selection]
        players = team_events['player'].dropna().unique()
        player_set.update(players)
        if match_id not in st.session_state.match_id_list:
            st.session_state.match_id_list.append(match_id)
            # st.session_state.matches_dict[match_id] = f"{events.iloc[0]['home_team']} - {events.iloc[0]['away_team']}"

    with st.form(key='select_a_player_form'):
        sorted_player_set = sorted(player_set)
        player_selection = st.selectbox("Select a player:", sorted_player_set)
        submit_selection_button = st.form_submit_button("Submit Selection")

    if submit_selection_button:
        st.session_state.player = player_selection
        st.session_state.step = 4
        st.rerun()


def reset_button():
    if st.button("Start Over"):
        st.session_state.step = 1
        st.session_state.user_input = ''
        st.session_state.selection = ''
        st.session_state.match_id_list = []
        # st.session_state.matches_dict = {}
        st.rerun()


def main(selection):
    if selection == "Pass to xG":
        st.title("Pass & Xg Creation Chart")
        initialize_session_state()
        if st.session_state.step == 1:
            user_input_form()
        elif st.session_state.step == 2:
            select_team_form()
        elif st.session_state.step == 3:
            pass_to_xg.country_pass_to_xg_result()
    elif selection in ["Player Passes", "Player Key Passes"]:
        st.title("Player Passes")
        initialize_session_state()
        if st.session_state.step == 1:
            user_input_form()
        elif st.session_state.step == 2:
            select_team_form()
        elif st.session_state.step == 3:
            select_player()
        elif st.session_state.step == 4:
            st.write(f"You selected team: {st.session_state.selection}")
            st.write(f"You selected player: {st.session_state.player}")
            # Conditionally run functions based on the type of analysis selected
            if selection == "Player Passes":
                passes_to_area.get_passes(st.session_state.match_id_list, st.session_state.player)
            elif selection == "Player Key Passes":
                key_passes.key_passes_method(st.session_state.match_id_list, st.session_state.player)

    reset_button()


if __name__ == "__main__":
    main()
    # select_player(55, 282, 'Turkey')
