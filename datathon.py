import streamlit as st
import requests
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
# from prophet import Prophet  # Descomente se for usar o Prophet
import openpyxl

st.set_page_config(layout='wide')

## Carregar dados
df = pd.read_csv("PEDE_PASSOS_DATASET_FIAP.csv", sep=';')

## Função de filtragem de colunas
def filter_columns(df, filters: list):
    selected_columns = [True] * len(df.columns)  # Inicializa todas as colunas como True
    for index, column in enumerate(df.columns):
        if any(filter in column for filter in filters):
            selected_columns[index] = False
    return df[df.columns[selected_columns]]

## Função de limpeza do dataset
def cleaning_dataset(df):
    _df = df.dropna(subset=df.columns.difference(['NOME']), how='all')  # Remove linhas com todas as colunas NaN, exceto 'NOME'
    _df = _df[~_df.isna().all(axis=1)]  # Remove linhas com apenas NaN
    return _df

## Função para converter colunas para float64 com duas casas decimais
def convert_to_float64_with_two_decimal_places(df, columns):
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').round(2)
    return df

## Tabelas filtradas
df_2020 = filter_columns(df, ['2021', '2022'])
df_2021 = filter_columns(df, ['2020', '2022'])
df_2022 = filter_columns(df, ['2020', '2021'])

df_melted = df.melt(id_vars=df.columns[~df.columns.str.contains('2020|2021|2022')],
                    value_vars=df.columns[df.columns.str.contains('2020|2021|2022')],
                    var_name='indicador',
                    value_name='value')
df_melted['Ano'] = df_melted['indicador'].apply(lambda x: int(x[-4:]))
df_melted['indicador2'] = df_melted['indicador'].apply(lambda x: str(x[:-5]))

## Tabelas filtradas e limpeza do dataset
df = cleaning_dataset(df)
df_2020 = filter_columns(df, ['2021', '2022'])
df_2021 = filter_columns(df, ['2020', '2022'])
df_2022 = filter_columns(df, ['2020', '2021'])

## Função para converter colunas para float64 com duas casas decimais
def convert_to_float64_with_two_decimal_places(df, columns):
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').round(2)
    return df

## Sidebar com filtros, se não estiver na aba "Power BI"
selected_tab = st.sidebar.radio('Escolha uma aba', ['Visão Geral', 'Power BI'])
if selected_tab == 'Visão Geral':
    with st.sidebar:
        min_year, max_year = st.slider(
            'Select the range of years',
            min_value=int(df_melted['Ano'].min()),
            max_value=int(df_melted['Ano'].max()),
            value=(int(df_melted['Ano'].min()), int(df_melted['Ano'].max()))
        )

filtered_df = df_melted[(df_melted['Ano'] >= min_year) & (df_melted['Ano'] <= max_year)]
df_g = filtered_df[filtered_df['indicador'].str.contains('INDE')]
df_g = df_g[df_g['value'].notna()]
df_g = df_g.drop_duplicates(subset=['Ano', 'NOME']).groupby(['Ano']).size().reset_index(name='Qtd Alunos')

## Gráficos
fig = go.Figure()
fig.update_layout(
    width=800,  # Largura em pixels
    height=500,  # Altura em pixels
)

fig.add_trace(go.Bar(x=df_g['Ano'], y=df_g['Qtd Alunos'], name='Quantidade de Alunos', marker_color='midnightblue'))
fig.update_xaxes(type='category')  # Garantindo que o eixo x seja categórico

## Visualização no Streamlit
st.title('PASSOS MÁGICOS')

if selected_tab == 'Visão Geral':
    coluna1, coluna2, coluna3, coluna4, coluna5 = st.columns(5)
    
    # Ajuste as linhas abaixo de acordo com a disponibilidade dos dados
    # with coluna1:
    #     st.metric('Máximo', formata_numero(df0['Brent (F0B)'].max(), ''))
    # with coluna2:
    #     st.metric('Mínimo', formata_numero(df0['Brent (F0B)'].min(), ''))
    # with coluna3:
    #     st.metric('Média', formata_numero(df0['Brent (F0B)'].mean(), ''))
    # with coluna4:
    #     st.metric('', '_')
    #     fig_consumo_fontes_energia = plotagem(dados)
    #     st.plotly_chart(fig_consumo_fontes_energia)
    
    st.plotly_chart(fig)
    st.table(df_g)
elif selected_tab == 'Power BI':
    power_bi_report_url = "https://app.powerbi.com/view?r=eyJrIjoiM2Q1YWUzMjMtZjNmNC00ZGY4LWI3ZWUtYmY4N2FhNjc0M2Q3IiwidCI6ImNhZTdkMDYxLTA4ZjMtNDBkZC04MGMzLTNjMGI4ODg5MjI0YSIsImMiOjh9"

    st.title("Relatório Power BI no Streamlit")
    st.markdown("Este é um relatório do Power BI incorporado no Streamlit.")

    # Incorporando o relatório do Power BI usando um iframe
    st.components.v1.iframe(power_bi_report_url, width=800, height=600, scrolling=True)