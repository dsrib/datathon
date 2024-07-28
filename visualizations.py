import streamlit as st
import plotly.graph_objects as go

# Histograma de alunos por ano
def plot_students_per_year(filtered_df):
    df_g = filtered_df[filtered_df['indicador'].str.contains('INDE')]
    df_g = df_g[df_g['value'].notna()]
    df_g = df_g.drop_duplicates(subset=['Ano', 'NOME']).groupby(['Ano']).size().reset_index(name='Qtd Alunos')
    fig = go.Figure()
    # Adiciona os traços do gráfico
    fig.add_trace(go.Bar(x=df_g['Ano'], y=df_g['Qtd Alunos'], name='Quantidade de Alunos', marker_color='midnightblue'))
    fig.update_xaxes(type='category')  # Garantindo que o eixo x seja categórico
    # Atualizar o layout para incluir uma borda
    fig.update_layout(
        width=150,  # Largura em pixels
        height=220,  # Altura em pixels
        margin=dict(l=40, r=40, t=40, b=40),  # Margens para simular a borda
        paper_bgcolor='white',  # Cor de fundo do papel
        plot_bgcolor='white',  # Cor de fundo do gráfico
        shapes=[
            dict(
                type='rect',
                xref='paper', yref='paper',
                x0=0, y0=0,
                x1=1, y1=1,
                line=dict(
                    color='black',  # Cor da borda
                    width=2,  # Largura da borda
                ),
                layer='below'  # Coloca a borda abaixo dos traços do gráfico
            )
        ]
    )
    return fig, df_g

#def plot_students_per_year(filtered_df):