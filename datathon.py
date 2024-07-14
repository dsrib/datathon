import  streamlit as st
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
#import pickle
from prophet import Prophet
import openpyxl

st.set_page_config(layout= 'wide')

##Tabelas
df = pd.read_csv("PEDE_PASSOS_DATASET_FIAP.csv", sep=';')
pd.DataFrame(df.loc[df['NOME'] == 'ALUNO-2']).transpose().T
df_2020 = filter_columns(df, ['2021', '2022'])
df_2021 = filter_columns(df, ['2020', '2022'])
df_2022 = filter_columns(df, ['2020', '2021'])
df_melted = df.melt(id_vars=df.columns[~df.columns.str.contains('2020|2021|2022')],
                    value_vars=df.columns[df.columns.str.contains('2020|2021|2022')],
                    var_name='indicador',
                    value_name='value')
## Funções
def filter_columns(df, filters: list): # adiciono no array o padrão que existe nas colunas e que não quero que tenha na saída final
  selected_columns = [True] * len(df.columns)  # Inicializa todas as colunas como True
  for index, column in enumerate(df.columns):
    if any(filter in column for filter in filters): selected_columns[index] = False
return df[df.columns[selected_columns]]
 
 def cleaning_dataset(df):
    _df = df.dropna(subset=df.columns.difference(['NOME']), how='all') # executa o dropna para todas as colunas sem visualizar a coluna NOME
    _df = _df[~_df.isna().all(axis=1)] # remove linhas com apenas NaN, se tiver algum dado na linha não remove
 return _df

def convert_to_float64_with_two_decimal_places(df, columns):
  for col in columns:
    # Tentar converter para float e tratar erros
    df[col] = pd.to_numeric(df[col], errors='coerce').round(2)
return df
  
## Modelo de ML Naive

## Filtros

with st.sidebar:
 
    data_inicial_padrao = df['Ano'].min()
    data_final_padrao = df['Ano'].max()

    data_inicial = st.date_input("Data Inicial", value=data_inicial_padrao, min_value=df['Data'].min())
    data_final = st.date_input("Data Final", value=data_final_padrao, max_value=df['Data'].max())

# Create a Streamlit button to toggle visibility of the second line
with st.sidebar:
    show_shanghai_index = st.checkbox("Bolsa de Xangai")

df['ds'] = pd.to_datetime(df['Data'])



df0 = df[(df['Data'] >= data_inicial) & (df['Data'] <= data_final)]
dfs = dfs[(dfs['Data'] >= data_inicial) & (dfs['Data'] <= data_final)]

##Gráficos

# Gráfico do Preço do Barril Brent
fig = go.Figure()
fig.update_layout(
    width=800,  # Largura em pixels
    height=500,  # Altura em pixels
)
# Plot 1: Preço do Petróleo Brent
fig.add_trace(go.Scatter(x=df0['Data'], y=df0['Brent (F0B)'], mode='lines', name='Preço do Petróleo', line=dict(color='midnightblue')))

# Plot 2: Índice de Xangai
#if show_shanghai_index:
    #fig.add_trace(go.Scatter(x=dfs['Data'], y=dfs['Último'], mode='markers', name='Índice de Xangai', marker=dict(color='green', size=3), yaxis='y2'))

# Formatação do layout
#fig.update_layout(title='Preço do Petróleo', xaxis_title='Data', legend=dict(x=0, y=1.1))

# Se o checkbox for marcado, atualize as configurações do eixo y para o Índice de Xangai
#if show_shanghai_index:
    #fig.update_layout(yaxis=dict(title='Preço do Petróleo (US$/barril)', color='midnightblue'),
                      #yaxis2=dict(title='Índice de Xangai', color='green', overlaying='y', side='right'))

#fig.update_xaxes(showgrid=True, zeroline=True, zerolinewidth=2, zerolinecolor='black')
#fig.update_yaxes(showgrid=True, zeroline=True, zerolinewidth=2, zerolinecolor='black')


##Visualização streamlit

st.title('PASSOS MÁGICOS')
aba1,  = st.tabs(['Visão Geral'])

with aba1:
    coluna1, coluna2, coluna3, coluna4, coluna5 = st.columns(5)

    #with coluna1:
        #st.metric('Máximo',formata_numero(df0['Brent (F0B)'].max(),''))
        #st.plotly_chart(fig)
   # with coluna2:
       # st.metric('Mínimo',formata_numero(df0['Brent (F0B)'].min(),''))
    #with coluna3:
      #  st.metric('Média',formata_numero(df0['Brent (F0B)'].mean(),''))
   # with coluna4:
       # st.metric('',' _')
       # fig_consumo_fontes_energia = plotagem(dados)
      #  st.plotly_chart(fig_consumo_fontes_energia)



 
