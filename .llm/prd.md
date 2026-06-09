# FIFA World Cup 2026 Simulator - Product Requirements Document (PRD)

## 1. Overview
The **FIFA World Cup 2026 Simulator** is an interactive web application that allows football fans to simulate the entire tournament, from the group stage to the final. The simulator implements the brand-new **48-team format** across **12 groups** (Groups A to L) and a **32-team knockout bracket**.

The application is built using **Python and Streamlit** for the frontend and logic, styled with custom CSS to deliver a premium, modern sports platform aesthetic (inspired by `ge.globo.com`) with vibrant green accents, glassmorphism card layouts, and complete responsiveness.

---

## 2. Key Features

### 2.1 Group Stage Simulator
*   **12 Groups (A to L):** Each group contains 4 pre-defined teams with their respective flags.
*   **Dynamic Rank Selectors:** For each group, the user selects the 1st, 2nd, and 3rd placed teams. To prevent invalid states, the options for 2nd place dynamically exclude the 1st place choice, and the options for 3rd place exclude both 1st and 2nd choices. The 4th-placed team is automatically resolved.
*   **Individual Random Draw ("Sorteio Aleatório"):** A button in each group card that shuffles the group and populates the rankings instantly.

### 2.2 Third-Place Qualification Panel
*   **Dynamic Pool:** Out of the 12 groups, the 12 third-placed teams are collected dynamically.
*   **Selection Grid:** The user selects exactly **8 third-placed teams** to advance.
*   **State Indicators:** A counter (`Selected: X/8`) with helpful indicators. The knockout stage is unlocked only when exactly 8 teams are selected.
*   **Backtracking Matchmaker:** A Python-based backtracking algorithm matches the 8 selected third-place teams to their official group-winner slots (E, I, A, L, D, G, B, K) in the Round of 32 based on FIFA's official group compatibility constraints.

### 2.3 Knockout Stage (Round of 32 to Final)
*   **Interactive Bracket:** Displayed using Streamlit columns representing the rounds (Round of 32, Round of 16, Quarter-finals, Semi-finals, and Final).
*   **Match Cards:** Each match is presented as a card containing two interactive team selection buttons. Clicking a team updates `st.session_state` and advances them to the next match slot.
*   **Cascading Updates:** Changing a winner in an earlier round automatically clears the subsequent slots that the team had advanced to, preventing stale team states.
*   **Third-Place Play-off:** A match between the two losing semi-finalists to decide the 3rd place.

### 2.4 Control Center
*   **Fill All Brackets ("Preencher Todas as Chaves"):** Instantly runs a random simulation for all groups, selects the 8 third-place teams, and simulates all knockout rounds to output a complete champion and podium.
*   **Reset ("Reiniciar"):** Clears the session state to start a new simulation.
*   **Share ("Compartilhar"):** Provides a summary of the champion and podium, with a button to copy the text to clipboard.

---

## 3. Official Tournament Data

### 3.1 Groups & Teams
*   **Group A:** México, África do Sul, Coreia do Sul, República Tcheca
*   **Group B:** Canadá, Bósnia, Catar, Suíça
*   **Group C:** Brasil, Marrocos, Haiti, Escócia
*   **Group D:** Estados Unidos, Paraguai, Austrália, Turquia
*   **Group E:** Alemanha, Curaçao, Costa do Marfim, Equador
*   **Group F:** Holanda, Japão, Suécia, Tunísia
*   **Group G:** Bélgica, Egito, Irã, Nova Zelândia
*   **Group H:** Espanha, Cabo Verde, Arábia Saudita, Uruguai
*   **Group I:** França, Senegal, Iraque, Noruega
*   **Group J:** Argentina, Argélia, Áustria, Jordânia
*   **Group K:** Portugal, RD Congo, Uzbequistão, Colômbia
*   **Group L:** Inglaterra, Croácia, Gana, Panamá

### 3.2 Round of 32 Fixed Matchups
*   **Match 73:** Runner-up Group A vs. Runner-up Group B
*   **Match 75:** Winner Group F vs. Runner-up Group C
*   **Match 76:** Winner Group C vs. Runner-up Group F
*   **Match 78:** Runner-up Group E vs. Runner-up Group I
*   **Match 83:** Runner-up Group K vs. Runner-up Group L
*   **Match 84:** Winner Group H vs. Runner-up Group J
*   **Match 86:** Winner Group J vs. Runner-up Group H
*   **Match 88:** Runner-up Group D vs. Runner-up Group G

### 3.3 Round of 32 Third-Place Matchups (Assigned Dynamically)
*   **Match 74:** Winner Group E vs. 3rd Place (Group A/B/C/D/F)
*   **Match 77:** Winner Group I vs. 3rd Place (Group C/D/F/G/H)
*   **Match 79:** Winner Group A vs. 3rd Place (Group C/E/F/H/I)
*   **Match 80:** Winner Group L vs. 3rd Place (Group E/H/I/J/K)
*   **Match 81:** Winner Group D vs. 3rd Place (Group B/E/F/I/J)
*   **Match 82:** Winner Group G vs. 3rd Place (Group A/E/H/I/J)
*   **Match 85:** Winner Group B vs. 3rd Place (Group E/F/G/I/J)
*   **Match 87:** Winner Group K vs. 3rd Place (Group D/E/I/J/L)

---

## 4. Visual Design & Tech Stack

### 4.1 Technology Stack
*   **Language:** Python (3.9+)
*   **Web Framework:** Streamlit (1.20+)
*   **Styling:** Custom CSS injected via `st.markdown(..., unsafe_allow_html=True)`
*   **Icons & Flags:** Emoji flags combined with clean text typography to ensure maximum rendering speed, portability, and native OS look.

### 4.2 Styling Guidelines (Aesthetics)
*   **Theme:** Light neutral base (`#f4f6f5`) with dark sport-centric headers (`#061d12`) and vibrant green accents (`#00b159` - ge.globo green).
*   **Glassmorphism Cards:** Semi-transparent cards with white backgrounds, subtle border-radius (`12px`), light shadows, and nice hover borders.
*   **Responsive Columns:** Using `st.columns` dynamically to stack on mobile and expand side-by-side on wide screens.

---

## 5. Verification Plan
*   **Validation of Dynamic Dropdowns:** Check that selecting a team as 1st updates the choices for 2nd and 3rd immediately.
*   **Verification of Backtracking Bipartite Matchmaker:** Test with various subsets of 3rd place teams to ensure correct matching without collisions.
*   **State Cascades:** Verify that changing a winner at the Round of 32 level immediately wipes that path in subsequent rounds.
*   **Full Simulation Flow:** Verify that clicking "Preencher Todas as Chaves" completes the simulator from end-to-end and outputs a champion.
