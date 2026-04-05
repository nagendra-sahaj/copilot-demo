import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from shared.config import CHROMA_PATH
from shared.ui import brain_header, example_query_buttons
from brains.navigator.retriever import retrieve
from brains.navigator.answerer import generate_answer

NAVIGATOR_COLOUR = "#7C3AED"

EXAMPLE_QUERIES = [
    "How do I submit a new issue in UAT?",
    "How do I escalate a critical issue?",
    "How do I link an issue to a feature request?",
    "How do I add revenue opportunity to feedback in FB360?",
    "How do I reset my password?",
]


def render_sidebar():
    st.sidebar.markdown("### Example queries")
    return example_query_buttons(EXAMPLE_QUERIES, key_prefix="navigator")


def render():
    brain_header(
        "Navigator",
        "Ask how-to questions about UAT and FB360 — get step-by-step guidance from documentation.",
        NAVIGATOR_COLOUR,
    )

    chroma_path = Path(CHROMA_PATH)
    if not chroma_path.exists():
        st.error(
            "Documentation index not found. Add .md files to data/docs/ and run "
            "`uv run python data/seed_navigator.py` to build the Navigator index."
        )
        return

    selected_query = st.session_state.pop("selected_query_navigator", None)

    question = st.text_input(
        "Your question",
        value=selected_query or "",
        placeholder="Ask a how-to question about UAT or FB360...",
        label_visibility="collapsed",
    )

    submit = st.button("Get answer", type="primary")

    if not (submit or selected_query):
        return

    if not question.strip():
        st.warning("Please enter a question.")
        return

    # Step 1: Retrieve docs
    with st.spinner("Searching documentation..."):
        try:
            docs = retrieve(question, n_results=5)
        except Exception as exc:
            st.error(f"Documentation search failed: {exc}")
            return

    if not docs:
        st.warning("No relevant documentation found.")
        return

    # Source pills
    st.markdown("**Sources consulted:**")
    pills_html = " ".join(
        f'<span style="background:#f0f0f0;color:#555;padding:3px 10px;'
        f'border-radius:12px;font-size:12px;margin-right:4px;">'
        f'{doc["source_file"]} — {doc["heading"]}</span>'
        for doc in docs
    )
    st.markdown(pills_html, unsafe_allow_html=True)
    st.markdown("")

    # Step 2: Generate answer
    with st.spinner("Generating answer..."):
        try:
            answer = generate_answer(question, docs)
        except Exception as exc:
            st.error(f"Answer generation failed: {exc}")
            return

    st.markdown(
        f"""
        <div style="background:#F5F0FF;border-left:4px solid {NAVIGATOR_COLOUR};
                    padding:16px 20px;border-radius:6px;margin-top:12px;">
            <p style="margin:0;font-size:15px;color:#1a1a1a;">{answer.replace(chr(10), '<br>')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Answers are based on UAT and FB360 documentation. "
        "For complex scenarios, consult your system administrator."
    )
