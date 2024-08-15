import streamlit as st
import streamlit_competition_selection


def menu_selection():
    pages = {
        "Home": "Welcome Here!",
        "Pass to xG": "Passes to create a xG!",
        "Player Passes": "Player's passes analysis",
        "Player Key Passes": "Player's passes to converted into shots analysis"
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
    elif selection == "Player Passes" or selection == "Player Key Passes":
        streamlit_competition_selection.main(selection)
        # all_passes_on_the_pitch.start()



if __name__ == '__main__':
    menu_selection()