import streamlit as st
from pathlib import Path
from shared.config import SEVERITY_COLOURS


def check_prerequisites(required: list[str]) -> bool:
    missing = [p for p in required if not Path(p).exists()]
    if missing:
        for p in missing:
            st.error(
                f"Required file or directory not found: `{p}`\n\n"
                "Please run the seed scripts to set up the database and vector index:\n"
                "```bash\n"
                "uv run python data/seed.py\n"
                "uv run python data/seed_resolver.py\n"
                "uv run python data/seed_navigator.py\n"
                "```"
            )
        return False
    return True


def brain_header(brain_name: str, description: str, colour: str):
    st.markdown(
        f"<h1 style='color:{colour};margin-bottom:0;'>{brain_name}</h1>"
        f"<p style='color:#888;margin-top:4px;font-size:16px;'>{description}</p>",
        unsafe_allow_html=True,
    )
    st.divider()


def example_query_buttons(queries: list[str], key_prefix: str) -> str | None:
    selected = None
    for i, query in enumerate(queries):
        if st.sidebar.button(query, key=f"{key_prefix}_example_{i}", use_container_width=True):
            selected = query
    return selected


def severity_badge(severity: str) -> str:
    colour = SEVERITY_COLOURS.get(severity, "#888")
    return (
        f'<span style="background:{colour};color:white;'
        f'padding:2px 8px;border-radius:4px;font-size:12px;">'
        f"{severity}</span>"
    )


def result_card(
    title: str,
    metadata: dict,
    content: str,
    relevance_score: float = None,
):
    with st.container():
        st.markdown(
            f"<div style='border:1px solid #e0e0e0;border-radius:8px;"
            f"padding:16px;margin-bottom:12px;background:#fafafa;'>",
            unsafe_allow_html=True,
        )
        st.markdown(f"**{title}**")

        meta_parts = []
        for k, v in metadata.items():
            if k == "severity":
                meta_parts.append(severity_badge(str(v)))
            else:
                meta_parts.append(
                    f"<span style='color:#888;font-size:12px;'>"
                    f"<b>{k}:</b> {v}</span>"
                )
        st.markdown(" &nbsp;|&nbsp; ".join(meta_parts), unsafe_allow_html=True)

        st.markdown(
            f"<div style='background:#f0f0f0;border-radius:4px;"
            f"padding:10px;margin-top:8px;font-size:13px;'>{content}</div>",
            unsafe_allow_html=True,
        )

        if relevance_score is not None:
            st.markdown(
                f"<span style='color:#888;font-size:11px;'>Relevance: {relevance_score:.2f}</span>",
                unsafe_allow_html=True,
            )
            st.progress(min(max(relevance_score, 0.0), 1.0))

        st.markdown("</div>", unsafe_allow_html=True)
