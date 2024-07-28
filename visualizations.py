import streamlit as st
import plotly.graph_objects as go

# Histograma de alunos por ano
def plot_students_per_year(filtered_df):
    df_g = filtered_df[filtered_df['indicador'].str.contains('INDE')]
    df_g = df_g[df_g['value'].notna()]
    df_g = df_g.drop_duplicates(subset=['Ano', 'NOME']).groupby(['Ano']).size().reset_index(name='Qtd Alunos')
    fig = go.Figure()
    fig.update_layout(
        width=150,  # Largura em pixels
        height=200,  # Altura em pixels
    )

    # Adiciona os traços do gráfico
    fig.add_trace(go.Bar(x=df_g['Ano'], y=df_g['Qtd Alunos'], name='Quantidade de Alunos', marker_color='midnightblue'))
    fig.update_xaxes(type='category')  # Garantindo que o eixo x seja categórico

    return fig, df_g

#def plot_students_per_year(filtered_df):