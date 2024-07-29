from statsbombpy import sb
import pandas as pd
import streamlit as st

from mplsoccer import Pitch, Sbopen
from mplsoccer import VerticalPitch,Pitch

import matplotlib.pyplot as plt

def draw_pass_xg(your_dict):
    inner_keys = list(your_dict.values())[0].keys()

    # x-axis is the outer keys
    labels = list(map(str, your_dict.keys()))
    # loop through inner_keys
    y_axis_values = []
    x_axis_values = []
    for x in inner_keys:
        # create a list of values for inner key
        if x == 'pass_count':
            y_axis_values = [v[x] for v in your_dict.values()]
        if x == 'xg':
            x_axis_values = [v[x] for v in your_dict.values()]

        # plot each inner key

    plt.rcParams["font.size"] = "4"
    fig, ax = plt.subplots()
    ax.scatter(x_axis_values, y_axis_values)
    for i, txt in enumerate(labels):
        ax.annotate(txt, (x_axis_values[i], y_axis_values[i]))
    # plt.show()

    plt.ylabel('pass_count', fontsize=9)
    plt.xlabel('xg', fontsize=9)
    plt.scatter(x_axis_values, y_axis_values, label=labels, color='green')

    # plt.legend()
    # plt.figure(figsize=(8, 8))
    plt.savefig('pass_to_xg.pdf')
    plt.show()
    st.pyplot(plt.gcf())



