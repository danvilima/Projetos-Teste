import streamlit as st
import random
from data import GROUPS

def init_state():
    # Initialize groups
    for g, teams in GROUPS.items():
        if f"group_{g}_1" not in st.session_state:
            st.session_state[f"group_{g}_1"] = None
        if f"group_{g}_2" not in st.session_state:
            st.session_state[f"group_{g}_2"] = None
        if f"group_{g}_3" not in st.session_state:
            st.session_state[f"group_{g}_3"] = None
            
    # Initialize third places selection
    if "selected_thirds" not in st.session_state:
        st.session_state["selected_thirds"] = []
        
    # Knockout stage
    if "knockout" not in st.session_state:
        st.session_state["knockout"] = {} # match_id -> winner team
    
    # Matching cache
    if "third_place_matching" not in st.session_state:
        st.session_state["third_place_matching"] = None

    # User Info
    if "user_name" not in st.session_state:
        st.session_state["user_name"] = ""


def randomize_group(g):
    teams = GROUPS[g].copy()
    random.shuffle(teams)
    st.session_state[f"group_{g}_1"] = teams[0]
    st.session_state[f"group_{g}_2"] = teams[1]
    st.session_state[f"group_{g}_3"] = teams[2]

def randomize_all():
    init_state()
    # Randomize groups
    for g in GROUPS.keys():
        randomize_group(g)
    
    # Randomize third places
    all_thirds = [(g, st.session_state[f"group_{g}_3"]) for g in GROUPS.keys()]
    random.shuffle(all_thirds)
    st.session_state["selected_thirds"] = all_thirds[:8]
    
    # We will trigger the knockout matching in the UI layer
    
def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()

def clear_subsequent_matches(match_id):
    """
    If a user changes a winner in an early round, we need to clear the team's path 
    in all subsequent rounds to prevent a team from magically appearing in the final.
    """
    from data import KNOCKOUT_BRACKET
    # A recursive or iterative clear logic
    def clear_recursive(m_id):
        # find matches that depend on m_id
        for round_name, matches in KNOCKOUT_BRACKET.items():
            for next_match_id, deps in matches.items():
                if m_id in deps:
                    if next_match_id in st.session_state["knockout"]:
                        del st.session_state["knockout"][next_match_id]
                    clear_recursive(next_match_id)
                    
    clear_recursive(match_id)

def set_knockout_winner(match_id, team):
    if st.session_state["knockout"].get(match_id) != team:
        st.session_state["knockout"][match_id] = team
        clear_subsequent_matches(match_id)
