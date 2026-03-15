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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Palette (light, clean — like the reference images) ── */
:root {
    --bg:       #f4f6f9;
    --white:    #ffffff;
    --border:   #e2e6ed;
    --text:     #1a1f2e;
    --muted:    #6b7280;
    --accent:   #c0392b;
    --blue:     #2563eb;
    --teal:     #0891b2;
    --orange:   #d97706;
    --green:    #16a34a;
    --radius:   8px;
    --shadow:   0 1px 3px rgba(0,0,0,0.07), 0 1px 2px rgba(0,0,0,0.04);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide Streamlit chrome but keep sidebar toggle intact */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    padding: 1.75rem 2rem 3rem !important;
    max-width: 1440px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--white) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
    padding-left: 1.25rem;
    padding-right: 1.25rem;
}

.sb-section {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.25rem 0 0.4rem;
}

.sb-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.25rem;
    line-height: 1.2;
}
.sb-title span { color: var(--accent); }
.sb-subtitle {
    font-size: 0.75rem;
    color: var(--muted);
    margin-bottom: 1.25rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border);
}

.sb-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.8rem;
    color: var(--muted);
}
.sb-stat b { color: var(--text); font-weight: 600; }

[data-testid="stSidebar"] label {
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    color: var(--text) !important;
}

/* ── Page title ── */
.page-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text);
    margin: 0 0 0.15rem;
    letter-spacing: -0.02em;
}
.page-meta {
    font-size: 0.8rem;
    color: var(--muted);
    margin-bottom: 1.5rem;
}
.page-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 0 0 1.5rem;
}

/* ── KPI cards ── */
.kpi-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.kpi-card {
    flex: 1;
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.25rem;
    box-shadow: var(--shadow);
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--muted);
    margin-bottom: 0.4rem;
}
.kpi-value {
    font-size: 1.65rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
    line-height: 1;
}
.kpi-sub {
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 0.3rem;
}
.kpi-card.accent .kpi-value { color: var(--accent); }
.kpi-card.blue   .kpi-value { color: var(--blue);   }
.kpi-card.green  .kpi-value { color: var(--green);  }

/* ── Tabs ── */
[data-testid="stTabs"] { background: transparent !important; }
[data-testid="stTabs"] button {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    padding: 0.55rem 1rem !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--text) !important;
    font-weight: 600 !important;
    border-bottom: 2px solid var(--accent) !important;
    background: transparent !important;
}
[data-testid="stTabs"] button:hover {
    color: var(--text) !important;
    background: transparent !important;
}

/* ── Section titles ── */
.sec-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text);
    margin: 1.25rem 0 0.2rem;
}
.sec-sub {
    font-size: 0.76rem;
    color: var(--muted);
    margin-bottom: 0.75rem;
}

/* ── Info box ── */
.info-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 3px solid var(--blue);
    border-radius: var(--radius);
    padding: 0.85rem 1.1rem;
    font-size: 0.8rem;
    color: #1e40af;
}

.js-plotly-plot .plotly .bg { fill: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR TOGGLE FIX (JS) ────────────────────────────────────────────────────
# CSS alone cannot reliably fix this — Streamlit re-renders and overwrites styles.
# A MutationObserver watches the DOM and re-applies visibility whenever Streamlit
# touches the collapsed control element.
st.markdown("""
<script>
(function() {
    function fixToggle() {
        // The arrow shown when sidebar is collapsed
        const collapsed = window.parent.document.querySelector('[data-testid="stSidebarCollapsedControl"]');
        if (collapsed) {
            collapsed.style.setProperty('visibility', 'visible', 'important');
            collapsed.style.setProperty('display', 'flex', 'important');
            collapsed.style.setProperty('opacity', '1', 'important');
            collapsed.style.setProperty('pointer-events', 'auto', 'important');
            collapsed.style.setProperty('z-index', '999999', 'important');
            collapsed.style.setProperty('background', '#ffffff', 'important');
            collapsed.style.setProperty('border', '1px solid #e2e6ed', 'important');
            collapsed.style.setProperty('border-radius', '0 8px 8px 0', 'important');
            collapsed.style.setProperty('box-shadow', '2px 2px 6px rgba(0,0,0,0.08)', 'important');
        }
        // The arrow inside the open sidebar
        const collapseBtn = window.parent.document.querySelector('[data-testid="stSidebarCollapseButton"]');
        if (collapseBtn) {
            collapseBtn.style.setProperty('visibility', 'visible', 'important');
            collapseBtn.style.setProperty('opacity', '1', 'important');
            collapseBtn.style.setProperty('pointer-events', 'auto', 'important');
        }
    }

    // Run immediately and on every DOM mutation
    fixToggle();
    const observer = new MutationObserver(fixToggle);
    observer.observe(window.parent.document.body, { childList: true, subtree: true, attributes: true });
})();
</script>
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
    st.markdown("""
        <div class="sb-title">Geo<span>Marketing</span></div>
        <div class="sb-subtitle">Cluster Analysis Dashboard</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Filtros</div>', unsafe_allow_html=True)

    ufs = st.multiselect(
        "Estados (UF)",
        options=sorted(df['UF'].unique()),
        default=list(df['UF'].unique()),
    )

    city_opts = sorted(df[df['UF'].isin(ufs)]['Cidade'].unique())
    cidades = st.multiselect(
        "Cidades",
        options=city_opts,
        default=city_opts[:2],
    )

    st.markdown('<div class="sb-section" style="margin-top:1.5rem">Resumo</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sb-stat"><span>Bairros no dataset</span><b>{len(df):,}</b></div>
        <div class="sb-stat"><span>Segmentos</span><b>{df['cluster'].nunique()}</b></div>
        <div class="sb-stat"><span>Estados</span><b>{df['UF'].nunique()}</b></div>
        <div class="sb-stat"><span>Cidades</span><b>{df['Cidade'].nunique()}</b></div>
    """, unsafe_allow_html=True)

df_filt = df[(df['UF'].isin(ufs)) & (df['Cidade'].isin(cidades))]


# ── PLOTLY THEME ───────────────────────────────────────────────────────────────
PL = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#6b7280", size=11),
    margin=dict(l=10, r=10, t=36, b=10),
    xaxis=dict(gridcolor="#e2e6ed", linecolor="#e2e6ed", tickcolor="#9ca3af", zeroline=False),
    yaxis=dict(gridcolor="#e2e6ed", linecolor="#e2e6ed", tickcolor="#9ca3af", zeroline=False),
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#e2e6ed",
        borderwidth=1,
        font=dict(size=11),
    ),
    colorway=["#c0392b","#2563eb","#0891b2","#d97706","#16a34a","#7c3aed"],
)

COLORS = ["#c0392b","#2563eb","#0891b2","#d97706","#16a34a","#7c3aed"]


# ── PAGE TITLE ─────────────────────────────────────────────────────────────────
st.markdown(f"""
    <div class="page-title">Segmentação Inteligente de Mercado</div>
    <div class="page-meta">
        Análise geomarketing &nbsp;·&nbsp; {len(df_filt):,} bairros selecionados
        &nbsp;·&nbsp; {len(cidades)} cidade(s)
    </div>
""", unsafe_allow_html=True)
st.markdown('<hr class="page-divider">', unsafe_allow_html=True)


# ── KPI CARDS ──────────────────────────────────────────────────────────────────
avg_income = df_filt['income'].mean() if not df_filt.empty else 0
total_pop  = df_filt['people'].sum()  if not df_filt.empty else 0
n_clusters = df['cluster'].nunique()
n_bairros  = len(df_filt)

income_display = f"R$ {avg_income:,.0f}" if not df_filt.empty else "—"

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card blue">
    <div class="kpi-label">Bairros Selecionados</div>
    <div class="kpi-value">{n_bairros:,}</div>
    <div class="kpi-sub">de {len(df):,} no dataset total</div>
  </div>
  <div class="kpi-card accent">
    <div class="kpi-label">Renda Média</div>
    <div class="kpi-value">{income_display}</div>
    <div class="kpi-sub">Média dos bairros filtrados</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-label">População Total</div>
    <div class="kpi-value">{total_pop:,.0f}</div>
    <div class="kpi-sub">Soma dos bairros filtrados</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Segmentos</div>
    <div class="kpi-value">{n_clusters}</div>
    <div class="kpi-sub">Clusters identificados</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── TABS ───────────────────────────────────────────────────────────────────────
tabs = st.tabs(["🗺️  Mapa Geográfico", "📊  Perfil dos Clusters", "🧬  Espaço PCA"])


# ── TAB 1 · MAP ───────────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown('<div class="sec-title">Distribuição Espacial por Segmento</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Cada ponto representa um bairro, colorido pelo seu cluster de mercado.</div>', unsafe_allow_html=True)

    if df_filt.empty:
        st.markdown("""
        <div style="
            display:flex; flex-direction:column; align-items:center; justify-content:center;
            height:420px; background:var(--white); border:1px solid var(--border);
            border-radius:var(--radius); gap:0.75rem; color:var(--muted);
        ">
            <svg width="40" height="40" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"/>
            </svg>
            <span style="font-size:0.95rem; font-weight:600; color:var(--text)">Nenhuma cidade selecionada</span>
            <span style="font-size:0.8rem;">Selecione ao menos uma cidade no painel lateral para visualizar o mapa.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        lat_min, lat_max = df_filt['Latitude'].min(), df_filt['Latitude'].max()
        lon_min, lon_max = df_filt['Longitude'].min(), df_filt['Longitude'].max()

        m = folium.Map(tiles='cartodbpositron')
        m.fit_bounds([[lat_min, lon_min], [lat_max, lon_max]], padding=[30, 30])

        for _, row in df_filt.iterrows():
            color = COLORS[int(row['cluster']) % len(COLORS)]
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=7,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.75,
                weight=1,
                popup=folium.Popup(
                    f"<b style='font-family:Inter'>{row['Bairro']}</b><br>"
                    f"Cluster: {row['cluster_nome']}<br>"
                    f"Renda: R$ {row['income']:,.0f}<br>"
                    f"Pop.: {row['people']:,.0f}",
                    max_width=200,
                ),
            ).add_to(m)

        st_folium(m, width="100%", height=500)


# ── TAB 2 · CLUSTER PROFILES ──────────────────────────────────────────────────
with tabs[1]:
    col_l, col_r = st.columns(2, gap="medium")

    features_radar = ['income', 'people', 'cons_a_total', 'class_a1', 'age_adults', 'density']
    perfil = df.groupby('cluster_nome')[features_radar].mean()
    perfil_norm = (perfil - perfil.min()) / (perfil.max() - perfil.min())

    with col_l:
        st.markdown('<div class="sec-title">Perfil Normalizado por Segmento</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Valores normalizados 0–1 para comparação entre variáveis.</div>', unsafe_allow_html=True)

        fig_radar = go.Figure()
        for i, name in enumerate(perfil_norm.index):
            vals = list(perfil_norm.iloc[i].values)
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=features_radar + [features_radar[0]],
                fill='toself',
                name=name,
                line=dict(color=COLORS[i % len(COLORS)], width=2),
                opacity=0.75,
            ))

        fig_radar.update_layout(
            **{k: v for k, v in PL.items() if k not in ('xaxis', 'yaxis')},
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True, range=[0, 1],
                    gridcolor="#e2e6ed", tickcolor="#9ca3af",
                    tickfont=dict(size=9), tickvals=[0.25, 0.5, 0.75, 1.0],
                ),
                angularaxis=dict(gridcolor="#e2e6ed", tickfont=dict(size=11, color="#374151")),
            ),
            height=400,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_r:
        st.markdown('<div class="sec-title">Renda Média por Segmento</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Comparativo direto de poder aquisitivo entre clusters.</div>', unsafe_allow_html=True)

        income_df = (
            df.groupby('cluster_nome')['income']
            .mean()
            .sort_values(ascending=True)
            .reset_index()
        )

        fig_bar = go.Figure(go.Bar(
            x=income_df['income'],
            y=income_df['cluster_nome'],
            orientation='h',
            marker=dict(color=COLORS[:len(income_df)], line=dict(width=0)),
            text=[f"R$ {v:,.0f}" for v in income_df['income']],
            textposition='outside',
            textfont=dict(size=11, color="#374151"),
        ))
        pl_bar = {**PL, 'xaxis': dict(**PL['xaxis'], title=dict(text="Renda Média (R$)", font=dict(size=11)))}
        fig_bar.update_layout(**pl_bar, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    # Population bar
    st.markdown('<div class="sec-title">População Total por Segmento</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Tamanho de mercado potencial por cluster (bairros filtrados).</div>', unsafe_allow_html=True)

    pop_df = (
        df_filt.groupby('cluster_nome')['people']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_pop = go.Figure(go.Bar(
        x=pop_df['cluster_nome'],
        y=pop_df['people'],
        marker=dict(color=COLORS[:len(pop_df)], line=dict(width=0)),
        text=[f"{v:,.0f}" for v in pop_df['people']],
        textposition='outside',
        textfont=dict(size=11, color="#374151"),
    ))
    pl_pop = {**PL, 'yaxis': dict(**PL['yaxis'], title=dict(text="População", font=dict(size=11)))}
    fig_pop.update_layout(**pl_pop, height=300)
    st.plotly_chart(fig_pop, use_container_width=True)


# ── TAB 3 · PCA ───────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown('<div class="sec-title">Separação Estatística — Projeção PCA 2D</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Quanto mais separados os grupos, mais distintos são os segmentos de mercado.</div>', unsafe_allow_html=True)

    if 'pca_1' in df.columns and 'pca_2' in df.columns:
        fig_pca = px.scatter(
            df_filt, x='pca_1', y='pca_2',
            color='cluster_nome',
            hover_name='Bairro',
            color_discrete_sequence=COLORS,
            opacity=0.75,
            labels={'pca_1': 'Componente Principal 1', 'pca_2': 'Componente Principal 2'},
        )
        fig_pca.update_traces(
            marker=dict(size=7, line=dict(width=0.5, color='white'))
        )
        fig_pca.update_layout(**PL, height=520)
        st.plotly_chart(fig_pca, use_container_width=True)
    else:
        st.markdown("""
        <div class="info-box">
            ℹ️  Execute o PCA no notebook e salve as colunas <b>pca_1</b> e <b>pca_2</b>
            no CSV para visualizar este gráfico.
        </div>
        """, unsafe_allow_html=True)
