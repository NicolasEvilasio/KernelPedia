import streamlit as st
from openai import OpenAI
from chatbot import ChatBot

# Importação do style sheet em CSS
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Título da página
st.title('KernelPedia - Enciclopédia Interativa de Sistemas Operacionais')

# APIKEY
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Criação do chatbot
chatbot = ChatBot(client)

# Exibir a mensagem inicial
chatbot.display_messages()

# Criação dos botões de perguntas sugeridas
chatbot.display_question_buttons()

# Criação do campo de input
if prompt := st.chat_input('What is up?'):
    chatbot.handle_input(prompt)
