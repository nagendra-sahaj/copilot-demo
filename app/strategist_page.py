import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from shared.config import PRIMARY_COLOUR, DB_PATH
from shared.ui import brain_header, example_query_buttons
from brains.strategist.sql_agent import generate_sql
from brains.strategist.executor import execute_sql
from brains.strategist.visualiser import select_and_render
from brains.strategist.summariser import summarise

EXAMPLE_QUERIES = [
    "What are the top 5 features by revenue generation potential?",
    "Show me the trend of issues created over the last 6 months",
    "Which clients have the highest revenue at risk from open issues?",
    "What is the breakdown of issues by severity?",
    "Which features in Backlog have the highest priority score?",
]


def render_sidebar():
    st.sidebar.markdown("### Example queries")
    return example_query_buttons(EXAMPLE_QUERIES, key_prefix="strategist")


def render():
    brain_header(
        "Strategist",
        "Ask business questions — get SQL, charts, and insights automatically.",
        PRIMARY_COLOUR,
    )

    if not Path(DB_PATH).exists():
        st.error(
            "Database not found. Run `uv run python data/seed.py` to set up the database."
        )
        return

    # Check for example query selection from sidebar
    selected_query = st.session_state.pop("selected_query_strategist", None)
    if selected_query:
        st.session_state["strategist_input"] = selected_query

    question = st.text_input(
        "Your question",
        key="strategist_input",
        placeholder="Ask a business question about issues, features, or client data...",
        label_visibility="collapsed",
    )

    submit = st.button("Generate insight", type="primary")

    if not submit:
        return

    if not question.strip():
        st.warning("Please enter a question.")
        return

    # Step 1: Generate SQL
    with st.spinner("Generating SQL query..."):
        try:
            sql = generate_sql(question)
        except Exception as exc:
            st.error(f"SQL generation failed: {exc}")
            return

    with st.expander("View generated SQL", expanded=False):
        st.code(sql, language="sql")

    # Step 2: Execute SQL
    with st.spinner("Running query..."):
        start = time.perf_counter()
        df, error = execute_sql(sql)
        elapsed_ms = (time.perf_counter() - start) * 1000

    if error:
        st.error(f"Query failed: {error}")
        return

    if df.empty:
        st.warning("No results found for this query.")
        return

    # Metrics row
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows returned", len(df))
    col2.metric("Columns", len(df.columns))
    col3.metric("Query time", f"{elapsed_ms:.0f}ms")

    # Step 3: Render chart
    with st.spinner("Rendering chart..."):
        try:
            fig = select_and_render(df, question)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as exc:
            st.warning(f"Chart could not be rendered: {exc}")
            st.dataframe(df, use_container_width=True)

    # Step 4: Generate summary
    with st.spinner("Generating summary..."):
        try:
            summary = summarise(df, question)
        except Exception as exc:
            summary = f"Summary unavailable: {exc}"

    st.markdown(
        f"""
        <div style="background:#E8F5F0;border-left:4px solid {PRIMARY_COLOUR};
                    padding:16px 20px;border-radius:6px;margin-top:12px;">
            <p style="margin:0;font-size:15px;color:#1a1a1a;">{summary}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
