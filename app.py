import streamlit as st
import os

from state_manager import init_state, randomize_all, reset_all
from components.groups import render_groups
from components.third_place import render_third_places
from components.knockout import render_knockout
from db import save_simulation

st.set_page_config(
    page_title="Simulador da Copa 2026",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Inject CSS
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()
init_state()

# Header
st.markdown(
    """
    <div class="app-header">
        <h1>Simulador da Copa do Mundo <span>2026</span></h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-subtitle">
        Quem levantará a taça? Escolha os dois primeiros colocados de cada grupo
        e oito terceiros colocados para formar os 32 que vão para o mata-mata.
        Depois, monte a chave até a final.
    </div>
    """,
    unsafe_allow_html=True,
)

# Identificação do jogador
st.markdown(
    """
    <div class="player-card">
        <div class="player-card-header">
            <div class="player-icon">👤</div>
            <h3>Identificação do Jogador</h3>
        </div>
        <p>Digite seu nome para salvar sua simulação no ranking.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

player_name = st.text_input(
    "Nome do jogador",
    value=st.session_state.get("user_name", ""),
    placeholder="Digite seu nome completo",
    key="player_name_input",
    label_visibility="collapsed",
)

if player_name != st.session_state.get("user_name"):
    st.session_state["user_name"] = player_name

# Controles
if st.button("🔄 Reiniciar", use_container_width=False):
    reset_all()
    st.rerun()

st.divider()

# 1. Groups
render_groups()

st.divider()

# 2. Third Places
is_unlocked = render_third_places()

st.divider()

# 3. Knockout
if is_unlocked or st.session_state.get("third_place_matching"):
    render_knockout()

    st.divider()

    st.subheader("🏁 Salvar Resultado")
    champion = st.session_state["knockout"].get(104)
    third_place = st.session_state["knockout"].get(103)

    if champion:
        st.success(f"🏆 Campeão: {champion}!")

        # Determine runner-up
        from data import KNOCKOUT_BRACKET, GROUPS

        m1, m2 = KNOCKOUT_BRACKET["FINAL"][104]
        t1 = st.session_state["knockout"].get(m1)
        t2 = st.session_state["knockout"].get(m2)
        runner_up = t2 if champion == t1 else t1

        user_name = st.session_state.get("user_name", "Anonymous")
        if not user_name.strip():
            user_name = "Anonymous"

        # Coletar dados completos
        group_predictions = {}
        for g in GROUPS.keys():
            group_predictions[g] = {
                "1st": st.session_state.get(f"group_{g}_1"),
                "2nd": st.session_state.get(f"group_{g}_2"),
            }

        third_place_predictions = {
            "selected": st.session_state.get("selected_thirds", []),
            "matching": st.session_state.get("third_place_matching", {}),
        }

        knockout_predictions = st.session_state.get("knockout", {})

        if st.button("💾 Salvar Simulação Completa no Supabase"):
            if save_simulation(
                champion,
                runner_up or "N/A",
                third_place or "N/A",
                user_name,
                group_predictions,
                third_place_predictions,
                knockout_predictions,
            ):
                st.balloons()
                st.success("Simulação salva com sucesso no Supabase!")
            else:
                st.error(
                    "Erro ao salvar simulação. Verifique as credenciais do Supabase."
                )
