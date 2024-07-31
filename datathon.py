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
import visualizations
# Defina a chave da API do OpenAI diretamente ou use st.secrets
#OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "sua-chave-de-api-aqui")

st.set_page_config(layout='wide')

# Carregar dados
df = pd.read_csv("PEDE_PASSOS_DATASET_FIAP.csv", sep=';')
# Carregar texto pré-formatado
descricao = functions.load_text('AboutPassos.txt')
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
    coluna1, coluna2, coluna3, coluna4, coluna5 = st.columns(5)
     # Sidebar com filtros (visível apenas na aba "Visão Geral")
    st.sidebar.header("Filtros de Ano")
    min_year, max_year = st.sidebar.slider(
        'Selecione o intervalo de anos',
        min_value=int(df_melted['Ano'].min()),
        max_value=int(df_melted['Ano'].max()),
        value=(int(df_melted['Ano'].min()), int(df_melted['Ano'].max()))
    )
    
    # Adicionar caixa de seleção única na barra lateral
    st.sidebar.header("Indicadores")
    indicadorx = df_melted['indicador2'].unique()  # Supondo que você tem uma coluna 'Ano' no seu DataFrame
    indicador_x = st.sidebar.selectbox(
        'Indicador para eixo y',
        options=indicadorx,
        index=0  # Define o ano inicial selecionado
    )
    # Adicionar caixa de seleção única na barra lateral

    indicadory = df_melted['indicador2'].unique()  # Supondo que você tem uma coluna 'Ano' no seu DataFrame
    indicador_y = st.sidebar.selectbox(
        'Indicador para eixo x',
        options=indicadory,
        index=0  # Define o ano inicial selecionado
    )

    with coluna1:
        st.write("Histograma")
        filtered_df = df_melted[(df_melted['Ano'] >= min_year) & (df_melted['Ano'] <= max_year)]
        fig, df_g = visualizations.plot_students_per_year(filtered_df)
        st.plotly_chart(fig)

    st.subheader("O que é a Passos Mágicos?")
    st.markdown(descricao)
    st.subheader("O que fazemos?") 
    st.markdown("A ONG se dedica em oferecer uma educação de qualidade, suporte psicológico e a ampliar a visão de mundo de cada aluno impactado. Disponibilizamos aulas de alfabetização, língua portuguesa e matemática para crianças e adolescentes. Os alunos são divididos conforme o nível de conhecimento, determinado por meio de uma prova de sondagem realizada ao ingressarem no Passos Mágicos. Eles são então colocados em turmas que vão desde a alfabetização até o nível 8, sendo:") 
    st.subheader("Programas Especiais:") 
    st.markdown{'Educacionais': ['Programa Vem Ser: projeto criado a partir da parceria entre a Associação Passos Mágicos e a Rede Decisão, que cedeu algumas de suas plataformas de ensino para que fossem utilizadas com nossos alunos do ensino médio e vestibulando'],
                'Assistência Psicológica': ['A Associação Passos Mágicos acredita que, para otimizar o desempenho dos alunos, é essencial não apenas o conhecimento acadêmico, mas também o suporte emocional. É fundamental abordar e resolver os problemas que podem dificultar o aprendizado. Para isso, desenvolvemos um trabalho com diversas dinâmicas, onde nossas psicólogas atuam tanto no comportamento individual quanto no coletivo dos jovens.'],
                'Atividades Culturais': ['Na Associação Passos Mágicos, acreditamos que integrar os alunos a diversos elementos culturais enriquece seu aprendizado e formação. Por isso, além das aulas, organizamos atividades semanais em museus, parques, eventos e outros locais que estimulam a curiosidade dos jovens.']}
    st.subheader("Eventos e Ações Socias:")
    st.markdown("Anualmente, são promovidas campanhas de arrecadação com a finalidade de presentear as crianças e adolescentes do projeto Passos Mágicos.") 
    
   


    
    
    #st.table(df_g)

with tabs[1]:
    st.title("Relatório de Desempenho dos Alunos da Passos Mágicos")
    st.markdown("Este relatório tem por objetivo resumir os principais indicadores acadêmicos dos alunos da Passos Mágicos.")

    # URL do relatório do Power BI
    power_bi_report_url = "https://app.powerbi.com/view?r=eyJrIjoiM2Q1YWUzMjMtZjNmNC00ZGY4LWI3ZWUtYmY4N2FhNjc0M2Q3IiwidCI6ImNhZTdkMDYxLTA4ZjMtNDBkZC04MGMzLTNjMGI4ODg5MjI0YSIsImMiOjh9"
    # Incorporando o relatório do Power BI usando um iframe
    st.components.v1.iframe(power_bi_report_url, width=1000, height=600, scrolling=True)

