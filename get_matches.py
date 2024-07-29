from statsbombpy import sb
import pandas as pd
import streamlit as st

import pass_map
import player_passes

def get_matches(competition_id, season_id, player_name):
    all_matches = sb.matches(competition_id=competition_id, season_id=season_id)
    team_matches = all_matches[(all_matches['home_team'] == 'Turkey') | (all_matches['away_team'] == 'Turkey')]
    arda_passes = pd.DataFrame()
    matches_dict = {}

    player_passes.player_pass(team_matches, player_name)


if __name__ == '__main__':
    get_matches(55, 282, 'Arda Güler')
