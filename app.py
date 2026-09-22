import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Sales Forecasting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DESIGN SYSTEM
# ============================================================
# One palette, reused everywhere: CSS, metric cards, and every
# Plotly chart. Nothing here is decorative for its own sake —
# it exists so the dashboard reads as one designed surface
# instead of a stack of default widgets.

PALETTE = {
    "bg":        "#0f1220",
    "panel":     "#171b2e",
    "panel_2":   "#1d2238",
    "border":    "#2a2f4a",
    "text":      "#eef0fa",
    "muted":     "#9096b5",
    "primary":   "#7c6ff2",   # indigo
    "primary_2": "#9d8cff",
    "accent":    "#22d3c5",   # teal
    "warn":      "#f5a35c",
    "bad":       "#f2607a",
    "good":      "#3ddc97",
}

CHART_COLORWAY = [
    PALETTE["primary_2"], PALETTE["accent"], PALETTE["warn"],
    PALETTE["bad"], PALETTE["good"], "#5eb1ff",
]

PLOTLY_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        colorway=CHART_COLORWAY,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=PALETTE["text"], size=13),
        title=dict(font=dict(size=17, color=PALETTE["text"])),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor=PALETTE["border"], zerolinecolor=PALETTE["border"],
                   linecolor=PALETTE["border"]),
        yaxis=dict(gridcolor=PALETTE["border"], zerolinecolor=PALETTE["border"],
                   linecolor=PALETTE["border"]),
        margin=dict(t=60, l=10, r=10, b=10),
    )
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(1200px 600px at 10% -10%, rgba(124,111,242,0.18), transparent),
            radial-gradient(1000px 500px at 100% 0%, rgba(34,211,197,0.10), transparent),
            {PALETTE["bg"]};
    }}

    #MainMenu, footer, header {{ visibility: hidden; }}

    * {{ box-sizing: border-box; }}

    .block-container {{
        padding-top: 2.2rem;
        max-width: 1360px;
    }}

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {PALETTE["panel"]} 0%, {PALETTE["bg"]} 100%);
        border-right: 1px solid {PALETTE["border"]};
    }}

    section[data-testid="stSidebar"] > div {{
        padding-top: 1.6rem;
    }}

    .sidebar-title {{
        font-size: 19px;
        font-weight: 800;
        color: {PALETTE["text"]};
        margin-bottom: 22px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .filter-group {{
        background: linear-gradient(180deg, {PALETTE["panel_2"]}, {PALETTE["panel"]});
        border: 1px solid {PALETTE["border"]};
        border-radius: 14px;
        padding: 14px 16px 4px 16px;
        margin-bottom: 14px;
        transition: border-color 0.2s ease;
    }}

    .filter-group:hover {{
        border-color: {PALETTE["primary_2"]}55;
    }}

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stDateInput label {{
        color: {PALETTE["muted"]} !important;
        font-weight: 700;
        font-size: 11.5px;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }}

    /* Native select / date input chrome */

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="input"] > div,
    .stDateInput input {{
        background-color: {PALETTE["bg"]} !important;
        border: 1px solid {PALETTE["border"]} !important;
        border-radius: 10px !important;
        color: {PALETTE["text"]} !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }}

    section[data-testid="stSidebar"] div[data-baseweb="select"]:focus-within > div,
    section[data-testid="stSidebar"] div[data-baseweb="input"]:focus-within > div {{
        border-color: {PALETTE["primary_2"]} !important;
        box-shadow: 0 0 0 3px {PALETTE["primary_2"]}22 !important;
    }}

    .sidebar-note {{
        color: {PALETTE["muted"]};
        font-size: 12px;
        line-height: 1.6;
        padding: 14px 4px 4px 4px;
        border-top: 1px solid {PALETTE["border"]};
        margin-top: 6px;
    }}

    /* ---------- Header ---------- */

    .hero {{
        position: relative;
        padding: 36px 40px;
        border-radius: 24px;
        background:
            radial-gradient(600px 260px at 100% 0%, rgba(34,211,197,0.16), transparent),
            linear-gradient(135deg, rgba(124,111,242,0.28), rgba(29,34,56,0.4));
        border: 1px solid {PALETTE["border"]};
        margin-bottom: 32px;
        overflow: hidden;
        box-shadow: 0 20px 60px -30px rgba(124,111,242,0.55);
    }}

    .hero::after {{
        content: "";
        position: absolute;
        top: -60px; right: -60px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, {PALETTE["primary_2"]}33, transparent 70%);
        pointer-events: none;
    }}

    .hero-eyebrow {{
        color: {PALETTE["accent"]};
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        background: {PALETTE["accent"]}18;
        border: 1px solid {PALETTE["accent"]}33;
    }}

    .hero-title {{
        font-size: 38px;
        font-weight: 800;
        color: {PALETTE["text"]};
        margin: 14px 0 8px 0;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }}

    .hero-subtitle {{
        font-size: 15.5px;
        color: {PALETTE["muted"]};
        max-width: 620px;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }}

    /* ---------- Section titles ---------- */

    .section-title {{
        font-size: 21px;
        font-weight: 700;
        color: {PALETTE["text"]};
        margin: 8px 0 4px 0;
        padding-left: 14px;
        border-left: 3px solid {PALETTE["primary_2"]};
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .section-sub {{
        color: {PALETTE["muted"]};
        font-size: 13px;
        margin: 4px 0 18px 17px;
    }}

    /* ---------- Metric cards ---------- */

    .kpi-row {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 10px;
    }}

    .kpi-card {{
        background: linear-gradient(165deg, {PALETTE["panel_2"]} 0%, {PALETTE["panel"]} 100%);
        border: 1px solid {PALETTE["border"]};
        border-radius: 18px;
        padding: 20px 22px;
        position: relative;
        overflow: hidden;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }}

    .kpi-card:hover {{
        transform: translateY(-3px);
        border-color: var(--accent-color, {PALETTE["primary_2"]})77;
        box-shadow: 0 16px 32px -18px var(--accent-color, {PALETTE["primary_2"]});
    }}

    .kpi-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-color, {PALETTE["primary_2"]}), transparent);
    }}

    .kpi-icon {{
        width: 38px; height: 38px;
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        background: var(--accent-color, {PALETTE["primary_2"]})1f;
        border: 1px solid var(--accent-color, {PALETTE["primary_2"]})40;
        margin-bottom: 14px;
    }}

    .kpi-label {{
        color: {PALETTE["muted"]};
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
    }}

    .kpi-value {{
        color: {PALETTE["text"]};
        font-size: 27px;
        font-weight: 800;
        letter-spacing: -0.01em;
    }}

    .kpi-delta {{
        font-size: 12.5px;
        font-weight: 700;
        margin-top: 8px;
        display: inline-block;
        padding: 2px 9px;
        border-radius: 999px;
    }}

    .kpi-delta.up   {{ color: {PALETTE["good"]}; background: {PALETTE["good"]}18; }}
    .kpi-delta.down {{ color: {PALETTE["bad"]};  background: {PALETTE["bad"]}18; }}
    .kpi-delta.flat {{ color: {PALETTE["muted"]}; background: {PALETTE["muted"]}18; }}

    /* ---------- Insight / info cards ---------- */

    .info-card {{
        background: linear-gradient(165deg, {PALETTE["panel_2"]}, {PALETTE["panel"]});
        border: 1px solid {PALETTE["border"]};
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 14px;
        display: flex;
        gap: 14px;
        align-items: flex-start;
        transition: transform 0.18s ease, border-color 0.18s ease;
    }}

    .info-card:hover {{
        transform: translateY(-2px);
        border-color: var(--accent-color, {PALETTE["primary_2"]})66;
    }}

    .info-card-icon {{
        width: 40px; height: 40px;
        min-width: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        background: var(--accent-color, {PALETTE["primary_2"]})1f;
        border: 1px solid var(--accent-color, {PALETTE["primary_2"]})40;
    }}

    .info-card-title {{
        font-size: 12.5px;
        font-weight: 700;
        color: {PALETTE["muted"]};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }}

    .info-card-main {{
        font-size: 21px;
        font-weight: 800;
        color: {PALETTE["text"]};
        margin-bottom: 4px;
        letter-spacing: -0.01em;
    }}

    .info-card-sub {{
        font-size: 13px;
        color: {PALETTE["muted"]};
        line-height: 1.5;
    }}

    /* ---------- Chart container ---------- */

    .chart-card {{
        background: linear-gradient(165deg, {PALETTE["panel"]}, {PALETTE["panel_2"]}55);
        border: 1px solid {PALETTE["border"]};
        border-radius: 18px;
        padding: 14px 18px 6px 18px;
        margin-bottom: 24px;
        transition: border-color 0.2s ease;
    }}

    .chart-card:hover {{
        border-color: {PALETTE["primary_2"]}55;
    }}

    /* ---------- Tabs (pill style) ---------- */

    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        background: {PALETTE["panel"]};
        padding: 6px;
        border-radius: 14px;
        border: 1px solid {PALETTE["border"]};
        margin-bottom: 28px;
    }}

    .stTabs [data-baseweb="tab"] {{
        color: {PALETTE["muted"]};
        font-weight: 600;
        font-size: 14px;
        padding: 9px 18px;
        border-radius: 10px;
        transition: all 0.15s ease;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        color: {PALETTE["text"]};
        background: {PALETTE["panel_2"]};
    }}

    .stTabs [aria-selected="true"] {{
        color: #ffffff !important;
        background: linear-gradient(135deg, {PALETTE["primary"]}, {PALETTE["primary_2"]}) !important;
        box-shadow: 0 6px 16px -6px {PALETTE["primary_2"]}aa;
    }}

    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* ---------- Dataframe ---------- */

    div[data-testid="stDataFrame"] {{
        border: 1px solid {PALETTE["border"]};
        border-radius: 14px;
        overflow: hidden;
    }}

    /* ---------- Native alerts (st.info / st.warning / st.success) ---------- */

    div[data-testid="stAlert"] {{
        background: linear-gradient(165deg, {PALETTE["panel_2"]}, {PALETTE["panel"]}) !important;
        border: 1px solid {PALETTE["border"]} !important;
        border-left: 3px solid {PALETTE["primary_2"]} !important;
        border-radius: 14px !important;
        color: {PALETTE["text"]} !important;
    }}

    div[data-testid="stAlert"] p {{
        color: {PALETTE["text"]} !important;
        line-height: 1.6;
    }}

    div[data-testid="stAlert"] code {{
        background: {PALETTE["bg"]};
        color: {PALETTE["accent"]};
        border-radius: 4px;
        padding: 1px 5px;
    }}

    /* ---------- Empty state ---------- */

    .empty-state {{
        background: linear-gradient(165deg, {PALETTE["panel_2"]}, {PALETTE["panel"]});
        border: 1px dashed {PALETTE["border"]};
        border-radius: 18px;
        padding: 30px 32px;
        text-align: center;
    }}

    .empty-state-icon {{
        font-size: 30px;
        margin-bottom: 10px;
    }}

    .empty-state-title {{
        font-size: 16px;
        font-weight: 700;
        color: {PALETTE["text"]};
        margin-bottom: 8px;
    }}

    .empty-state-sub {{
        font-size: 13.5px;
        color: {PALETTE["muted"]};
        max-width: 560px;
        margin: 0 auto;
        line-height: 1.6;
    }}

    .empty-state-sub code {{
        background: {PALETTE["bg"]};
        color: {PALETTE["accent"]};
        border-radius: 4px;
        padding: 1px 5px;
    }}

    hr {{ border-color: {PALETTE["border"]}; }}

    .footer-caption {{
        color: {PALETTE["muted"]};
        font-size: 12.5px;
        text-align: center;
        padding: 26px 0 6px 0;
        position: relative;
    }}

    .footer-caption::before {{
        content: "";
        display: block;
        width: 60px;
        height: 3px;
        margin: 0 auto 16px auto;
        border-radius: 999px;
        background: linear-gradient(90deg, {PALETTE["primary_2"]}, {PALETTE["accent"]});
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SMALL UI HELPERS
# ============================================================

def kpi_card(label, value, accent=PALETTE["primary_2"], delta=None, delta_dir="flat", icon="📌"):
    """Render one KPI tile as styled HTML instead of the default st.metric box."""
    delta_html = ""
    if delta is not None:
        arrow = {"up": "▲", "down": "▼", "flat": "•"}[delta_dir]
        delta_html = f'<div class="kpi-delta {delta_dir}">{arrow} {delta}</div>'

    return f"""
    <div class="kpi-card" style="--accent-color:{accent}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """


def info_card(title, main, sub, accent=PALETTE["primary_2"], icon="💡"):
    return f"""
    <div class="info-card" style="--accent-color:{accent}">
        <div class="info-card-icon">{icon}</div>
        <div>
            <div class="info-card-title">{title}</div>
            <div class="info-card-main">{main}</div>
            <div class="info-card-sub">{sub}</div>
        </div>
    </div>
    """


def empty_state(title, sub, icon="🗂️"):
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-state-icon">{icon}</div>
            <div class="empty-state-title">{title}</div>
            <div class="empty-state-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section(title, subtitle=None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)


def style_fig(fig, height=440):
    fig.update_layout(template=PLOTLY_TEMPLATE, height=height, hovermode="x unified")
    return fig


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_forecast_data():
    df = pd.read_csv("forecast_output.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


@st.cache_data
def load_sales_data():
    df = pd.read_csv("clean_data/clean_data.csv")
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    return df


@st.cache_data
def load_model_results():
    try:
        return pd.read_csv("model_results.csv")
    except FileNotFoundError:
        return None


forecast_df = load_forecast_data()
sales_df = load_sales_data()
model_results = load_model_results()


# ============================================================
# DATA CLEANING
# ============================================================

forecast_df = forecast_df.dropna(
    subset=["Date", "Store", "Dept", "Actual_Sales", "Predicted_Sales"]
)

sales_df = sales_df.dropna(
    subset=["Date", "Store", "Dept", "Weekly_Sales"]
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">Machine Learning · Time Series</div>
        <div class="hero-title">📊 Retail Sales Forecasting</div>
        <div class="hero-subtitle">
            Interactive analysis of historical retail sales, forecasting accuracy,
            store performance and the external factors driving demand.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    '<div class="sidebar-title">🔎 Filters</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown('<div class="filter-group">', unsafe_allow_html=True)
store_options = ["All"] + sorted(forecast_df["Store"].unique().tolist())
selected_store = st.sidebar.selectbox("🏪 Store", store_options)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="filter-group">', unsafe_allow_html=True)
dept_options = ["All"] + sorted(forecast_df["Dept"].unique().tolist())
selected_dept = st.sidebar.selectbox("🏬 Department", dept_options)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="filter-group">', unsafe_allow_html=True)
min_date = forecast_df["Date"].min().date()
max_date = forecast_df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

if isinstance(selected_dates, tuple):
    if len(selected_dates) == 2:
        start_date = pd.Timestamp(selected_dates[0])
        end_date = pd.Timestamp(selected_dates[1])
    else:
        start_date = pd.Timestamp(selected_dates[0])
        end_date = start_date
else:
    start_date = pd.Timestamp(selected_dates)
    end_date = start_date

st.sidebar.markdown('<div class="filter-group">', unsafe_allow_html=True)
holiday_filter = st.sidebar.selectbox(
    "🎉 Holiday Period",
    ["All", "Holiday Weeks", "Non-Holiday Weeks"]
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown(
    '<div class="sidebar-note">Data refreshes from the latest exported '
    'forecast and model files.</div>',
    unsafe_allow_html=True
)


# ============================================================
# FILTER FORECAST DATA
# ============================================================

filtered_df = forecast_df.copy()

if selected_store != "All":
    filtered_df = filtered_df[filtered_df["Store"] == selected_store]

if selected_dept != "All":
    filtered_df = filtered_df[filtered_df["Dept"] == selected_dept]

filtered_df = filtered_df[
    (filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)
]


# ============================================================
# FILTER ORIGINAL DATA
# ============================================================

filtered_sales = sales_df.copy()

if selected_store != "All":
    filtered_sales = filtered_sales[filtered_sales["Store"] == selected_store]

if selected_dept != "All":
    filtered_sales = filtered_sales[filtered_sales["Dept"] == selected_dept]

filtered_sales = filtered_sales[
    (filtered_sales["Date"] >= start_date) & (filtered_sales["Date"] <= end_date)
]


# ============================================================
# HOLIDAY FILTER
# ============================================================

if holiday_filter != "All":

    holiday_data = (
        sales_df[["Date", "Store", "Dept", "IsHoliday"]]
        .drop_duplicates()
    )

    filtered_df = filtered_df.merge(
        holiday_data, on=["Date", "Store", "Dept"], how="left"
    )

    if holiday_filter == "Holiday Weeks":
        filtered_df = filtered_df[filtered_df["IsHoliday"] == True]
    elif holiday_filter == "Non-Holiday Weeks":
        filtered_df = filtered_df[filtered_df["IsHoliday"] == False]


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:
    empty_state(
        "No data for these filters",
        "Please select a different Store, Department or Date Range from the sidebar.",
        icon="🔍"
    )
    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_actual_sales = filtered_df["Actual_Sales"].sum()
total_predicted_sales = filtered_df["Predicted_Sales"].sum()
average_weekly_sales = filtered_df["Actual_Sales"].mean()
mae = filtered_df["Error"].abs().mean()
rmse = np.sqrt((filtered_df["Error"] ** 2).mean())
mape = filtered_df["Abs_Percent_Error"].mean()

forecast_bias = total_predicted_sales - total_actual_sales
bias_pct = (forecast_bias / total_actual_sales * 100) if total_actual_sales else 0


# ============================================================
# TABS
# ============================================================

tab_overview, tab_accuracy, tab_insights, tab_store, tab_external, tab_models, tab_data = st.tabs(
    ["📈 Overview", "🎯 Forecast Accuracy", "💡 Insights", "🏪 Store & Dept",
     "🌡️ External Factors", "🤖 Models", "🔍 Raw Data"]
)


# ------------------------------------------------------------
# TAB: OVERVIEW
# ------------------------------------------------------------

with tab_overview:

    section("Key Performance Indicators")

    kpi_html = f"""
    <div class="kpi-row">
        {kpi_card("Total Actual Sales", f"${total_actual_sales:,.0f}", PALETTE["primary_2"], icon="💰")}
        {kpi_card("Average Weekly Sales", f"${average_weekly_sales:,.0f}", PALETTE["accent"], icon="📅")}
        {kpi_card("Predicted Sales", f"${total_predicted_sales:,.0f}", PALETTE["good"] if forecast_bias <= 0 else PALETTE["warn"],
                   f"{bias_pct:+.1f}% vs actual", "up" if bias_pct > 0 else ("down" if bias_pct < 0 else "flat"), icon="🔮")}
        {kpi_card("MAPE", f"{mape:.2f}%", PALETTE["bad"] if mape > 15 else PALETTE["good"], icon="🎯")}
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)

    section("Actual vs Predicted Sales", "Weekly comparison across the selected filters")

    plot_df = filtered_df.sort_values("Date")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=plot_df["Date"], y=plot_df["Actual_Sales"],
        mode="lines+markers", name="Actual Sales",
        line=dict(width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=plot_df["Date"], y=plot_df["Predicted_Sales"],
        mode="lines+markers", name="Predicted Sales",
        line=dict(width=2.5, dash="dot")
    ))
    fig.update_layout(title="Weekly Actual vs Predicted Sales",
                       xaxis_title="Date", yaxis_title="Sales")
    style_fig(fig, height=460)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------
# TAB: FORECAST ACCURACY
# ------------------------------------------------------------

with tab_accuracy:

    section("Forecast Error Over Time")

    error_fig = px.line(plot_df, x="Date", y="Error", title="Prediction Error Over Time")
    error_fig.add_hline(y=0, line_dash="dash", line_color=PALETTE["muted"])
    style_fig(error_fig, height=420)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(error_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    section("Forecast Performance")

    perf_html = f"""
    <div class="kpi-row" style="grid-template-columns:repeat(3,1fr);">
        {kpi_card("Mean Absolute Error", f"{mae:,.2f}", PALETTE["primary_2"], icon="📏")}
        {kpi_card("Root Mean Squared Error", f"{rmse:,.2f}", PALETTE["accent"], icon="📐")}
        {kpi_card("Mean Absolute % Error", f"{mape:.2f}%", PALETTE["warn"], icon="📊")}
    </div>
    """
    st.markdown(perf_html, unsafe_allow_html=True)


# ------------------------------------------------------------
# TAB: BUSINESS INSIGHTS
# ------------------------------------------------------------

with tab_insights:

    section("Business Insights")

    best_week = filtered_df.loc[filtered_df["Actual_Sales"].idxmax()]
    worst_week = filtered_df.loc[filtered_df["Actual_Sales"].idxmin()]
    average_prediction_error = filtered_df["Error"].mean()

    if forecast_bias > 0:
        bias_text = "The model tends to over-predict sales."
        bias_accent = PALETTE["warn"]
    elif forecast_bias < 0:
        bias_text = "The model tends to under-predict sales."
        bias_accent = PALETTE["bad"]
    else:
        bias_text = "Predictions are approximately unbiased."
        bias_accent = PALETTE["good"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            info_card("Highest Sales Week",
                      f"${best_week['Actual_Sales']:,.2f}",
                      f"📅 {best_week['Date'].strftime('%d %b %Y')}",
                      PALETTE["good"], icon="🏆"),
            unsafe_allow_html=True
        )
        st.markdown(
            info_card("Lowest Sales Week",
                      f"${worst_week['Actual_Sales']:,.2f}",
                      f"📅 {worst_week['Date'].strftime('%d %b %Y')}",
                      PALETTE["bad"], icon="📉"),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            info_card("Forecast Bias", f"${abs(forecast_bias):,.2f}", bias_text, bias_accent, icon="⚖️"),
            unsafe_allow_html=True
        )
        st.markdown(
            info_card("Average Prediction Error",
                      f"${average_prediction_error:,.2f}",
                      "Average signed error across the selected period",
                      PALETTE["primary_2"], icon="🧮"),
            unsafe_allow_html=True
        )

    section("Holiday Sales Analysis", "Average weekly sales, holiday vs non-holiday")

    holiday_analysis = sales_df.copy()

    if selected_store != "All":
        holiday_analysis = holiday_analysis[holiday_analysis["Store"] == selected_store]

    if selected_dept != "All":
        holiday_analysis = holiday_analysis[holiday_analysis["Dept"] == selected_dept]

    holiday_analysis = holiday_analysis[
        (holiday_analysis["Date"] >= start_date) & (holiday_analysis["Date"] <= end_date)
    ]

    holiday_summary = (
        holiday_analysis.groupby("IsHoliday")["Weekly_Sales"].mean().reset_index()
    )
    holiday_summary["Period"] = holiday_summary["IsHoliday"].map(
        {True: "Holiday", False: "Non-Holiday"}
    )

    holiday_fig = px.bar(
        holiday_summary, x="Period", y="Weekly_Sales",
        title="Average Sales: Holiday vs Non-Holiday Weeks",
        text_auto=".2s", color="Period",
        color_discrete_sequence=[PALETTE["warn"], PALETTE["primary_2"]]
    )
    holiday_fig.update_layout(showlegend=False)
    style_fig(holiday_fig, height=420)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(holiday_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------
# TAB: STORE & DEPARTMENT PERFORMANCE
# ------------------------------------------------------------

with tab_store:

    if selected_store == "All":

        section("Store Performance", "Top 15 stores by actual sales")

        store_summary = (
            forecast_df.groupby("Store")
            .agg(Actual_Sales=("Actual_Sales", "sum"),
                 Predicted_Sales=("Predicted_Sales", "sum"),
                 MAPE=("Abs_Percent_Error", "mean"))
            .reset_index()
            .sort_values("Actual_Sales", ascending=False)
        )

        store_fig = px.bar(
            store_summary.head(15), x="Store", y="Actual_Sales",
            title="Top 15 Stores by Actual Sales", text_auto=".2s",
            color="Actual_Sales", color_continuous_scale=[PALETTE["panel_2"], PALETTE["primary_2"]]
        )
        style_fig(store_fig, height=460)
        store_fig.update_layout(coloraxis_showscale=False)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(store_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        section("Department Performance", "Top 15 departments by actual sales")

        dept_summary = (
            forecast_df.groupby("Dept")
            .agg(Actual_Sales=("Actual_Sales", "sum"),
                 Predicted_Sales=("Predicted_Sales", "sum"),
                 MAPE=("Abs_Percent_Error", "mean"))
            .reset_index()
            .sort_values("Actual_Sales", ascending=False)
        )

        dept_fig = px.bar(
            dept_summary.head(15), x="Dept", y="Actual_Sales",
            title="Top 15 Departments by Actual Sales", text_auto=".2s",
            color="Actual_Sales", color_continuous_scale=[PALETTE["panel_2"], PALETTE["accent"]]
        )
        style_fig(dept_fig, height=460)
        dept_fig.update_layout(coloraxis_showscale=False)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(dept_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        empty_state(
            "Single-store view active",
            "Store and department breakdowns are shown when "
            "<code>All</code> stores are selected in the sidebar.",
            icon="🏪"
        )


# ------------------------------------------------------------
# TAB: EXTERNAL FACTORS
# ------------------------------------------------------------

with tab_external:

    section("External Factors & Sales", "Relationship between demand and macro/environmental variables")

    factor_df = filtered_sales.copy()

    def factor_scatter(col, title):
        if col not in factor_df.columns:
            return None
        fig = px.scatter(
            factor_df, x=col, y="Weekly_Sales", trendline="ols",
            title=title, opacity=0.55,
            color_discrete_sequence=[PALETTE["primary_2"]]
        )
        style_fig(fig, height=420)
        return fig

    temp_fig = factor_scatter("Temperature", "Sales vs Temperature")
    fuel_fig = factor_scatter("Fuel_Price", "Sales vs Fuel Price")
    cpi_fig = factor_scatter("CPI", "Sales vs CPI")
    unemployment_fig = factor_scatter("Unemployment", "Sales vs Unemployment")

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    for col_slot, fig in [
        (row1_col1, temp_fig), (row1_col2, fuel_fig),
        (row2_col1, cpi_fig), (row2_col2, unemployment_fig),
    ]:
        with col_slot:
            if fig is not None:
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------
# TAB: MODEL COMPARISON
# ------------------------------------------------------------

with tab_models:

    section("Model Comparison", "Standard regression / time-series evaluation metrics")

    if model_results is not None:

        st.dataframe(model_results, use_container_width=True, hide_index=True)

        possible_metric_columns = ["MAE", "RMSE", "MAPE"]
        available_metrics = [c for c in possible_metric_columns if c in model_results.columns]

        if available_metrics:
            selected_metric = st.selectbox("Select evaluation metric", available_metrics)

            model_fig = px.bar(
                model_results, x="Model", y=selected_metric,
                title=f"Model Comparison — {selected_metric}",
                text_auto=".2f", color="Model",
                color_discrete_sequence=CHART_COLORWAY
            )
            model_fig.update_layout(showlegend=False)
            style_fig(model_fig, height=440)

            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(model_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        empty_state(
            "Model comparison not exported yet",
            "The dashboard is currently using the final <code>forecast_output.csv</code>. "
            "Once evaluation results are exported from the notebook into "
            "<code>model_results.csv</code>, this section will automatically display "
            "Linear Regression, Decision Tree, Random Forest, XGBoost, ARIMA and "
            "SARIMAX performance.",
            icon="🤖"
        )


# ------------------------------------------------------------
# TAB: RAW DATA
# ------------------------------------------------------------

with tab_data:

    section("Forecast Data")
    with st.expander("View filtered forecast data", expanded=False):
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    section("Historical Sales Data")
    with st.expander("View filtered historical sales data", expanded=False):
        st.dataframe(filtered_sales, use_container_width=True, hide_index=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-caption">Retail Sales Forecasting · '
    'Machine Learning + Time Series Analysis + Streamlit</div>',
    unsafe_allow_html=True
)