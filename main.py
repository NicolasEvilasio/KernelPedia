import os
import openai
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv('.env')
client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY")
)

st.title('Ola, sou o seu instrutor digital')
st.text('Pergunte-me alguma coisa sobre Sistemas Operacionais.')

st.write('Perguntas sugeridas:')
with st.container(height=150):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        pergunta1 = st.button('O que são sistemas operacionais?')
        if pergunta1:
            st.session_state.input_text = 'O que são sistemas operacionais?'

    with col2:
        pergunta2 = st.button('O que é um sistema Unix?')
        if pergunta2:
            st.session_state.input_text = 'O que é um sistema Unix?'

    with col3:
        pergunta3 = st.button('O que são processos de um Sistema Operacional?')
        if pergunta3:
            st.session_state.input_text = 'O que são processos de um Sistema Operacional?'

    with col4:
        pergunta4 = st.button('Qual a relação entre processos e Sistema Operacional?')
        if pergunta4:
            st.session_state.input_text = 'Qual a relação entre processos e Sistema Operacional?'

st.divider()

input_text = st.text_input("Você:",
                           value=st.session_state.input_text if 'input_text' in st.session_state else '',
                           max_chars=None,
                           key=None,
                           type='default')

if st.button('Enviar'):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {'role': 'system',
             'content':"You are an experient university Information System's teacher. "
              "You are skilled in explaining complex programming concepts and how did Operational Systems works! ",
             'role':'user',
             'content':f'{input_text}'
             }
        ]
    )
    st.text_area("Chatbot:", value=response.choices[0].message.content, height=None, max_chars=None, key=None)