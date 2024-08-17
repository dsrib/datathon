import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
# Histograma de alunos por ano
def plot_students_per_year(filtered_df):
    df_g = filtered_df[filtered_df['indicador'].str.contains('INDE')]
    df_g = df_g[df_g['value'].notna()]
    df_g = df_g.drop_duplicates(subset=['Ano', 'NOME']).groupby(['Ano']).size().reset_index(name='Qtd Alunos')
    fig = go.Figure()
    # Adiciona os traços do gráfico
        # Adiciona os traços do gráfico com rótulos
    fig.add_trace(go.Bar(
        x=df_g['Ano'],
        y=df_g['Qtd Alunos'],
        name='Quantidade de Alunos',
        marker_color='midnightblue',
        text=df_g['Qtd Alunos'],  # Adiciona os rótulos nas barras
        textposition='auto'  # Posições automáticas dos rótulos
    ))
    fig.update_xaxes(type='category')  # Garantindo que o eixo x seja categórico
    # Atualizar o layout para incluir uma borda
    fig.update_layout(
        width=250,  # Largura em pixels
        height=230,  # Altura em pixels
        #margin=dict(l=40, r=40, t=40, b=40),  # Margens para simular a borda
        #paper_bgcolor='white',  # Cor de fundo do papel
        #plot_bgcolor='white',  # Cor de fundo do gráfico
        #shapes=[
        #    dict(
        #        type='rect',
        #        xref='paper', yref='paper',
        #        x0=0, y0=0,
        #        x1=1, y1=1,
        #        line=dict(
        #            color='black',  # Cor da borda
        #            width=2,  # Largura da borda
        #        ),
        #        layer='below'  # Coloca a borda abaixo dos traços do gráfico
        #    )
        #]
    )
    return fig, df_g


def scatter_plot(df, varx, vary, legend, width, height):
    if df.empty:
        fig = px.scatter()  # Cria um gráfico vazio
        fig.update_layout(
            title="Nenhum dado disponível",
            xaxis_title=varx,
            yaxis_title=vary,
            width=width,
            height=height,
            xaxis=dict(range=[0, 1]),  # Define uma faixa padrão para o eixo X
            yaxis=dict(range=[0, 1]),  # Define uma faixa padrão para o eixo Y
        )
        return fig
    var_x = varx
    var_y = vary
    legenda = legend
    

    #legenda
    df_melted=df
    df_scatter = df_melted[df_melted['indicador'].str.startswith(legenda)].drop(columns=['indicador', 'indicador2'])
    df_scatter.rename(columns={"value" : legenda}, inplace=True)
    
    #Eixo Y
    df_y = df_melted[df_melted['indicador'].str.startswith(var_y)].drop(columns=['indicador', 'indicador2'])
    df_y['value'] = pd.to_numeric(df_y['value'], errors='coerce')
    df_y.rename(columns={"value" : var_y}, inplace=True)
    
    #Eixo X
    df_x = df_melted[df_melted['indicador'].str.startswith(var_x)].drop(columns=['indicador', 'indicador2'])
    df_x['value'] = pd.to_numeric(df_x['value'], errors='coerce')
    df_x.rename(columns={"value" : var_x}, inplace=True)
    
    df_final = df_scatter.merge(df_x, on=['NOME', 'Ano'], how='left').merge(df_y, on=['NOME', 'Ano'], how='left')

        # Verifica se as colunas x e y estão vazias ou contêm apenas NaN
    if df_final[varx].dropna().empty or df_final[vary].dropna().empty:
        fig = px.scatter()  # Cria um gráfico vazio
        fig.update_layout(
            title="Dados insuficientes para plotar",
            xaxis_title=varx,
            yaxis_title=vary,
            width=width,
            height=height,
            xaxis=dict(range=[0, 1]),
            yaxis=dict(range=[0, 1]),
        )
        return fig
    
        # Substitui NaN por 0 para evitar erros ao calcular o mínimo e máximo
    df_final[varx].fillna(0, inplace=True)
    df_final[vary].fillna(0, inplace=True)

    fig = px.scatter(df_final, x=var_x, y=var_y, animation_frame="Ano", # Changed 'value' to 'value_x'
                 color=legenda,
                 hover_data=["Ano"])
    # Configure axes and title
    fig.update_xaxes(range=[min(df_final[var_x]), max(df_final[var_x]*1.2)], title=var_x)
    fig.update_yaxes(range=[min(df_final[var_y]), max(df_final[var_y])*1.2], title=var_y,  nticks=10)
    fig.update_layout(title="Dispersão de " + var_y + " vs " + var_x, xaxis_title=var_x, yaxis_title=var_y)
    fig.update_layout(
        width=width,  # Largura em pixels
        height=height
        )
    

    return fig
#def plot_students_per_year(filtered_df):



# Função para retornar o gráfico
def line_chart_column():
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

    # Criando uma figura com dois eixos Y
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    # Adicionando a primeira linha com o primeiro eixo Y (%Populacao)
    fig2.add_trace(
        go.Bar(x=df2['Ano'], y=df2['%Populacao']),
        secondary_y=False
    )

    # Adicionando a segunda linha com o segundo eixo Y (Populacao)
    # fig2.add_trace(
    #     go.Bar(x=df2['Ano'], y=df2['Populacao'], name='Populacao'),
    #     secondary_y=True
    # )

    # Configurando o layout do gráfico
    fig2.update_layout(
        title={
            'text': 'Alunos/População (%)',
            'font': {
                'size': 11,  # Tamanho da fonte do título
                'color': 'gray',
                'family': 'Arial',
                'weight': 'normal'
            }
        },
        #xaxis_title='Ano',
        height=190,
        width=280,
        yaxis=dict(
        showticklabels=False  # Oculta os rótulos dos ticks no eixo Y
        ),
        yaxis_autorange=True
    )

    # Adicionando rótulos de dados somente ao gráfico de barras
    # fig2.update_traces(
    #     selector=dict(type='bar'), 
    #     texttemplate='%{y:.2f}', 
    #     textposition='top center'
    # )

    #fig2.update_yaxes(title_text='%Populacao', secondary_y=False)
    #fig2.update_yaxes(title_text='Populacao', secondary_y=True)
    return fig2

def plot_piramide_etaria(piramide_etaria):
    
    #Tratamento dos dados para o gráfico
    piramide_etaria.drop(['Município', 'Sigla UF', 'Código do Município', 'codMun'], axis=1, inplace=True)
    pop_list=['População feminina(pessoas)', 'População masculina(pessoas)']
    piramide_etaria['População por idade']=piramide_etaria[pop_list].sum(axis=1)
    pop_total = piramide_etaria['População por idade'].sum()
    piramide_etaria['Percentual'] = (piramide_etaria['População por idade'] / pop_total * 100)
    piramide2 = piramide_etaria.set_index(['Grupo de idade']).T
    idade_escolar = ['5 a 9 anos', '10 a 14 anos', '15 a 19 anos', '20 a 24 anos']
    pop_escolar = piramide2[idade_escolar]
    total_pop_escolar = pop_escolar.loc['População por idade'].sum()
    pop_escolar_ordenada = pop_escolar.sort_values(by='População por idade', axis=1)

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    # Plotando a pirâmide etária de Embu-Guaçu
    axes[0].barh(piramide_etaria['Grupo de idade'], piramide_etaria['População por idade'], color='skyblue')
    axes[0].set_title('Pirâmide Etária de Embu-Guaçu', fontsize=16)
    axes[0].set_xlabel('População', fontsize=14)
    axes[0].set_ylabel('Grupo de Idade', fontsize=14)
    axes[0].tick_params(axis='both', labelsize=12)

    for i, v in enumerate(piramide_etaria['Percentual']):
        bar_width = piramide_etaria['População por idade'][i]
        axes[0].text(bar_width / 2, i, f'{v:.1f}%', va='center', ha='center', color='darkblue', fontsize=12)

    # Plotando a pirâmide etária da população em idade escolar
    axes[1].barh(pop_escolar_ordenada.columns, pop_escolar_ordenada.loc['População por idade'], color='coral')
    axes[1].set_title('Pirâmide Etária da População em Idade Escolar de Embu-Guaçu', fontsize=16)
    axes[1].set_xlabel('População', fontsize=14)
    axes[1].set_ylabel('Grupo de Idade', fontsize=14)
    axes[1].tick_params(axis='both', labelsize=12)

    for i, v in enumerate(pop_escolar_ordenada.loc['População por idade']):
        percentual_escolar = v / total_pop_escolar * 100
        bar_width = pop_escolar_ordenada.loc['População por idade'][i]
        axes[1].text(bar_width / 2, i, f'{percentual_escolar:.1f}%', va='center', ha='center', color='saddlebrown', fontsize=12)

    # Exiba o gráfico
    st.pyplot(fig)
