import pandas as pd
import plotly.graph_objects as go
from shared.config import PRIMARY_COLOUR

_FONT = {"size": 13, "family": "Arial"}
_GRID_COLOUR = "#f0f0f0"
_BG = "white"


def _axis_label(col: str) -> str:
    return col.replace("_", " ").title()


def _chart_title(user_question: str) -> str:
    title = user_question.strip()
    title = title[0].upper() + title[1:] if title else title
    return title[:60]


def _layout_base(title: str, show_legend: bool = False) -> dict:
    return dict(
        title=dict(text=title, font=_FONT),
        font=_FONT,
        plot_bgcolor=_BG,
        paper_bgcolor=_BG,
        showlegend=show_legend,
        margin=dict(l=60, r=20, t=60, b=60),
        yaxis=dict(showgrid=True, gridcolor=_GRID_COLOUR),
        xaxis=dict(showgrid=False),
    )


def _best_label_col(cat_cols: list[str]) -> str:
    """Pick the most human-readable label column when there are several categorical cols."""
    priority_keywords = ("name", "title", "label", "client", "feature")
    for kw in priority_keywords:
        for col in cat_cols:
            if kw in col.lower():
                return col
    return cat_cols[0]


def _best_numeric_col(numeric_cols: list[str]) -> str:
    """Pick the primary metric column — prefer revenue/total/score/count aggregates."""
    priority_keywords = ("revenue", "total", "amount", "score", "impact", "count", "usd")
    for kw in priority_keywords:
        for col in numeric_cols:
            if kw in col.lower():
                return col
    return numeric_cols[-1]  # last column is usually the main aggregate


def _render_table(df: pd.DataFrame, title: str) -> go.Figure:
    header_vals = [_axis_label(c) for c in df.columns]
    cell_vals = [df[c].astype(str).tolist() for c in df.columns]
    fig = go.Figure(go.Table(
        header=dict(
            values=header_vals,
            fill_color=PRIMARY_COLOUR,
            font=dict(color="white", size=12),
            align="left",
        ),
        cells=dict(
            values=cell_vals,
            fill_color=[["white", "#f9f9f9"] * (len(df) // 2 + 1)],
            align="left",
            font=_FONT,
        ),
    ))
    fig.update_layout(
        title=dict(text=title, font=_FONT),
        font=_FONT,
        margin=dict(l=60, r=20, t=60, b=60),
    )
    return fig


def _render_h_bar(df: pd.DataFrame, cat_col: str, num_col: str, title: str) -> go.Figure:
    df_sorted = df.sort_values(num_col, ascending=True)
    fig = go.Figure(go.Bar(
        x=df_sorted[num_col],
        y=df_sorted[cat_col],
        orientation="h",
        marker_color=PRIMARY_COLOUR,
        name=_axis_label(num_col),
    ))
    layout = _layout_base(title)
    layout["xaxis"]["title"] = _axis_label(num_col)
    layout["yaxis"]["title"] = _axis_label(cat_col)
    layout["yaxis"]["showgrid"] = False
    layout["xaxis"]["showgrid"] = True
    layout["xaxis"]["gridcolor"] = _GRID_COLOUR
    fig.update_layout(**layout)
    return fig


def select_and_render(df: pd.DataFrame, user_question: str) -> go.Figure:
    title = _chart_title(user_question)

    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])
                 or (df[c].dtype == object and _looks_like_date(df[c]))]
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    cat_cols = [c for c in df.columns if c not in numeric_cols and c not in date_cols]

    # 1. Single metric (1 row × 1 col)
    if len(df) == 1 and len(df.columns) == 1:
        value = df.iloc[0, 0]
        fig = go.Figure(go.Indicator(
            mode="number",
            value=float(value) if pd.api.types.is_numeric_dtype(type(value)) else 0,
            number={"font": {"size": 64, "color": PRIMARY_COLOUR}},
            title={"text": _axis_label(df.columns[0]), "font": _FONT},
        ))
        fig.update_layout(
            title=dict(text=title, font=_FONT),
            font=_FONT,
            plot_bgcolor=_BG,
            paper_bgcolor=_BG,
            margin=dict(l=60, r=20, t=60, b=60),
        )
        return fig

    # 2. Wide or tall result → table
    # Must come before time-series and scatter checks so they don't swallow list-style queries.
    if len(df.columns) > 5 or len(df) > 50:
        return _render_table(df, title)

    # 3. Time series — date column present, ≥3 rows, and result is narrow (≤4 cols total).
    # The row-count and column-count guards prevent a single-row or multi-column
    # detail query from being misread as a trend chart.
    if date_cols and numeric_cols and len(df) >= 3 and len(df.columns) <= 4:
        date_col = date_cols[0]
        num_col = numeric_cols[0]
        df_sorted = df.sort_values(date_col)
        fig = go.Figure(go.Scatter(
            x=df_sorted[date_col],
            y=df_sorted[num_col],
            mode="lines+markers",
            line=dict(color=PRIMARY_COLOUR, width=2),
            marker=dict(color=PRIMARY_COLOUR, size=6),
            name=_axis_label(num_col),
        ))
        layout = _layout_base(title)
        layout["xaxis"]["title"] = _axis_label(date_col)
        layout["yaxis"]["title"] = _axis_label(num_col)
        fig.update_layout(**layout)
        return fig

    # 4a. Exactly 1 categorical + 1 numeric + ≤ 8 rows → pie chart (breakdown queries)
    if len(cat_cols) == 1 and len(numeric_cols) == 1 and len(df) <= 8:
        cat_col = cat_cols[0]
        num_col = numeric_cols[0]
        fig = go.Figure(go.Pie(
            labels=df[cat_col],
            values=df[num_col],
            hole=0.35,
            marker=dict(colors=[
                PRIMARY_COLOUR, "#2196F3", "#FF9800", "#9C27B0",
                "#F44336", "#00BCD4", "#8BC34A", "#FF5722",
            ]),
            textinfo="label+percent",
            insidetextorientation="radial",
        ))
        fig.update_layout(
            title=dict(text=title, font=_FONT),
            font=_FONT,
            paper_bgcolor=_BG,
            showlegend=True,
            margin=dict(l=60, r=20, t=60, b=60),
        )
        return fig

    # 4b. Exactly 1 categorical + 1 numeric + > 8 rows → horizontal bar
    if len(cat_cols) == 1 and len(numeric_cols) == 1:
        return _render_h_bar(df, cat_cols[0], numeric_cols[0], title)

    # 5. Exactly 1 categorical + 2+ numeric → grouped bar
    if len(cat_cols) == 1 and len(numeric_cols) >= 2:
        cat_col = cat_cols[0]
        colours = [PRIMARY_COLOUR, "#2196F3", "#FF9800", "#9C27B0", "#F44336"]
        traces = []
        for i, num_col in enumerate(numeric_cols):
            traces.append(go.Bar(
                x=df[cat_col],
                y=df[num_col],
                name=_axis_label(num_col),
                marker_color=colours[i % len(colours)],
            ))
        fig = go.Figure(data=traces)
        layout = _layout_base(title, show_legend=True)
        layout["xaxis"]["title"] = _axis_label(cat_col)
        layout["barmode"] = "group"
        fig.update_layout(**layout)
        return fig

    # 6. Multiple categorical cols + at least 1 numeric → horizontal bar.
    # Pick the most human-readable label column and the primary metric column.
    # This handles queries like "clients by revenue at risk" which return
    # (client_name, tier, industry, open_issues, total_revenue_at_risk).
    if len(cat_cols) >= 2 and numeric_cols:
        label_col = _best_label_col(cat_cols)
        metric_col = _best_numeric_col(numeric_cols)
        return _render_h_bar(df, label_col, metric_col, title)

    # 7. Only numeric columns (no categoricals) → scatter
    if len(numeric_cols) >= 2 and not cat_cols:
        x_col = numeric_cols[0]
        y_col = numeric_cols[1]
        fig = go.Figure(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode="markers",
            marker=dict(color=PRIMARY_COLOUR, size=8, opacity=0.7),
        ))
        layout = _layout_base(title)
        layout["xaxis"]["title"] = _axis_label(x_col)
        layout["yaxis"]["title"] = _axis_label(y_col)
        fig.update_layout(**layout)
        return fig

    # 8. Default → vertical bar using first cat and first numeric
    x_col = cat_cols[0] if cat_cols else df.columns[0]
    y_col = numeric_cols[0] if numeric_cols else df.columns[1] if len(df.columns) > 1 else df.columns[0]
    fig = go.Figure(go.Bar(
        x=df[x_col],
        y=df[y_col],
        marker_color=PRIMARY_COLOUR,
        name=_axis_label(y_col),
    ))
    layout = _layout_base(title)
    layout["xaxis"]["title"] = _axis_label(x_col)
    layout["yaxis"]["title"] = _axis_label(y_col)
    fig.update_layout(**layout)
    return fig


def _looks_like_date(series: pd.Series) -> bool:
    try:
        sample = series.dropna().head(5)
        if len(sample) == 0:
            return False
        pd.to_datetime(sample)
        return True
    except Exception:
        return False
