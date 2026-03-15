import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GeoMarketing · Cluster Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0b0f1a;
    --surface:   #121828;
    --surface2:  #1a2236;
    --border:    #1f2d47;
    --accent:    #3b82f6;
    --accent2:   #8b5cf6;
    --success:   #10b981;
    --warn:      #f59e0b;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --radius:    14px;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem; max-width: 1600px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .css-1d391kg { padding-top: 1.5rem; }

.sidebar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text);
    padding: 0 1rem 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.sidebar-logo span { color: var(--accent); }

[data-testid="stSidebar"] label {
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 2rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border);
}
.page-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    margin: 0;
    background: linear-gradient(135deg, #e2e8f0 30%, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.page-header p {
    font-size: 0.85rem;
    color: var(--muted);
    margin: 0.4rem 0 0;
}
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    color: var(--success);
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    letter-spacing: 0.04em;
}
.status-dot {
    width: 6px; height: 6px;
    background: var(--success);
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; } 50% { opacity:0.4; }
}

/* ── KPI cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1rem; margin-bottom: 1.75rem; }
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color .2s;
}
.kpi-card:hover { border-color: var(--accent); }
.kpi-card::before {
    content: '';
    position: absolute; top:0; left:0; right:0; height:3px;
    background: var(--accent-grad, linear-gradient(90deg, var(--accent), var(--accent2)));
}
.kpi-card.green::before { --accent-grad: linear-gradient(90deg,#10b981,#34d399); }
.kpi-card.amber::before { --accent-grad: linear-gradient(90deg,#f59e0b,#fbbf24); }
.kpi-label {
    font-size: 0.7rem; font-weight: 500;
    letter-spacing: 0.09em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.75rem; font-weight: 700;
    letter-spacing: -0.03em; line-height: 1;
    color: var(--text);
}
.kpi-sub { font-size: 0.75rem; color: var(--muted); margin-top: 0.35rem; }

/* ── Tabs ── */
[data-testid="stTabs"] button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 0.6rem 1.1rem !important;
    transition: color .15s !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--text) !important;
    border-bottom: 2px solid var(--accent) !important;
    background: transparent !important;
}
[data-testid="stTabs"] { border-bottom: 1px solid var(--border) !important; }

/* ── Section title ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem; font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--text);
    margin: 1.5rem 0 0.75rem;
}
.section-subtitle {
    font-size: 0.8rem; color: var(--muted); margin-top: -0.5rem; margin-bottom: 1rem;
}

/* ── Chart wrapper ── */
.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem;
}

/* ── Info banner ── */
.info-banner {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.25);
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    font-size: 0.82rem;
    color: #93c5fd;
    display: flex; align-items: center; gap: 0.6rem;
}

/* ── Plotly dark override ── */
.js-plotly-plot .plotly .bg { fill: transparent !important; }
</style>
""", unsafe_allow_html=True)


# ── DATA ───────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("df_final_com_clusters.csv")

try:
    df = load_data()
except Exception:
    st.error("⚠️  Arquivo **df_final_com_clusters.csv** não encontrado.")
    st.stop()


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">Geo<span>MKT</span> · Clusters</div>', unsafe_allow_html=True)

    st.markdown("##### Estados (UF)")
    ufs = st.multiselect(
        "Estados",
        options=sorted(df['UF'].unique()),
        default=list(df['UF'].unique()),
        label_visibility="collapsed",
    )

    st.markdown("##### Cidades")
    city_opts = sorted(df[df['UF'].isin(ufs)]['Cidade'].unique())
    cidades = st.multiselect(
        "Cidades",
        options=city_opts,
        default=city_opts[:2],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        f'<div style="font-size:0.72rem;color:var(--muted);line-height:1.7">'
        f'<b style="color:var(--text)">{len(df)} bairros</b> no dataset<br>'
        f'<b style="color:var(--text)">{df["cluster"].nunique()}</b> segmentos identificados<br>'
        f'<b style="color:var(--text)">{df["UF"].nunique()}</b> estados cobertos</div>',
        unsafe_allow_html=True,
    )

df_filt = df[(df['UF'].isin(ufs)) & (df['Cidade'].isin(cidades))]


# ── PLOTLY THEME ───────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#94a3b8", size=12),
    margin=dict(l=16, r=16, t=40, b=16),
    xaxis=dict(gridcolor="#1f2d47", linecolor="#1f2d47", tickcolor="#64748b"),
    yaxis=dict(gridcolor="#1f2d47", linecolor="#1f2d47", tickcolor="#64748b"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1f2d47", borderwidth=1),
    colorway=["#3b82f6","#8b5cf6","#10b981","#f59e0b","#ef4444","#06b6d4"],
)

CLUSTER_COLORS = ["#3b82f6","#8b5cf6","#10b981","#f59e0b","#ef4444","#06b6d4"]


# ── PAGE HEADER ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
  <div>
    <h1>Segmentação de Mercado</h1>
    <p>Análise geomarketing · {len(df_filt):,} bairros selecionados</p>
  </div>
  <span class="status-badge"><span class="status-dot"></span>Live</span>
</div>
""", unsafe_allow_html=True)


# ── KPI CARDS ──────────────────────────────────────────────────────────────────
avg_income  = df_filt['income'].mean()
total_pop   = df_filt['people'].sum()
n_clusters  = df['cluster'].nunique()

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">Renda Média</div>
    <div class="kpi-value">R$ {avg_income:,.0f}</div>
    <div class="kpi-sub">Média dos bairros filtrados</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-label">População Total</div>
    <div class="kpi-value">{total_pop:,.0f}</div>
    <div class="kpi-sub">Soma dos bairros filtrados</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-label">Segmentos</div>
    <div class="kpi-value">{n_clusters}</div>
    <div class="kpi-sub">Clusters identificados no dataset</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── TABS ───────────────────────────────────────────────────────────────────────
tabs = st.tabs(["🗺️  Mapa Geográfico", "📊  Perfil dos Clusters", "🧬  Espaço PCA"])


# ── TAB 1 · MAP ───────────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown('<div class="section-title">Distribuição Espacial por Segmento</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Cada ponto representa um bairro, colorido por cluster de mercado.</div>', unsafe_allow_html=True)

    cores_folium = ['#3b82f6','#8b5cf6','#10b981','#f59e0b','#ef4444','#06b6d4']

    m = folium.Map(
        location=[df_filt['Latitude'].mean(), df_filt['Longitude'].mean()],
        zoom_start=11,
        tiles='cartodbdark_matter',  # dark base map
    )

    for _, row in df_filt.iterrows():
        color = cores_folium[int(row['cluster']) % len(cores_folium)]
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            weight=1.5,
            popup=folium.Popup(
                f"<b>{row['Bairro']}</b><br>Cluster: {row['cluster_nome']}<br>"
                f"Renda: R$ {row['income']:,.0f}<br>Pop.: {row['people']:,.0f}",
                max_width=200,
            ),
        ).add_to(m)

    st_folium(m, width="100%", height=500)


# ── TAB 2 · RADAR ─────────────────────────────────────────────────────────────
with tabs[1]:
    col_left, col_right = st.columns([1.1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-title">Assinatura de Cada Segmento</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Valores normalizados 0–1 para comparação entre variáveis.</div>', unsafe_allow_html=True)

        features_radar = ['income', 'people', 'cons_a_total', 'class_a1', 'age_adults', 'density']
        perfil = df.groupby('cluster_nome')[features_radar].mean()
        perfil_norm = (perfil - perfil.min()) / (perfil.max() - perfil.min())

        fig_radar = go.Figure()
        for i, name in enumerate(perfil_norm.index):
            fig_radar.add_trace(go.Scatterpolar(
                r=list(perfil_norm.iloc[i].values) + [perfil_norm.iloc[i].values[0]],
                theta=features_radar + [features_radar[0]],
                fill='toself',
                name=name,
                line=dict(color=CLUSTER_COLORS[i % len(CLUSTER_COLORS)], width=2),
                fillcolor=CLUSTER_COLORS[i % len(CLUSTER_COLORS)].replace('#','rgba(') + ',0.12)' if False else CLUSTER_COLORS[i % len(CLUSTER_COLORS)],
                opacity=0.85,
            ))

        fig_radar.update_layout(
            **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ('xaxis','yaxis')},
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0,1], gridcolor="#1f2d47", tickcolor="#64748b", tickfont=dict(size=10)),
                angularaxis=dict(gridcolor="#1f2d47", tickcolor="#64748b"),
            ),
            height=420,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-title">Renda Média por Segmento</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Comparativo direto de poder aquisitivo.</div>', unsafe_allow_html=True)

        income_by_cluster = df.groupby('cluster_nome')['income'].mean().sort_values(ascending=True).reset_index()

        fig_bar = go.Figure(go.Bar(
            x=income_by_cluster['income'],
            y=income_by_cluster['cluster_nome'],
            orientation='h',
            marker=dict(
                color=income_by_cluster['income'],
                colorscale=[[0,'#1f2d47'],[0.5,'#3b82f6'],[1,'#8b5cf6']],
                showscale=False,
            ),
            text=[f"R$ {v:,.0f}" for v in income_by_cluster['income']],
            textposition='outside',
            textfont=dict(size=11, color='#94a3b8'),
        ))
        fig_bar.update_layout(**PLOTLY_LAYOUT, height=420)
        st.plotly_chart(fig_bar, use_container_width=True)


# ── TAB 3 · PCA ───────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown('<div class="section-title">Separação Estatística — Projeção PCA 2D</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Quanto mais separados os grupos, mais distintos são os segmentos.</div>', unsafe_allow_html=True)

    if 'pca_1' in df.columns and 'pca_2' in df.columns:
        fig_pca = px.scatter(
            df_filt, x='pca_1', y='pca_2',
            color='cluster_nome',
            hover_name='Bairro',
            color_discrete_sequence=CLUSTER_COLORS,
            opacity=0.8,
        )
        fig_pca.update_traces(marker=dict(size=8, line=dict(width=0.5, color='#0b0f1a')))
        fig_pca.update_layout(**PLOTLY_LAYOUT, height=500)
        st.plotly_chart(fig_pca, use_container_width=True)
    else:
        st.markdown("""
        <div class="info-banner">
            ℹ️  Execute o PCA no notebook e salve as colunas <b>pca_1</b> e <b>pca_2</b> no CSV para visualizar este gráfico.
        </div>
        """, unsafe_allow_html=True)
