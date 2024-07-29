

import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen

from statsbombpy import sb

def draw_player_pass_to_shot(passes, matches_dict):
    pitch = Pitch(line_color='white', pitch_color='#02540b', pad_top=20)
    fig, ax = pitch.draw(figsize=(10, 7))

    for i, thepass in passes.iterrows():
        x = thepass['location'][0]
        y = thepass['location'][1]
        # plot circle
        passCircle = plt.Circle((x, y), 2, color="white")
        passCircle.set_alpha(.2)
        ax.add_patch(passCircle)

        dx = thepass['pass_end_location'][0] - x
        dy = thepass['pass_end_location'][1] - y
        # plot arrow
        if thepass['pass_outcome'] != 'Incomplete':
            passArrow = plt.Arrow(x, y, dx, dy, width=1, color="yellow")
            ax.add_patch(passArrow)
        # else:
        #     passArrow = plt.Arrow(x, y, dx, dy, width=1, color="blue")
        #     ax.add_patch(passArrow)
        # plt.annotate(thepass['shot_statsbomb_xg'], xy=(x, y))

    ax.set_title("from arda passes to", fontsize=24)
    fig.set_size_inches(10, 7)
    plt.show()

    # all_matches_seperate_pass_map(passes)
    passes_separately(passes, matches_dict)


def all_matches_seperate_pass_map(events):
    # pitch = all_passes(events)
    # passes_seperately(events, pitch)
    passes_separately(events)


def passes_separately(passes, matches_dict):
    pitch = Pitch(line_color='white', pitch_color='#02540b', pad_top=20)
    fig, axs = pitch.grid(ncols=2, nrows=3, grid_height=0.85, title_height=0.06, axis=False,
                          endnote_height=0.04, title_space=0.04, endnote_space=0.01)

    match_ids = passes['match_id'].unique()
    for match, ax in zip(match_ids, axs['pitch'].flat[:len(match_ids)]):
        # put match_id over the plot
        ax.text(60, -10, matches_dict.get(match),
                ha='center', va='center', fontsize=8)
        # take only passes by this player, for now its already only Neymar's passes.
        player_df = passes.loc[passes["match_id"] == match]

        # scatter
        pitch.scatter(player_df.x, player_df.y, alpha=0.2, s=50, color="blue", ax=ax)

        # plot arrow
        goal_df = player_df.loc[player_df["pass_outcome"] != 'Incomplete']
        pitch.arrows(goal_df.x, goal_df.y,
                     goal_df.end_x, goal_df.end_y, color="yellow", ax=ax, width=1)

        non_goal_df = player_df.loc[player_df["pass_outcome"] == 'Incomplete']
        pitch.arrows(non_goal_df.x, non_goal_df.y,
                     non_goal_df.end_x, non_goal_df.end_y, color="red", ax=ax, width=1)

        # plt.annotate(player_df['shot_statsbomb_xg'], xy=(player_df.x, player_df.y))

    # We have more than enough pitches - remove them
    for ax in axs['pitch'][-1, 16 - len(match_ids):]:
        ax.remove()
    # Another way to set title using mplsoccer
    axs['title'].text(0.5, 0.5, 'Neymar passes converted to shot, every game', ha='center', va='center', fontsize=24)
    plt.show()


def all_passes(events):
    plt.rcParams.update({'figure.max_open_warning': 0})
    pitch = Pitch(line_color='white', pitch_color='#02540b', pad_top=20)
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                         endnote_height=0.04, title_space=0, endnote_space=0)
    goal_df = events.loc[events["pass_outcome"] != 'Incomplete']
    non_goal_df = events.loc[events["pass_outcome"] == 'Incomplete']
    pitch.arrows(goal_df.x, goal_df.y,
                 goal_df.end_x, goal_df.end_y, color="yellow", ax=ax['pitch'])
    # pitch.arrows(non_goal_df.x, non_goal_df.y,
    #              non_goal_df.end_x, non_goal_df.end_y, color="red", ax=ax['pitch'])
    pitch.scatter(events.x, events.y, alpha=0.2, s=500, color="purple", ax=ax['pitch'])
    fig.suptitle("Lucy Bronze passes against Sweden", fontsize=30)
    plt.show()
    return pitch
