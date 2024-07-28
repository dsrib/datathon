import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from statsforecast import StatsForecast
from statsforecast.models import Naive, SeasonalNaive, SeasonalWindowAverage
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error
from statsmodels.tsa.seasonal import seasonal_decompose
import openpyxl
import functions
# Defina a chave da API do OpenAI diretamente ou use st.secrets
#OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "sua-chave-de-api-aqui")

st.set_page_config(layout='wide')

# Carregar dados
df = pd.read_csv("PEDE_PASSOS_DATASET_FIAP.csv", sep=';')

# Tabelas filtradas
df_2020 = functions.filter_columns(df, ['2021', '2022'])
df_2021 = functions.filter_columns(df, ['2020', '2022'])
df_2022 = functions.filter_columns(df, ['2020', '2021'])

df_melted = df.melt(id_vars=df.columns[~df.columns.str.contains('2020|2021|2022')],
                    value_vars=df.columns[df.columns.str.contains('2020|2021|2022')],
                    var_name='indicador',
                    value_name='value')
df_melted['Ano'] = df_melted['indicador'].apply(lambda x: int(x[-4:]))
df_melted['indicador2'] = df_melted['indicador'].apply(lambda x: str(x[:-5]))

# Visualização no Streamlit
st.title('PASSOS MÁGICOS')
tabs = st.tabs(['Visão Geral', 'Relatório Geral dos Alunos'])

with tabs[0]:
    st.subheader("O que é a Passos Mágicos?")
    st.markdown("A Passos Mágicos é uma instituição dedicada a promover o desenvolvimento acadêmico e pessoal dos alunos através de programas educativos e sociais.")
    
    # Sidebar com filtros (visível apenas na aba "Visão Geral")
    st.sidebar.header("Filtros de Ano")
    min_year, max_year = st.sidebar.slider(
        'Selecione o intervalo de anos',
        min_value=int(df_melted['Ano'].min()),
        max_value=int(df_melted['Ano'].max()),
        value=(int(df_melted['Ano'].min()), int(df_melted['Ano'].max()))
    )

    filtered_df = df_melted[(df_melted['Ano'] >= min_year) & (df_melted['Ano'] <= max_year)]
    df_g = filtered_df[filtered_df['indicador'].str.contains('INDE')]
    df_g = df_g[df_g['value'].notna()]
    df_g = df_g.drop_duplicates(subset=['Ano', 'NOME']).groupby(['Ano']).size().reset_index(name='Qtd Alunos')

    # Gráficos
    fig = go.Figure()
    fig.update_layout(
        width=800,  # Largura em pixels
        height=500,  # Altura em pixels
    )

    # Adiciona os traços do gráfico
    fig.add_trace(go.Bar(x=df_g['Ano'], y=df_g['Qtd Alunos'], name='Quantidade de Alunos', marker_color='midnightblue'))
    fig.update_xaxes(type='category')  # Garantindo que o eixo x seja categórico

    st.plotly_chart(fig)
    st.table(df_g)

with tabs[1]:
    st.title("Relatório de Desempenho dos Alunos da Passos Mágicos")
    st.markdown("Este relatório tem por objetivo resumir os principais indicadores acadêmicos dos alunos da Passos Mágicos.")

    # URL do relatório do Power BI
    power_bi_report_url = "https://app.powerbi.com/view?r=eyJrIjoiM2Q1YWUzMjMtZjNmNC00ZGY4LWI3ZWUtYmY4N2FhNjc0M2Q3IiwidCI6ImNhZTdkMDYxLTA4ZjMtNDBkZC04MGMzLTNjMGI4ODg5MjI0YSIsImMiOjh9"
    # Incorporando o relatório do Power BI usando um iframe
    st.components.v1.iframe(power_bi_report_url, width=1000, height=600, scrolling=True)

