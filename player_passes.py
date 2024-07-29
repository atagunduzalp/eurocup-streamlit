from statsbombpy import sb
import pandas as pd
import streamlit as st

import pass_map

# all_matches = sb.matches(competition_id=55, season_id=282)
# turkey_matches = all_matches[(all_matches['home_team'] == 'Turkey') | (all_matches['away_team'] == 'Turkey')]


def player_pass(turkey_matches, player_name ):
    player_pass_df = pd.DataFrame()
    matches_dict = {}

    for match in turkey_matches['match_id']:

        home_team = turkey_matches[turkey_matches['match_id'] == match]['home_team']
        away_team = turkey_matches[turkey_matches['match_id'] == match]['away_team']
        matches_dict[match] = home_team.iloc[0] + " - " + away_team.iloc[0]

        events = sb.events(match_id=match)
        passes = events[events['type'] == 'Pass'][['match_id', 'id', 'player', 'pass_recipient', 'location', 'pass_end_location', 'pass_outcome']]

        passes_arda = passes[passes['player'] == player_name]
        player_pass_df = player_pass_df._append(passes_arda, ignore_index=True)


    print(matches_dict)
    player_pass_df[['x', 'y']] = pd.DataFrame(player_pass_df.location.tolist(), index=player_pass_df.index)
    player_pass_df[['end_x', 'end_y']] = pd.DataFrame(player_pass_df.pass_end_location.tolist(), index=player_pass_df.index)
    pass_map.draw_player_pass_to_shot(player_pass_df, matches_dict)



