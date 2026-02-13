"""
Enterprise Institutional Effectiveness Dashboard
A decision-support tool for academic medical center leadership.
Built by Per Nilsson | Director, Accreditation & Strategic Planning
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIG & THEME
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Institutional Effectiveness Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Executive color palette — muted, professional
COLORS = {
    "primary": "#1B2A4A",      # deep navy
    "accent": "#2E86AB",       # steel blue
    "success": "#2D936C",      # muted green
    "warning": "#D4A843",      # muted gold
    "danger": "#C44536",       # muted red
    "light_bg": "#F8F9FA",     # near-white
    "text": "#333333",         # dark gray
    "muted": "#8C8C8C",        # medium gray
    "card_border": "#E8ECF0",  # light border
}

st.markdown(f"""
<style>
    /* Global */
    .stApp {{
        background-color: {COLORS['light_bg']};
    }}
    
    /* Remove default padding */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }}
    
    /* Header */
    .dashboard-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, #2A3F6B 100%);
        color: white;
        padding: 1.8rem 2.2rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
    }}
    .dashboard-header h1 {{
        font-size: 1.6rem;
        font-weight: 600;
        margin: 0 0 0.3rem 0;
        letter-spacing: -0.02em;
    }}
    .dashboard-header p {{
        font-size: 0.85rem;
        color: rgba(255,255,255,0.7);
        margin: 0;
    }}
    
    /* KPI Cards */
    .kpi-card {{
        background: white;
        border: 1px solid {COLORS['card_border']};
        border-radius: 10px;
        padding: 1.4rem 1.6rem;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        height: 100%;
    }}
    .kpi-label {{
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {COLORS['muted']};
        margin-bottom: 0.4rem;
    }}
    .kpi-value {{
        font-size: 2.2rem;
        font-weight: 700;
        color: {COLORS['primary']};
        line-height: 1.1;
        margin-bottom: 0.3rem;
    }}
    .kpi-delta {{
        font-size: 0.8rem;
        font-weight: 500;
    }}
    .kpi-delta.positive {{ color: {COLORS['success']}; }}
    .kpi-delta.negative {{ color: {COLORS['danger']}; }}
    .kpi-delta.neutral {{ color: {COLORS['muted']}; }}
    
    /* Section headers */
    .section-header {{
        font-size: 1.05rem;
        font-weight: 600;
        color: {COLORS['primary']};
        margin: 1.6rem 0 0.3rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid {COLORS['accent']};
        display: inline-block;
    }}
    .section-caption {{
        font-size: 0.8rem;
        color: {COLORS['muted']};
        margin-bottom: 1rem;
        font-style: italic;
    }}
    
    /* Chart containers */
    .chart-card {{
        background: white;
        border: 1px solid {COLORS['card_border']};
        border-radius: 10px;
        padding: 1.4rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }}
    .chart-title {{
        font-size: 0.9rem;
        font-weight: 600;
        color: {COLORS['primary']};
        margin-bottom: 0.2rem;
    }}
    .chart-insight {{
        font-size: 0.78rem;
        color: {COLORS['muted']};
        margin-bottom: 0.8rem;
        line-height: 1.4;
    }}
    
    /* Narrative box */
    .narrative-box {{
        background: white;
        border-left: 4px solid {COLORS['accent']};
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.4rem;
        margin: 0.8rem 0;
        font-size: 0.85rem;
        color: {COLORS['text']};
        line-height: 1.6;
    }}
    
    /* Footer */
    .dashboard-footer {{
        text-align: center;
        font-size: 0.72rem;
        color: {COLORS['muted']};
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid {COLORS['card_border']};
    }}
    
    /* Hide Streamlit extras */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    .stDeployButton {{ display: none; }}
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-size: 0.85rem;
        font-weight: 500;
        padding: 0.5rem 1rem;
    }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SYNTHETIC DATA ENGINE
# ─────────────────────────────────────────────
np.random.seed(42)

ACADEMIC_YEARS = ["2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
DEPARTMENTS = [
    "Internal Medicine", "Surgery", "Pediatrics", "OB-GYN",
    "Psychiatry", "Family Medicine", "Neurology", "Emergency Medicine"
]

def generate_education_data():
    return {
        "enrollment": [192, 195, 198, 200, 205, 210],
        "step1_pass": [96.2, 97.1, 95.8, 97.5, 98.1, 97.8],
        "step2_pass": [97.8, 98.2, 97.5, 98.6, 99.0, 98.4],
        "match_rate": [93.5, 94.2, 91.8, 95.1, 96.3, 95.8],
        "top_choice_match": [62.1, 64.5, 58.3, 66.2, 68.1, 67.5],
        "attrition_rate": [3.2, 2.8, 3.5, 2.1, 1.9, 2.2],
        "msq_overall_satisfaction": [3.72, 3.68, 3.55, 3.81, 3.89, 3.92],
        "gq_satisfaction": [78.5, 80.2, 76.1, 82.4, 84.1, 85.3],
    }

def generate_research_data():
    return {
        "total_funding_m": [148.2, 155.6, 162.1, 171.8, 185.3, 192.7],
        "nih_funding_m": [98.5, 103.2, 108.7, 115.4, 124.1, 128.9],
        "faculty_pubs": [1842, 1923, 2015, 2187, 2341, 2456],
        "h_index_median": [18, 19, 19, 20, 21, 22],
        "clinical_trials": [245, 262, 278, 301, 324, 338],
    }

def generate_workforce_data():
    return {
        "total_faculty": [685, 698, 712, 725, 741, 758],
        "pct_female_faculty": [38.2, 39.1, 40.5, 41.8, 43.2, 44.1],
        "pct_urm_faculty": [12.5, 13.1, 13.8, 14.5, 15.2, 15.8],
        "voluntary_turnover": [8.2, 7.8, 9.1, 7.5, 6.9, 7.1],
        "time_to_promotion_yr": [6.8, 6.5, 6.7, 6.3, 6.1, 5.9],
        "dept_satisfaction": {
            dept: round(3.2 + np.random.uniform(0, 1.2), 2) for dept in DEPARTMENTS
        },
    }

def generate_compliance_data():
    return {
        "lcme_standards_met": 93,
        "lcme_total_standards": 95,
        "accreditation_status": "Full (Next visit: 2028)",
        "open_action_items": 4,
        "isa_completion": 97.2,
        "cqi_projects_active": 12,
        "cqi_projects_complete": 8,
        "compliance_training_pct": 94.8,
    }

ed_data = generate_education_data()
res_data = generate_research_data()
wf_data = generate_workforce_data()
comp_data = generate_compliance_data()


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def kpi_card(label, value, delta=None, delta_dir="positive", prefix="", suffix=""):
    delta_html = ""
    if delta is not None:
        arrow = "▲" if delta_dir == "positive" else "▼" if delta_dir == "negative" else "●"
        delta_html = f'<div class="kpi-delta {delta_dir}">{arrow} {delta}</div>'
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{prefix}{value}{suffix}</div>
        {delta_html}
    </div>
    """

def make_trend_chart(years, values, title, insight, color=COLORS["accent"],
                     suffix="", yrange=None, show_target=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=values,
        mode="lines+markers",
        line=dict(color=color, width=2.5),
        marker=dict(size=7, color=color),
        hovertemplate="%{x}: %{y:.1f}" + suffix + "<extra></extra>",
    ))
    if show_target is not None:
        fig.add_hline(
            y=show_target, line_dash="dot",
            line_color=COLORS["muted"],
            annotation_text="Target",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color=COLORS["muted"],
        )
    fig.update_layout(
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            showgrid=False, showline=True,
            linecolor=COLORS["card_border"],
            tickfont=dict(size=10, color=COLORS["muted"]),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#F0F0F0",
            showline=False,
            tickfont=dict(size=10, color=COLORS["muted"]),
            ticksuffix=suffix,
            range=yrange,
        ),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    return fig

def make_bar_chart(categories, values, title, color=COLORS["accent"],
                   horizontal=False, suffix=""):
    if horizontal:
        fig = go.Figure(go.Bar(
            y=categories, x=values,
            orientation="h",
            marker_color=color,
            text=[f"{v}{suffix}" for v in values],
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig.update_layout(
            height=max(200, len(categories) * 35),
            margin=dict(l=10, r=40, t=10, b=10),
            xaxis=dict(showgrid=False, showticklabels=False, showline=False),
            yaxis=dict(showgrid=False, showline=False,
                       tickfont=dict(size=10, color=COLORS["text"]),
                       autorange="reversed"),
        )
    else:
        fig = go.Figure(go.Bar(
            x=categories, y=values,
            marker_color=color,
            text=[f"{v}{suffix}" for v in values],
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig.update_layout(
            height=220,
            margin=dict(l=10, r=10, t=10, b=10),
            yaxis=dict(showgrid=True, gridcolor="#F0F0F0", showline=False,
                       tickfont=dict(size=10, color=COLORS["muted"])),
            xaxis=dict(showgrid=False, showline=True,
                       linecolor=COLORS["card_border"],
                       tickfont=dict(size=10, color=COLORS["muted"])),
        )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    return fig

def make_gauge(value, max_val, label, color=COLORS["success"]):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(suffix="%", font=dict(size=28, color=COLORS["primary"])),
        gauge=dict(
            axis=dict(range=[0, max_val], showticklabels=False),
            bar=dict(color=color, thickness=0.6),
            bgcolor="#F0F0F0",
            borderwidth=0,
            shape="angular",
        ),
    ))
    fig.update_layout(
        height=160,
        margin=dict(l=20, r=20, t=30, b=10),
        paper_bgcolor="white",
    )
    return fig


# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────

# Header
st.markdown(f"""
<div class="dashboard-header">
    <h1>Institutional Effectiveness Dashboard</h1>
    <p>Academic Year 2024–25  ·  Synthetic demonstration data  ·  Updated {datetime.now().strftime('%B %d, %Y')}</p>
</div>
""", unsafe_allow_html=True)

# ── TOP-LINE KPIs ──
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(kpi_card("Total Enrollment", ed_data["enrollment"][-1],
                         "+5 vs. prior year", "positive"), unsafe_allow_html=True)
with c2:
    st.markdown(kpi_card("Match Rate", f'{ed_data["match_rate"][-1]}',
                         "−0.5pp vs. prior year", "negative", suffix="%"), unsafe_allow_html=True)
with c3:
    st.markdown(kpi_card("Research Funding", f'{res_data["total_funding_m"][-1]}',
                         "+$7.4M vs. prior year", "positive", prefix="$", suffix="M"), unsafe_allow_html=True)
with c4:
    st.markdown(kpi_card("Faculty Count", wf_data["total_faculty"][-1],
                         "+17 net new", "positive"), unsafe_allow_html=True)
with c5:
    st.markdown(kpi_card("LCME Standards Met",
                         f'{comp_data["lcme_standards_met"]}/{comp_data["lcme_total_standards"]}',
                         "2 newly met this cycle", "positive"), unsafe_allow_html=True)

st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)

# ── TABS ──
tab_ed, tab_res, tab_wf, tab_comp = st.tabs([
    "📚  Education", "🔬  Research", "👥  Workforce", "✅  Compliance"
])

# ════════════════════════════════════════════
# EDUCATION TAB
# ════════════════════════════════════════════
with tab_ed:
    st.markdown('<div class="section-header">Education Outcomes</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Decision focus: Are students succeeding, and where do we need to intervene?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">USMLE Step 1 Pass Rate (%)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">Consistently above national average. Stable performance suggests curriculum strength.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_trend_chart(
            ACADEMIC_YEARS, ed_data["step1_pass"], "Step 1 Pass Rate",
            "", color=COLORS["success"], suffix="%", yrange=[90, 100],
            show_target=96.0
        ), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Residency Match Rate (%)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">Recovered from 2021 dip. Watch whether top-choice rate sustains above 65%.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_trend_chart(
            ACADEMIC_YEARS, ed_data["match_rate"], "Match Rate",
            "", color=COLORS["accent"], suffix="%", yrange=[85, 100],
            show_target=94.0
        ), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Student Satisfaction (MSQ Overall, 1–5 Scale)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">Steady climb since COVID low in 2020–21. Approaching 4.0 threshold for first time.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_trend_chart(
            ACADEMIC_YEARS, ed_data["msq_overall_satisfaction"], "MSQ Satisfaction",
            "", color=COLORS["warning"], suffix="", yrange=[3.0, 4.5],
            show_target=4.0
        ), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Attrition Rate (%)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">Below 2.5% for two consecutive years. Retention initiatives are working.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_trend_chart(
            ACADEMIC_YEARS, ed_data["attrition_rate"], "Attrition",
            "", color=COLORS["danger"], suffix="%", yrange=[0, 5],
            show_target=2.5
        ), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="narrative-box">
        <strong>What this means:</strong> Education outcomes are strong and improving. The match rate dip in 2020–21
        reflected national pandemic disruption, not a structural weakness. The key strategic question is whether
        rising satisfaction translates to improved GQ metrics, which directly affect reputation and rankings.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# RESEARCH TAB
# ════════════════════════════════════════════
with tab_res:
    st.markdown('<div class="section-header">Research Enterprise</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Decision focus: Is research funding growing, and are we diversifying revenue?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Total Research Funding ($M)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">30% growth over 6 years. NIH share remains ~67%, suggesting healthy but concentrated portfolio.</div>', unsafe_allow_html=True)

        fig = go.Figure()
        non_nih = [t - n for t, n in zip(res_data["total_funding_m"], res_data["nih_funding_m"])]
        fig.add_trace(go.Bar(
            x=ACADEMIC_YEARS, y=res_data["nih_funding_m"],
            name="NIH", marker_color=COLORS["accent"],
        ))
        fig.add_trace(go.Bar(
            x=ACADEMIC_YEARS, y=non_nih,
            name="Other", marker_color=COLORS["warning"],
        ))
        fig.update_layout(
            barmode="stack", height=240,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
            xaxis=dict(showgrid=False, showline=True, linecolor=COLORS["card_border"],
                       tickfont=dict(size=10, color=COLORS["muted"])),
            yaxis=dict(showgrid=True, gridcolor="#F0F0F0", showline=False,
                       tickfont=dict(size=10, color=COLORS["muted"]), tickprefix="$", ticksuffix="M"),
            hoverlabel=dict(bgcolor="white", font_size=12),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Faculty Publications (Peer-Reviewed)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">Consistent upward trend. 33% increase since 2019–20 reflects hiring and productivity gains.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_trend_chart(
            ACADEMIC_YEARS, res_data["faculty_pubs"], "Publications",
            "", color=COLORS["primary"], suffix=""
        ), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Active Clinical Trials</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">38% growth signals expanding clinical research enterprise and industry partnerships.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_trend_chart(
            ACADEMIC_YEARS, res_data["clinical_trials"], "Clinical Trials",
            "", color=COLORS["success"], suffix=""
        ), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Median Faculty h-index</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">Steady improvement. Crossing 20 is a meaningful benchmark for research-intensive schools.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_trend_chart(
            ACADEMIC_YEARS, res_data["h_index_median"], "h-index",
            "", color=COLORS["accent"], suffix="", yrange=[15, 25]
        ), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="narrative-box">
        <strong>What this means:</strong> The research enterprise is on an upward trajectory across all indicators.
        The strategic risk is NIH concentration — if federal funding tightens, the institution needs non-NIH
        revenue streams (industry, state, philanthropy) to sustain momentum. Consider setting a target of
        reducing NIH dependency to &lt;60% of total funding within 3 years.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# WORKFORCE TAB
# ════════════════════════════════════════════
with tab_wf:
    st.markdown('<div class="section-header">Faculty & Workforce</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Decision focus: Are we building a diverse, stable, and productive workforce?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Faculty Diversity Trends</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">Both female and URM representation are rising, but URM pace needs to accelerate to meet strategic goals.</div>', unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ACADEMIC_YEARS, y=wf_data["pct_female_faculty"],
            name="% Female", mode="lines+markers",
            line=dict(color=COLORS["accent"], width=2.5),
            marker=dict(size=7),
        ))
        fig.add_trace(go.Scatter(
            x=ACADEMIC_YEARS, y=wf_data["pct_urm_faculty"],
            name="% URM", mode="lines+markers",
            line=dict(color=COLORS["warning"], width=2.5),
            marker=dict(size=7),
        ))
        fig.update_layout(
            height=220,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
            xaxis=dict(showgrid=False, showline=True, linecolor=COLORS["card_border"],
                       tickfont=dict(size=10, color=COLORS["muted"])),
            yaxis=dict(showgrid=True, gridcolor="#F0F0F0", showline=False,
                       tickfont=dict(size=10, color=COLORS["muted"]), ticksuffix="%",
                       range=[0, 50]),
            hoverlabel=dict(bgcolor="white", font_size=12),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Voluntary Turnover Rate (%)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">Below 7.5% and declining. Retention strategies and mentorship investment are paying off.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_trend_chart(
            ACADEMIC_YEARS, wf_data["voluntary_turnover"], "Turnover",
            "", color=COLORS["danger"], suffix="%", yrange=[4, 12],
            show_target=7.5
        ), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Median Time to Promotion (Years)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">Trending below 6 years for the first time. Streamlined review processes are accelerating career progression.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_trend_chart(
            ACADEMIC_YEARS, wf_data["time_to_promotion_yr"], "Years",
            "", color=COLORS["primary"], suffix=" yr", yrange=[4, 8],
            show_target=6.0
        ), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Department Satisfaction Scores (1–5)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">Most departments above 3.5. Identify low-scoring departments for targeted leadership development.</div>', unsafe_allow_html=True)
        depts = list(wf_data["dept_satisfaction"].keys())
        scores = list(wf_data["dept_satisfaction"].values())
        # Sort by score
        sorted_pairs = sorted(zip(depts, scores), key=lambda x: x[1])
        depts_sorted = [p[0] for p in sorted_pairs]
        scores_sorted = [p[1] for p in sorted_pairs]
        colors_bar = [COLORS["danger"] if s < 3.5 else COLORS["accent"] for s in scores_sorted]

        fig = go.Figure(go.Bar(
            y=depts_sorted, x=scores_sorted,
            orientation="h",
            marker_color=colors_bar,
            text=[f"{v:.1f}" for v in scores_sorted],
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig.update_layout(
            height=280,
            margin=dict(l=10, r=40, t=10, b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False, showticklabels=False, showline=False, range=[0, 5]),
            yaxis=dict(showgrid=False, showline=False,
                       tickfont=dict(size=10, color=COLORS["text"])),
            hoverlabel=dict(bgcolor="white", font_size=12),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="narrative-box">
        <strong>What this means:</strong> The workforce is stabilizing and diversifying. Two priorities emerge:
        (1) URM faculty recruitment needs dedicated pipeline programs to reach 18% by 2027, and
        (2) department-level satisfaction gaps require chair-specific action plans. The declining time-to-promotion
        is a competitive advantage for recruitment.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# COMPLIANCE TAB
# ════════════════════════════════════════════
with tab_comp:
    st.markdown('<div class="section-header">Accreditation & Compliance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Decision focus: Are we ready for the next LCME visit, and where are the gaps?</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_card("Accreditation Status", "Full",
                             "Next visit: 2028", "positive"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card("Standards Met",
                             f'{comp_data["lcme_standards_met"]} of {comp_data["lcme_total_standards"]}',
                             "97.9% compliance", "positive"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card("Open Action Items", comp_data["open_action_items"],
                             "Down from 7 last year", "positive"), unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">ISA Completion</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">On track for full completion before visit.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(comp_data["isa_completion"], 100, "ISA", COLORS["success"]),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">CQI Projects</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">12 active, 8 completed this cycle.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(
            comp_data["cqi_projects_complete"] / (comp_data["cqi_projects_active"] + comp_data["cqi_projects_complete"]) * 100,
            100, "CQI", COLORS["accent"]
        ), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col6:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Compliance Training</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-insight">94.8% complete. Target: 98% by June.</div>', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(comp_data["compliance_training_pct"], 100, "Training", COLORS["warning"]),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # LCME Standards Heatmap
    st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">LCME Standards Compliance Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-insight">Green = met, gold = in progress, red = needs attention. Two standards require action before 2028 visit.</div>', unsafe_allow_html=True)

    np.random.seed(99)
    standards = []
    for i in range(1, 13):
        for j in range(1, 9):
            sid = f"{i}.{j}"
            r = np.random.random()
            if r < 0.03:
                status = "Needs Attention"
                color = COLORS["danger"]
            elif r < 0.08:
                status = "In Progress"
                color = COLORS["warning"]
            else:
                status = "Met"
                color = COLORS["success"]
            standards.append({"element": i, "sub": j, "status": status, "color": color, "id": sid})

    df_standards = pd.DataFrame(standards)
    pivot = df_standards.pivot(index="sub", columns="element", values="status")

    color_map = {"Met": COLORS["success"], "In Progress": COLORS["warning"], "Needs Attention": COLORS["danger"]}
    z_numeric = pivot.map(lambda x: 2 if x == "Met" else 1 if x == "In Progress" else 0)

    fig = go.Figure(go.Heatmap(
        z=z_numeric.values,
        x=[f"Std {i}" for i in range(1, 13)],
        y=[f"Elem {j}" for j in range(1, 9)],
        colorscale=[
            [0, COLORS["danger"]],
            [0.5, COLORS["warning"]],
            [1.0, COLORS["success"]],
        ],
        showscale=False,
        hovertemplate="Standard %{x}, Element %{y}<br>Status: %{text}<extra></extra>",
        text=pivot.values,
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(tickfont=dict(size=9, color=COLORS["muted"]), side="top"),
        yaxis=dict(tickfont=dict(size=9, color=COLORS["muted"]), autorange="reversed"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="narrative-box">
        <strong>What this means:</strong> Accreditation posture is strong with 97.9% of standards met. The 4 open
        action items are tracked and assigned. Priority before the 2028 visit: close the 2 "needs attention"
        standards (likely curriculum mapping completeness and assessment documentation) and achieve 98%
        compliance training completion by June.
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ──
st.markdown(f"""
<div class="dashboard-footer">
    Enterprise Institutional Effectiveness Dashboard  ·  Demonstration with synthetic data<br>
    Built by Per Nilsson  ·  Director, Accreditation & Strategic Planning  ·  {datetime.now().year}
</div>
""", unsafe_allow_html=True)
