import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from shared.config import DB_PATH, CHROMA_PATH, PRIMARY_COLOUR

st.set_page_config(
    page_title="Copilot Demo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

import strategist_page
import resolver_page
import navigator_page

# Sidebar — logo and brain selector
st.sidebar.markdown(
    f"<h2 style='color:{PRIMARY_COLOUR};margin-bottom:0;'>🧠 Copilot Demo</h2>",
    unsafe_allow_html=True,
)
st.sidebar.divider()

brain = st.sidebar.radio(
    "Select a brain",
    options=["🟣 Navigator", "🟢 Resolver", "🔵 Strategist"],
    label_visibility="collapsed",
)

BRAIN_DESCRIPTIONS = {
    "🟣 Navigator": "How-to documentation",
    "🟢 Resolver": "Issue resolution guidance",
    "🔵 Strategist": "Analytics & business insights",
}
st.sidebar.caption(BRAIN_DESCRIPTIONS.get(brain, ""))
st.sidebar.divider()

# Render sidebar content for selected brain and capture any example query click
if brain == "🟣 Navigator":
    selected = navigator_page.render_sidebar()
    if selected:
        st.session_state["selected_query_navigator"] = selected
        st.rerun()

elif brain == "🟢 Resolver":
    selected = resolver_page.render_sidebar()
    if selected:
        st.session_state["selected_query_resolver"] = selected
        st.rerun()

elif brain == "🔵 Strategist":
    selected = strategist_page.render_sidebar()
    if selected:
        st.session_state["selected_query_strategist"] = selected
        st.rerun()

# Startup checks
db_exists = Path(DB_PATH).exists()
chroma_exists = Path(CHROMA_PATH).exists()

if not db_exists:
    st.error(
        "**Database not found.**\n\n"
        "Run the following to set up:\n"
        "```bash\n"
        "uv run python data/seed.py\n"
        "```"
    )

if not chroma_exists:
    st.info(
        "**Vector index not found.** Resolver and Navigator brains require seeding:\n"
        "```bash\n"
        "uv run python data/seed_resolver.py\n"
        "uv run python data/seed_navigator.py\n"
        "```\n"
        "The Strategist brain works without this."
    )

# Render selected brain
if brain == "🟣 Navigator":
    navigator_page.render()
elif brain == "🟢 Resolver":
    resolver_page.render()
elif brain == "🔵 Strategist":
    strategist_page.render()
