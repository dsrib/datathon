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
tabs = st.tabs(['Visão Geral', 'Relatório Geral dos Alunos', 'Indicadores de Sucesso'])

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

    with coluna2:
        st.write("Indicadores")
        filtered_df = df_melted[(df_melted['Ano'] >= min_year) & (df_melted['Ano'] <= max_year)]
        fig2 = visualizations.scatter_plot(filtered_df, "INDE", "IAA", "INSTITUICAO")
        # Criando um container para o gráfico
    with st.container():
        fig_width = 1000
        
        # Aplicando CSS para permitir que o gráfico extrapole a largura da coluna
        st.markdown(
            f"""
            <style>
                .container {{
                    width: 100%;
                    overflow-x: auto;
                }}
                .plot-container {{
                    width: {fig_width}px;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Exibindo o gráfico no container com estilo aplicado
        st.plotly_chart(fig2, use_container_width=False, config={'responsive': True})
        
    st.title("O que é a Passos Mágicos?")
    st.markdown(descricao)
    st.title("O que fazemos?") 
    st.markdown("A ONG se dedica em oferecer uma educação de qualidade, suporte psicológico e a ampliar a visão de mundo de cada aluno impactado. Disponibilizamos aulas de alfabetização, língua portuguesa e matemática para crianças e adolescentes. Os alunos são divididos conforme o nível de conhecimento, determinado por meio de uma prova de sondagem realizada ao ingressarem no Passos Mágicos. Eles são então colocados em turmas que vão desde a alfabetização até o nível 8, sendo:")
    st.header("Fase de Alfabetização:")
    st.markdown("Alunos que estão em fase de alfabetização ou enfrentam dificuldades na leitura e na escrita.")
    st.header("Fase 1 e 2:")
    st.markdown("Focadas no conteúdo do ensino fundamental 1, com uma abordagem que detalha progressivamente o material à medida que os alunos avançam de um nível para o outro.")
    st.header("Fase 3 e 4:")
    st.markdown("Focadas no conteúdo do ensino fundamental 2, com uma abordagem que explora o material com mais detalhes à medida que os alunos progridem de um nível para o outro.")
    st.header("Fase 5 e 6:")
    st.markdown("Focadas em conteúdos voltados para jovens e adolescentes do ensino médio, visando um aprofundamento no nível de conhecimento.")
    st.header("Fase 7 e 8:")
    st.markdown("Destinadas a jovens alunos em fase de conclusão do ensino médio e vestibulandos, com ênfase na aceleração do conhecimento.")            
    st.title("Programas Especiais:") 
    st.header("Educacionais:")
    st.markdown("'Programa Vem Ser', projeto criado a partir da parceria entre a Associação Passos Mágicos e a Rede Decisão, que cedeu algumas de suas plataformas de ensino para que fossem utilizadas com nossos alunos do ensino médio e vestibulando.")
    st.header("Assistência Psicológica:")
    st.markdown("A Associação Passos Mágicos acredita que, para otimizar o desempenho dos alunos, é essencial não apenas o conhecimento acadêmico, mas também o suporte emocional. É fundamental abordar e resolver os problemas que podem dificultar o aprendizado. Para isso, desenvolvemos um trabalho com diversas dinâmicas, onde nossas psicólogas atuam tanto no comportamento individual quanto no coletivo dos jovens.")
    st.header("Atividades Culturais:")
    st.markdown("Na Associação Passos Mágicos, acreditamos que integrar os alunos a diversos elementos culturais enriquece seu aprendizado e formação. Por isso, além das aulas, organizamos atividades semanais em museus, parques, eventos e outros locais que estimulam a curiosidade dos jovens.")
    st.title("Eventos e Ações Socias:")
    st.markdown("Anualmente, são promovidas campanhas de arrecadação com a finalidade de presentear as crianças e adolescentes do projeto Passos Mágicos. Sendo elas:")
    st.header("Materiais Escolares:")
    st.markdown("Campanha de coleta de doações de materiais para estudantes bolsistas e todos os demais alunos.")  
    st.header("Páscoa Mágica:")
    st.markdown("Coleta de ovos de Páscoa, barras e caixas de chocolate para distribuição aos alunos.")
    st.header("Dia das Crianças:")
    st.markdown("Coleta de brinquedos para os alunos.")            
    st.header("Campanha do Agasalho:")
    st.markdown("Arrecadação de roupas de inverno para os alunos e suas famílias.")            
    st.header("Natal Mágico:")
    st.markdown("São entregues presentes cuidadosamente escolhidos para os alunos, e as sacolas, montadas a partir das doações, são distribuídas aos familiares das crianças.")            
    st.header("Confraternização de Encerramento:")
    st.markdown("Todo ano, é realizado um evento de confraternização para celebrar as conquistas e realizações do ano que passou.")

    
    
    #st.table(df_g)

with tabs[1]:
    st.title("Relatório de Desempenho dos Alunos da Passos Mágicos")
    st.markdown("Este relatório tem por objetivo resumir os principais indicadores acadêmicos dos alunos da Passos Mágicos.")

    # URL do relatório do Power BI
    power_bi_report_url = "https://app.powerbi.com/view?r=eyJrIjoiM2Q1YWUzMjMtZjNmNC00ZGY4LWI3ZWUtYmY4N2FhNjc0M2Q3IiwidCI6ImNhZTdkMDYxLTA4ZjMtNDBkZC04MGMzLTNjMGI4ODg5MjI0YSIsImMiOjh9"
    # Incorporando o relatório do Power BI usando um iframe
    st.components.v1.iframe(power_bi_report_url, width=800, height=600, scrolling=True)


with tabs[2]:
    st.title("Indicadores de Impacto no ano de 2023:")
    col1,col2,col3,col4,col5 =st.columns(5)
    with col1:
       st.markdown("'4400'Pessoas impactadas (Considerando a média de 4 familiares por aluno)")
    with col2:
      st.markdown("'1100'Alunos no programa de Aceleração do Conhecimento") 
    with col3:
      st.markdown("'98'Bolsistas em instituições de ensino particular")  
    with col4:
      st.markdown("'103'Universitários em instituições de ensino superior")
    with col5:
      st.markdown("'41'Alunos formados em instituições de ensino superior")  

    
    #Dados para gráfico de linha
    data = {
          'Ano' : ['2016', '2017', '2018', '2019','2020','2021','2022','2023'],
          'Alunos' : [70, 300, 550, 812, 841, 824, 970, 1100],
          'Bolsistas' : [26,35,80,106,112,133,112,100 ],
          'Universitários' : [0,0,1,2,26,51,71,94]}
    df = pd.DataFrame(data)
    # Criando o gráfico de linha
    plt.figure(figsize=(10, 6))
    plt.plot(df['Ano'], df['Alunos'], marker='o', label='Alunos')
    plt.plot(df['Ano'], df['Bolsistas'], marker='o', label='Bolsistas')
    plt.plot(df['Ano'], df['Universitários'], marker='o', label='Universitários')
    plt.title('Alunos X Bolsistas X Universitários')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade')
    plt.legend()
    plt.grid(True)
    plt.show()
    # Salvando o gráfico
    plt.savefig('grafico_linha_tempo.png')

    # Exibindo o gráfico com o Streamlit
    st.title('Alunos X Bolsistas X Universitários')
    st.line_chart(df.set_index('Data'))

    # Para exibir a imagem salva do gráfico
    st.image('grafico_linha_tempo.png')
    
