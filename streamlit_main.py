from statsbombpy import sb
import pandas as pd
import streamlit as st
import pass_to_xg
import pass_viz
import pass_map
import streamlit_competition_selection
import all_passes_on_the_pitch


def menu_selection():
    pages = {
        "Home": "Welcome Here!",
        "Pass to xG": "Passes to create a xG!",
        "Player Passes": "Player's passes analysis"
    }

    # Create a sidebar with a clickable list
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Display content based on the selection
    st.title(selection)
    st.write(pages[selection])

    # streamlit_competition_selection.main(selection)

    if selection == "Pass to xG":
        streamlit_competition_selection.main(selection)
    elif selection == "Player Passes":
        streamlit_competition_selection.main(selection)
        # all_passes_on_the_pitch.start()



if __name__ == '__main__':
    menu_selection()