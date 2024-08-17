# Função de filtragem de colunas
def filter_columns(df, filters: list):
    selected_columns = [True] * len(df.columns)  # Inicializa todas as colunas como True
    for index, column in enumerate(df.columns):
        if any(filter in column for filter in filters):
            selected_columns[index] = False
    return df[df.columns[selected_columns]]
# Função de limpeza do dataset
def cleaning_dataset(df):
    _df = df.dropna(subset=df.columns.difference(['NOME']), how='all')  # Remove linhas com todas as colunas NaN, exceto 'NOME'
    _df = _df[~_df.isna().all(axis=1)]  # Remove linhas com apenas NaN
    return _df

# Função para converter colunas para float64 com duas casas decimais
def convert_to_float64_with_two_decimal_places(df, columns):
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').round(2)
    return df

# Função para carregar texto de arquivo
def load_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Função para o chat com OpenAI
def chat_with_openai():
    # Set OpenAI API key from Streamlit secrets
    #client = OpenAI(api_key=OPENAI_API_KEY)

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

# Função de ajuste dos dados de alunos
def ajuste(dados_alunos):
    colunas_interesse = ['IdAluno', 'DataNascimento']
    idade_alunos = dados_alunos[colunas_interesse]
    idade_alunos2 = idade_alunos.drop(793)         # Erro na base
    idade_alunos2['DataNascimento'] = pd.to_datetime(idade_alunos2['DataNascimento'])
    idade_alunos2['Idade']=2022-idade_alunos2['DataNascimento'].dt.year        # Cálculo da idade

    # Agrupamento por faixa etária
    fx_etaria = [
    (idade_alunos2['Idade'] >= 5) & (idade_alunos2['Idade'] <= 9),
    (idade_alunos2['Idade'] >= 10) & (idade_alunos2['Idade'] <= 14),
    (idade_alunos2['Idade'] >= 15) & (idade_alunos2['Idade'] <= 19),
    (idade_alunos2['Idade'] >= 20) & (idade_alunos2['Idade'] <= 24),
    (idade_alunos2['Idade'] >= 25)
]

    grupos = ['05 a 09 anos', '10 a 14 anos', '15 a 19 anos', '20 a 24 anos', '25 anos ou mais']
    idade_alunos2['Grupo de idade'] = np.select(fx_etaria, grupos)
    idade_alunos2 = idade_alunos2[idade_alunos2['Idade'] > 0]
    qtde_alunos_idade = idade_alunos2['Grupo de idade'].value_counts().sort_index()

    return qtde_alunos_idade
    
