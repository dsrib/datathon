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
#from prophet import Prophet  # Descomente se for usar o Prophet
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

## Sidebar com filtros
with st.sidebar:
    #data_inicial_padrao = df_melted['Ano'].min()
    #data_final_padrao = df_melted['Ano'].max()

    # data_inicial = st.date_input("Data Inicial", value=data_inicial_padrao, min_value=df_melted['Data'].min())
    # data_final = st.date_input("Data Final", value=data_final_padrao, max_value=df_melted['Data'].max())

    show_shanghai_index = st.checkbox("Bolsa de Xangai")

## Gráficos
fig = go.Figure()
fig.update_layout(
    width=800,  # Largura em pixels
    height=500,  # Altura em pixels
)

# Descomente e ajuste as seguintes linhas se os dados estiverem disponíveis e formatados corretamente
# fig.add_trace(go.Scatter(x=df0['Data'], y=df0['Brent (F0B)'], mode='lines', name='Preço do Petróleo', line=dict(color='midnightblue')))
# if show_shanghai_index:
#     fig.add_trace(go.Scatter(x=dfs['Data'], y=dfs['Último'], mode='markers', name='Índice de Xangai', marker=dict(color='green', size=3), yaxis='y2'))

# fig.update_layout(title='Preço do Petróleo', xaxis_title='Data', legend=dict(x=0, y=1.1))
# if show_shanghai_index:
#     fig.update_layout(yaxis=dict(title='Preço do Petróleo (US$/barril)', color='midnightblue'),
#                       yaxis2=dict(title='Índice de Xangai', color='green', overlaying='y', side='right'))

# fig.update_xaxes(showgrid=True, zeroline=True, zerolinewidth=2, zerolinecolor='black')
# fig.update_yaxes(showgrid=True, zeroline=True, zerolinewidth=2, zerolinecolor='black')

## Visualização no Streamlit
st.title('PASSOS MÁGICOS')
aba1, = st.tabs(['Visão Geral'])

with aba1:
    coluna1, coluna2, coluna3, coluna4, coluna5 = st.columns(5)

    # Ajuste as linhas abaixo de acordo com a disponibilidade dos dados
    # with coluna1:
    #     st.metric('Máximo', formata_numero(df0['Brent (F0B)'].max(), ''))
    #     st.plotly_chart(fig)
    # with coluna2:
    #     st.metric('Mínimo', formata_numero(df0['Brent (F0B)'].min(), ''))
    # with coluna3:
    #     st.metric('Média', formata_numero(df0['Brent (F0B)'].mean(), ''))
    # with coluna4:
    #     st.metric('', '_')
    #     fig_consumo_fontes_energia = plotagem(dados)
    #     st.plotly_chart(fig_consumo_fontes_energia)
