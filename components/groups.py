import streamlit as st
from data import GROUPS
from state_manager import randomize_group

def render_groups():
    st.markdown("<h2>Grupos</h2>", unsafe_allow_html=True)
    
    groups_list = list(GROUPS.keys())
    # Create rows of 3 groups each
    for i in range(0, len(groups_list), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(groups_list):
                g = groups_list[i + j]
                with col:
                    # Glassmorphism card wrap via CSS styling
                    st.markdown(f"<h3>Grupo {g}</h3>", unsafe_allow_html=True)
                    
                    teams = GROUPS[g]
                    
                    # Current selections
                    s1 = st.session_state[f"group_{g}_1"]
                    s2 = st.session_state[f"group_{g}_2"]
                    s3 = st.session_state[f"group_{g}_3"]
                    
                    # 1st place
                    opts1 = [None] + teams
                    idx1 = opts1.index(s1) if s1 in opts1 else 0
                    pos1 = st.selectbox("1º Colocado", opts1, index=idx1, key=f"sel_{g}_1", label_visibility="collapsed", format_func=lambda x: "1° lugar" if x is None else f"1° lugar - {x}")
                    if pos1 != s1:
                        st.session_state[f"group_{g}_1"] = pos1
                        if pos1 == s2: st.session_state[f"group_{g}_2"] = None
                        if pos1 == s3: st.session_state[f"group_{g}_3"] = None
                        st.rerun()
                        
                    # 2nd place
                    opts2 = [None] + [t for t in teams if t != st.session_state[f"group_{g}_1"]]
                    idx2 = opts2.index(s2) if s2 in opts2 else 0
                    pos2 = st.selectbox("2º Colocado", opts2, index=idx2, key=f"sel_{g}_2", label_visibility="collapsed", format_func=lambda x: "2° lugar" if x is None else f"2° lugar - {x}")
                    if pos2 != s2:
                        st.session_state[f"group_{g}_2"] = pos2
                        if pos2 == s3: st.session_state[f"group_{g}_3"] = None
                        st.rerun()
                        
                    # 3rd place
                    opts3 = [None] + [t for t in teams if t not in [st.session_state[f"group_{g}_1"], st.session_state[f"group_{g}_2"]]]
                    idx3 = opts3.index(s3) if s3 in opts3 else 0
                    pos3 = st.selectbox("3º Colocado", opts3, index=idx3, key=f"sel_{g}_3", label_visibility="collapsed", format_func=lambda x: "3° lugar" if x is None else f"3° lugar - {x}")
                    if pos3 != s3:
                        st.session_state[f"group_{g}_3"] = pos3
                        st.rerun()
