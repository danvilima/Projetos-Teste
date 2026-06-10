import streamlit as st
from data import KNOCKOUT_BRACKET, R32_FIXED, GROUPS
from state_manager import set_knockout_winner

def get_r32_team(slot_name):
    # slot_name ex: "1º Grupo A", "2º Grupo B"
    parts = slot_name.split()
    pos = parts[0]
    group = parts[-1]
    
    if pos == "1º":
        return st.session_state[f"group_{group}_1"]
    elif pos == "2º":
        return st.session_state[f"group_{group}_2"]
    return None

def render_match_card(match_id, team_home, team_away, col, title="Match"):
    with col:
        st.markdown(f"<div class='match-card'><b>{title} {match_id}</b>", unsafe_allow_html=True)
        winner = st.session_state["knockout"].get(match_id)
        
        # Home team button
        t1_class = "selected" if winner == team_home and team_home else ""
        if st.button(team_home or "TBD", key=f"m_{match_id}_home", disabled=not team_home, use_container_width=True):
            set_knockout_winner(match_id, team_home)
            st.rerun()
            
        st.markdown("<div style='text-align: center; color: #888;'>vs</div>", unsafe_allow_html=True)
        
        # Away team button
        t2_class = "selected" if winner == team_away and team_away else ""
        if st.button(team_away or "TBD", key=f"m_{match_id}_away", disabled=not team_away, use_container_width=True):
            set_knockout_winner(match_id, team_away)
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

def render_knockout():
    st.markdown("<h2>Mata-mata</h2>", unsafe_allow_html=True)
    
    matching = st.session_state.get("third_place_matching")
    if not matching:
        st.warning("Complete a seleção de terceiros colocados para ver o mata-mata.")
        return

    cols = st.columns(5)
    
    # --- Round of 32 ---
    r32_matches = list(R32_FIXED.keys()) + list(matching.keys())
    r32_matches.sort()
    
    with cols[0]:
        st.markdown("<h4>16-avos</h4>", unsafe_allow_html=True)
        for mid in r32_matches:
            if mid in R32_FIXED:
                th = get_r32_team(R32_FIXED[mid][0])
                ta = get_r32_team(R32_FIXED[mid][1])
            else:
                from data import R32_THIRD_PLACE
                th = get_r32_team(R32_THIRD_PLACE[mid][0])
                ta = matching[mid]
            render_match_card(mid, th, ta, st, "R32")
            
    # --- Round of 16 ---
    with cols[1]:
        st.markdown("<h4>Oitavas</h4>", unsafe_allow_html=True)
        for mid, (m1, m2) in KNOCKOUT_BRACKET["R16"].items():
            th = st.session_state["knockout"].get(m1)
            ta = st.session_state["knockout"].get(m2)
            render_match_card(mid, th, ta, st, "R16")
            
    # --- Quarter Finals ---
    with cols[2]:
        st.markdown("<h4>Quartas</h4>", unsafe_allow_html=True)
        for mid, (m1, m2) in KNOCKOUT_BRACKET["QF"].items():
            th = st.session_state["knockout"].get(m1)
            ta = st.session_state["knockout"].get(m2)
            render_match_card(mid, th, ta, st, "QF")
            
    # --- Semi Finals ---
    with cols[3]:
        st.markdown("<h4>Semis</h4>", unsafe_allow_html=True)
        for mid, (m1, m2) in KNOCKOUT_BRACKET["SF"].items():
            th = st.session_state["knockout"].get(m1)
            ta = st.session_state["knockout"].get(m2)
            render_match_card(mid, th, ta, st, "SF")
            
    # --- Final & Third Place ---
    with cols[4]:
        st.markdown("<h4>Finais</h4>", unsafe_allow_html=True)
        
        # Third Place Playoff (103)
        th_sf = st.session_state["knockout"].get(101)
        ta_sf = st.session_state["knockout"].get(102)
        # Losers of 101 and 102
        loser1 = None
        loser2 = None
        if th_sf: # if 101 has winner
            from data import KNOCKOUT_BRACKET
            m1, m2 = KNOCKOUT_BRACKET["SF"][101]
            t1 = st.session_state["knockout"].get(m1)
            t2 = st.session_state["knockout"].get(m2)
            loser1 = t2 if th_sf == t1 else t1
            
        if ta_sf: # if 102 has winner
            m1, m2 = KNOCKOUT_BRACKET["SF"][102]
            t1 = st.session_state["knockout"].get(m1)
            t2 = st.session_state["knockout"].get(m2)
            loser2 = t2 if ta_sf == t1 else t1
            
        render_match_card(103, loser1, loser2, st, "3º Lugar")
        
        # Final (104)
        mid = 104
        m1, m2 = KNOCKOUT_BRACKET["FINAL"][mid]
        th = st.session_state["knockout"].get(m1)
        ta = st.session_state["knockout"].get(m2)
        render_match_card(mid, th, ta, st, "Final")
