import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
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

    fig = px.scatter(df_final, x=var_x, y=var_y, animation_frame="Ano", # Changed 'value' to 'value_x'
                 color=legenda,
                 hover_data=["Ano"])
    # Configure axes and title
    fig.update_xaxes(range=[min(df_final[var_x]), max(df_final[var_x])], title=var_x)
    fig.update_yaxes(range=[min(df_final[var_y]), max(df_final[var_y])], title=var_y)
    fig.update_layout(title="Dispersão de " + var_y + " vs " + var_x, xaxis_title=var_x, yaxis_title=var_y)
    fig.update_layout(
        width=width,  # Largura em pixels
        height=height)

    return fig
#def plot_students_per_year(filtered_df):

