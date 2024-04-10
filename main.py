import os
import openai
import streamlit as st
from openai import OpenAI


client = OpenAI(
    api_key=st.secrets['OPENAI_API_KEY']
)

# Título
st.title('KernelPedia - Enciclopédia Interativa de Sistemas Operacionais')

# Descrição do propósito do site
st.text('Bem-vindo ao KernelPedia, sua Enciclopédia Interativa de Sistemas Operacionais!\n'   
        'Você pode fazer perguntas sobre sistemas operacionais e aprender mais sobre eles.')

st.subheader('Perguntas sugeridas:')

perguntas = [
    "O que são sistemas operacionais?",
    "O que é um sistema Unix?",
    "O que são processos em um sistema operacional?",
    "Qual é a relação entre processos e sistemas operacionais?"
]

# Layout das perguntas sugeridas
col1, col2, col3, col4 = st.columns(4)
for i, pergunta in enumerate(perguntas):
    with eval(f'col{i % 4 + 1}'):
        if st.button(pergunta):
            st.session_state.input_text = pergunta

# Campo de entrada para a pergunta do usuário
input_text = st.text_input("Faça uma pergunta sobre sistemas operacionais:",
                           value=st.session_state.input_text if 'input_text' in st.session_state else '')

# Botão para enviar a pergunta
if st.button('Enviar'):
    # Chamada à API do OpenAI para obter a resposta
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {'role': 'system',
             'content': "You are an experient university Information System's teacher. "
                        "You are skilled in explaining complex programming concepts and how did Operational Systems works! ",
             'role': 'user',
             'content': f'{input_text}'
             }
        ]
    )
    # Exibindo a resposta do chatbot
    st.subheader("Resposta:")
    st.text_area('resposta', response.choices[0].message.content, height=None, max_chars=None, key=None,
                 label_visibility='hidden')
