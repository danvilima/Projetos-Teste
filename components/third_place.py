import streamlit as st
from data import GROUPS
from matching_algorithm import match_third_places
from components.utils import render_team_html

def render_third_places():
    st.markdown("<h2>Seleção dos Terceiros Colocados</h2>", unsafe_allow_html=True)
    st.markdown("<p>Selecione exatamente 8 terceiros colocados para avançar para o mata-mata.</p>", unsafe_allow_html=True)
    
    # Collect all 3rd places that are valid
    available_thirds = []
    for g in GROUPS.keys():
        t = st.session_state[f"group_{g}_3"]
        if t:
            available_thirds.append((g, t))
            
    if len(available_thirds) < 8:
        st.warning("Você precisa definir pelo menos 8 terceiros colocados nos grupos acima.")
        return False
        
    selected = st.session_state.get("selected_thirds", [])
    
    cols = st.columns(4)
    for idx, (g, t) in enumerate(available_thirds):
        col = cols[idx % 4]
        with col:
            st.markdown(f"<div class='third-place-card'>", unsafe_allow_html=True)
            st.markdown(render_team_html(t), unsafe_allow_html=True)
            is_checked = (g, t) in selected
            if st.checkbox(f"Gr. {g}", value=is_checked, key=f"chk_3rd_{g}"):
                if (g, t) not in selected:
                    selected.append((g, t))
            else:
                if (g, t) in selected:
                    selected.remove((g, t))
            st.markdown("</div>", unsafe_allow_html=True)
                    
    st.session_state["selected_thirds"] = selected
    
    st.markdown(f"**Selecionados: {len(selected)}/8**")
    
    if len(selected) > 8:
        st.error("Você selecionou mais de 8 times. Desmarque alguns.")
        return False
    elif len(selected) == 8:
        # Run matching algorithm
        matching = match_third_places(selected)
        if matching:
            st.session_state["third_place_matching"] = matching
            st.success("Mapeamento realizado com sucesso! O Mata-mata está desbloqueado.")
            return True
        else:
            st.error("A combinação selecionada é inválida segundo as regras da FIFA de cruzamento. Altere sua seleção.")
            return False
    else:
        st.info("Selecione mais times para completar os 8.")
        return False
