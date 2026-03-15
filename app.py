import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# Configuração da página
st.set_page_config(page_title="GeoMarketing Cluster Analysis", layout="wide")

# --- CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data():
    # Certifique-se de que o nome do arquivo coincida com o que você salvou no Colab
    df = pd.read_csv("df_final_com_clusters.csv")
    return df

try:
    df = load_data()
except:
    st.error("Arquivo 'df_final_com_clusters.csv' não encontrado. Por favor, suba o arquivo no GitHub.")
    st.stop()

# --- SIDEBAR / FILTROS ---
st.sidebar.header("Filtros de Negócio")
ufs = st.sidebar.multiselect("Estados (UF)", options=sorted(df['UF'].unique()), default=df['UF'].unique())
cidades = st.sidebar.multiselect("Cidades", options=sorted(df[df['UF'].isin(ufs)]['Cidade'].unique()), default=df[df['UF'].isin(ufs)]['Cidade'].unique()[:2])

df_filt = df[(df['UF'].isin(ufs)) & (df['Cidade'].isin(cidades))]

# --- DASHBOARD PRINCIPAL ---
st.title("📍 Segmentação Inteligente de Mercado")
st.markdown(f"Análise baseada em **{len(df_filt)} bairros** nas capitais brasileiras.")

# Métricas de resumo
m1, m2, m3 = st.columns(3)
m1.metric("Média de Renda", f"R$ {df_filt['income'].mean():.2f}")
m2.metric("População Total", f"{df_filt['people'].sum():,.0f}")
m3.metric("Nº de Clusters", df['cluster'].nunique())

tabs = st.tabs(["🗺️ Mapa Geográfico", "📊 Perfil dos Clusters", "🧬 Espaço PCA"])

# TAB 1: MAPA
with tabs[0]:
    st.subheader("Distribuição Espacial por Segmento")
    cores = ['red', 'blue', 'green', 'purple', 'orange', 'darkred']
    
    m = folium.Map(location=[df_filt['Latitude'].mean(), df_filt['Longitude'].mean()], zoom_start=11, tiles='cartodbpositron')
    
    for _, row in df_filt.iterrows():
        color = cores[int(row['cluster']) % len(cores)]
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=8, color=color, fill=True, fill_opacity=0.7,
            popup=f"Bairro: {row['Bairro']}<br>Cluster: {row['cluster_nome']}"
        ).add_to(m)
    
    st_folium(m, width=1300, height=500)

# TAB 2: RADAR CHART (Assinatura do Cluster)
with tabs[1]:
    st.subheader("O que define cada grupo?")
    
    # Seleção de features numéricas para o Radar
    features_radar = ['income', 'people', 'cons_a_total', 'class_a1', 'age_adults', 'density']
    perfil = df.groupby('cluster_nome')[features_radar].mean()
    perfil_norm = (perfil - perfil.min()) / (perfil.max() - perfil.min())

    fig_radar = go.Figure()
    for i in range(len(perfil_norm)):
        fig_radar.add_trace(go.Scatterpolar(
            r=perfil_norm.iloc[i].values,
            theta=features_radar,
            fill='toself',
            name=perfil_norm.index[i]
        ))
    st.plotly_chart(fig_radar, use_container_width=True)

# TAB 3: PCA
with tabs[2]:
    st.subheader("Separação Estatística (2D)")
    # Se você salvou as colunas pca_1 e pca_2 no CSV
    if 'pca_1' in df.columns:
        fig_pca = px.scatter(df_filt, x='pca_1', y='pca_2', color='cluster_nome', 
                             hover_name='Bairro', title="Projeção PCA")
        st.plotly_chart(fig_pca, use_container_width=True)
    else:
        st.info("Execute o PCA no notebook e salve as colunas 'pca_1' e 'pca_2' no CSV para ver este gráfico.")