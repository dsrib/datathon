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
#from prophet import Prophet  # Descomente se for usar o Prophet
import openpyxl
from openai import OpenAI, error

# Defina a chave da API do OpenAI diretamente ou use st.secrets
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "sua-chave-de-api-aqui")

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

## Sidebar com filtros
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

# Adiciona os traços do gráfico
fig.add_trace(go.Bar(x=df_g['Ano'], y=df_g['Qtd Alunos'], name='Quantidade de Alunos', marker_color='midnightblue'))
fig.update_xaxes(type='category')  # Garantindo que o eixo x seja categórico

## Visualização no Streamlit
st.title('PASSOS MÁGICOS')
aba1, aba2 = st.tabs(['Visão Geral','Relatório Geral dos Alunos'])

with aba1:
    coluna1, coluna2, coluna3, coluna4, coluna5 = st.columns(5)
    
    # Set OpenAI API key from Streamlit secrets
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        try:
            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = "".join(chunk["choices"][0]["delta"]["content"] for chunk in stream)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        except error.AuthenticationError:
            st.error("Erro de autenticação. Verifique sua chave de API.")
        except error.APIError as e:
            st.error(f"Erro na API: {str(e)}")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {str(e)}")

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
    # st.plotly_chart(fig)

st.table(df_g)

with aba2:
    # URL do relatório do Power BI
    power_bi_report_url = "https://app.powerbi.com/view?r=eyJrIjoiM2Q1YWUzMjMtZjNmNC00ZGY4LWI3ZWUtYmY4N2FhNjc0M2Q3IiwidCI6ImNhZTdkMDYxLTA4ZjMtNDBkZC04MGMzLTNjMGI4ODg5MjI0YSIsImMiOjh9"

    st.title("Relatório de Desempenho dos Alunos da Passos Mágicos")
    st.markdown("Este é um tem por objetivo resumir os principais indicadores acadêmicos dos alunos da Passos Mágicos")

    # Incorporando o relatório do Power BI usando um iframe
    st.components.v1.iframe(power_bi_report_url, width=800, height=600, scrolling=True)
