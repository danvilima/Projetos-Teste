import streamlit as st
import os

from state_manager import init_state, randomize_all, reset_all
from components.groups import render_groups
from components.third_place import render_third_places
from components.knockout import render_knockout
from db import save_simulation

st.set_page_config(page_title="Simulador da Copa 2026", layout="wide", initial_sidebar_state="collapsed")

# Inject CSS
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
init_state()

# Header
st.markdown("<h1 class='accent-text'>Simulador da Copa do Mundo 2026</h1>", unsafe_allow_html=True)
st.write("Quem levantará a taça? Escolha os dois primeiros colocados de cada grupo e oito terceiros colocados para formar os 32 que vão para o mata-mata. Depois, monte a chave até a final.")

st.divider()

# Controls
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎲 Preencher Todas as Chaves (Aleatório)"):
        randomize_all()
        # We also need to automatically advance teams in knockout for a full simulation
        # but for simplicity let's just randomize groups and thirds to unlock knockout.
        st.rerun()
with col2:
    if st.button("🔄 Reiniciar"):
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
        from data import KNOCKOUT_BRACKET
        m1, m2 = KNOCKOUT_BRACKET["FINAL"][104]
        t1 = st.session_state["knockout"].get(m1)
        t2 = st.session_state["knockout"].get(m2)
        runner_up = t2 if champion == t1 else t1
        
        user_name = st.text_input("Seu nome para salvar o placar (opcional):", "Anonymous")
        
        if st.button("💾 Salvar Simulação no Supabase"):
            if save_simulation(champion, runner_up or "N/A", third_place or "N/A", user_name):
                st.balloons()
                st.success("Simulação salva com sucesso no Supabase!")
            else:
                st.error("Erro ao salvar simulação. Verifique as credenciais do Supabase.")
