# 📍 GeoMarketing Cluster Analysis

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg.svg)](https://geo-marketing-app-8fqfzqiufoavbfpugtfcpp.streamlit.app/)

## 📖 Sobre o Projeto
Este projeto é uma ferramenta de **Inteligência Geográfica** desenvolvida para segmentar bairros das capitais brasileiras com base em dados demográficos, socioeconômicos e de potencial de consumo. 

O objetivo é fornecer insights estratégicos para expansão de negócios, permitindo identificar áreas com perfis similares de renda, densidade populacional e hábitos de consumo através de **Machine Learning Não Supervisionado**.

---

## 🚀 Funcionalidades
- **Enriquecimento de Dados:** Integração com a API GreatSpaces para coleta de +50 variáveis de mercado por coordenada geográfica.
- **Clusterização K-Means:** Agrupamento estatístico de bairros em perfis distintos (ex: Elite Socioeconômica, Polos de Adensamento Popular).
- **Análise Multidimensional:** Redução de dimensionalidade via **PCA** para visualização da separação dos grupos.
- **Dashboard Interativo:** Mapa de calor e gráficos de radar desenvolvidos em Streamlit para exploração do cliente.

---

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.12
- **Data Wrangling:** Pandas, Numpy
- **Geolocalização:** GeoPy (Nominatim) & Google BigQuery (Base dos Dados)
- **Machine Learning:** Scikit-Learn (K-Means, PCA, StandardScaler)
- **Visualização:** Plotly, Folium
- **Deploy:** Streamlit Cloud

---

## 📊 Metodologia Científica
1. **Coleta de Pontos:** Identificação dos centros geográficos dos 30 bairros mais populosos de cada capital brasileira.
2. **Feature Engineering:** Tratamento de dados brutos da API (conversão de strings monetárias para floats, tratamento de NaNs).
3. **Escalonamento:** Normalização das variáveis para evitar viés de magnitude nas distâncias euclidianas.
4. **Otimização de Hyperparameters:** Aplicação do *Elbow Method* (Método do Cotovelo) para determinar o número ideal de clusters.
5. **Profiling:** Tradução dos centroides dos clusters em personas de mercado.

---

## 💻 Como Rodar Localmente
1. Clone o repositório:
   ```bash
   git clone [https://github.com/seu-usuario/geo-marketing-app.git](https://github.com/seu-usuario/geo-marketing-app.git)
