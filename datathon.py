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
from plotly.subplots import make_subplots
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
    coluna1, coluna2, coluna3, coluna4, coluna5, coluna6, coluna7, coluna8, coluna9 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1])
     # Sidebar com filtros (visível apenas na aba "Visão Geral")
 
    alunos_2020 = 727
    alunos_2021 = 684
    alunos_2022 = 862
    qtd_alunos = df_melted['NOME'].nunique()

    # Calcular a variação percentual entre anos
    delta_2020 = alunos_2020 - alunos_2020
    delta_2021 = alunos_2021 - alunos_2020
    delta_2022 = alunos_2022 - alunos_2021

    with coluna1:
        st.write("")
        st.write("")
        st.metric(label="Pessoas Impactadas", value=qtd_alunos*4, delta=0)
    with coluna2:
        st.write("")
        st.write("")
        st.metric(label="Qtd Alunos", value=qtd_alunos, delta=0)
    with coluna3:
        st.write("")
        st.write("")
        st.metric(label="Alunos 2020", value=alunos_2020, delta=delta_2020)
    with coluna4:
        st.write("")
        st.write("")
        st.metric(label="Alunos 2021", value=alunos_2021, delta=delta_2021)
    with coluna5:
        st.write("")
        st.write("")
        st.metric(label="Alunos 2022", value=alunos_2022, delta=delta_2022)
    with coluna6:
        st.write("")
        st.write("")
        st.metric(label="Bolsistas 2023", value=98, delta=0)
    with coluna7:
        st.write("")
        st.write("")
        st.metric(label="Universitários 2023", value=103, delta=0)
    with coluna8:
        st.write("")
        st.write("")
        st.metric(label="Graduados 2023", value=41, delta=0)
    with coluna9:
        st.plotly_chart(visualizations.line_chart_column(), use_container_width=True)  

    #st.table(df_g)
    
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

    st.header("Gráficos Dados Históricos:")    

with tabs[0]:
        col1, col2 = st.columns([1, 1])
        with col1:
            data = {
                'Ano': ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'],
                'Alunos': [70, 300, 550, 812, 841, 824, 970, 1100],
                'Bolsistas': [26, 35, 80, 106, 112, 133, 112, 100],
                'Universitários': [0, 0, 1, 2, 26, 51, 71, 94]
            }
            df1 = pd.DataFrame(data)

            # Criando o gráfico de linha 1
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df1['Ano'], y=df1['Alunos'], mode='lines+markers', name='Alunos'))
            fig.add_trace(go.Scatter(x=df1['Ano'], y=df1['Bolsistas'], mode='lines+markers', name='Bolsistas'))
            fig.add_trace(go.Scatter(x=df1['Ano'], y=df1['Universitários'], mode='lines+markers', name='Universitários'))

            fig.update_layout(
                title='Alunos X Bolsistas X Universitários',
                xaxis_title='Ano',
                yaxis_title='Quantidade',
                height=400,
                width=500
            )

            # Display with Streamlit
            st.plotly_chart(fig)                                    

        with col2:
            # Dados para gráfico de linha 2
            data_2 = {
                'Ano': ['2016', '2017', '2018', '2019', '2020', '2021', '2022'],
                'Alunos': [70, 300, 550, 812, 841, 824, 970],
                'Bolsistas': [26, 35, 80, 106, 112, 133, 112],
                'Universitários': [0, 0, 1, 2, 26, 51, 71],
                'Populacao': [67788, 68270, 68750, 69385, 70083, 70402, 66970],
                '%Populacao': [0.10, 0.44, 0.80, 1.17, 1.20, 1.17, 1.45]
            }
            df2 = pd.DataFrame(data_2)

            # Criando o gráfico de linha 2
            # Criando uma figura com dois eixos Y
            fig2 = make_subplots(specs=[[{"secondary_y": True}]])

            # Adicionando a primeira linha com o primeiro eixo Y (%Populacao)
            fig2.add_trace(
                go.Scatter(x=df2['Ano'], y=df2['%Populacao'], mode='lines+markers', name='%Populacao'),
                secondary_y=False
            )

            # Adicionando a segunda linha com o segundo eixo Y (Populacao)
            fig2.add_trace(
                go.Scatter(x=df2['Ano'], y=df2['Populacao'], mode='lines+markers', name='Populacao'),
                secondary_y=True
            )
                    

            fig2.update_layout(
                title='Quantidade Alunos ONG X População Embu-Guaçu',
                xaxis_title='Ano',
                yaxis_title='Quantidade',
                height=400,
                width=500
            )
            fig2.update_yaxes(title_text='%Populacao', secondary_y=False)
            fig2.update_yaxes(title_text='Populacao', secondary_y=True)
            # Exibindo o gráfico com o Streamlit
            st.plotly_chart(fig2)



with tabs[1]:  

    indicador_x = "IDADE_ALUNO"
    indicador_y = "IDA"
    legenda = "INSTITUICAO"  
# Configuração do intervalo de anos lado a lado
    col1, col2 = st.columns([1, 3])

    # Garantindo que os valores mínimos e máximos sejam inteiros
    min_ano = int(df_melted['Ano'].min())
    max_ano = int(df_melted['Ano'].max())

    with col1:
        min_year, max_year = st.select_slider(
            'Selecione o intervalo de anos',
            options=list(range(min_ano, max_ano)),  # Garante uma lista de anos inteiros
            value=(min_ano, max_ano)  # Valor inicial como o intervalo completo
        )

    with col2:
        #st.markdown("### Indicadores")

        # Configuração das select boxes lado a lado
        col3, col4, col5, col6 = st.columns(4)

        with col3:
            df_melted_numeric = df_melted[df_melted['value'].apply(lambda x: str(x).isnumeric())]
            indicadorx = df_melted_numeric['indicador2'].unique()
            indicador_x = st.selectbox(
                'Indicador para eixo x',
                options=indicadorx,
                index=list(indicadorx).index("INDE") if "INDE" in indicadorx else 0
            )

        with col4:
            df_melted_numeric = df_melted[df_melted['value'].apply(lambda x: str(x).isnumeric())]
            indicadory = df_melted_numeric['indicador2'].unique()
            indicador_y = st.selectbox(
                'Indicador para eixo y',
                options=indicadory,
                index=list(indicadory).index("IDA") if "IDA" in indicadory else 0
            )

    st.title("Relatório de Desempenho dos Alunos da Passos Mágicos")
    st.markdown("Este relatório tem por objetivo resumir os principais indicadores acadêmicos dos alunos da Passos Mágicos.")

    # Usando st.columns para layout da seção do gráfico
    col1 = st.columns(1)

    with col1[0]:

            #st.write("Indicadores")
            filtered_df = df_melted[(df_melted['Ano'] >= min_year) & (df_melted['Ano'] <= max_year)]
            fig2 = visualizations.scatter_plot(filtered_df, indicador_x, indicador_y, legenda, width=1400, height=500)
            st.plotly_chart(fig2, use_container_width=False, config={'responsive': True})
            # URL do relatório do Power BI
            power_bi_report_url = "https://app.powerbi.com/view?r=eyJrIjoiM2Q1YWUzMjMtZjNmNC00ZGY4LWI3ZWUtYmY4N2FhNjc0M2Q3IiwidCI6ImNhZTdkMDYxLTA4ZjMtNDBkZC04MGMzLTNjMGI4ODg5MjI0YSIsImMiOjh9"
            # Incorporando o relatório do Power BI usando um iframe
            st.components.v1.iframe(power_bi_report_url, width=1400, height=800, scrolling=True)
            # Dados para gráfico de linha 1
        

