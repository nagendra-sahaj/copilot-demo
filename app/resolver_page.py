import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from shared.config import PRIMARY_COLOUR, CHROMA_PATH
from shared.ui import brain_header, example_query_buttons, result_card
from brains.resolver.retriever import retrieve
from brains.resolver.reranker import rerank
from brains.resolver.answerer import generate_answer

RESOLVER_COLOUR = "#7B4FD4"

EXAMPLE_QUERIES = [
    "Summarise issues for Alpine Ski House",
    "Show me unresolved Critical security issues and how similar ones were fixed",
    "Find issues related to billing and payment failures",
    "What patterns do we see in Performance issues for Platinum clients?",
    "API gateway timeouts causing batch job failures at Bellows College — find similar resolved Performance issues and how they were fixed",
]


def render_sidebar():
    st.sidebar.markdown("### Example queries")
    return example_query_buttons(EXAMPLE_QUERIES, key_prefix="resolver")


def render():
    brain_header(
        "Resolver",
        "Ask anything about operational issues — summaries, patterns, resolution guidance.",
        RESOLVER_COLOUR,
    )

    chroma_path = Path(CHROMA_PATH)
    if not chroma_path.exists():
        st.error(
            "Vector index not found. Run `uv run python data/seed_resolver.py` "
            "to build the Resolver index."
        )
        return

    selected_query = st.session_state.pop("selected_query_resolver", None)
    if selected_query:
        st.session_state["resolver_input"] = selected_query

    query = st.text_area(
        "Describe the issue",
        key="resolver_input",
        placeholder="Ask about issues — summaries, patterns, resolution guidance, or specific clients...",
        height=100,
        label_visibility="collapsed",
    )

    submit = st.button("Ask Resolver", type="primary")

    if not submit:
        return

    if not query.strip():
        st.warning("Please enter a question.")
        return

    # Step 1: Retrieve
    with st.spinner("Searching for similar issues..."):
        try:
            results = retrieve(query, n_results=8)
        except Exception as exc:
            st.error(f"Retrieval failed: {exc}")
            return

    if not results:
        st.warning(
            "No similar issues found. Try different keywords or remove filters."
        )
        return

    # Step 2: Rerank
    with st.spinner("Reranking by relevance..."):
        try:
            ranked = rerank(query, results, top_k=3)
        except Exception as exc:
            st.error(f"Reranking failed: {exc}")
            ranked = results[:3]

    # Step 3: Generate answer — shown first
    with st.spinner("Generating response..."):
        try:
            answer = generate_answer(query, ranked)
        except Exception as exc:
            st.error(f"Answer generation failed: {exc}")
            return

    st.markdown(
        f"""
        <div style="background:#F3EEF9;border-left:4px solid {RESOLVER_COLOUR};
                    padding:16px 20px;border-radius:6px;margin-bottom:24px;">
            <p style="margin:0;font-size:15px;color:#1a1a1a;">{answer.replace(chr(10), '<br>')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Issue cards — shown below the response
    st.subheader("Issues retrieved")
    for result in ranked:
        result_card(
            title=result["matched_chunk"][:80] + "...",
            metadata={
                "client": result["client_name"],
                "severity": result["severity"],
                "status": result["status"],
                "revenue impact": f"${result['revenue_impact_usd']:,}",
            },
            content=result["parent_text"][:400] + "...",
            relevance_score=result.get("relevance_score"),
        )
