import openai
import streamlit as st
from openai import OpenAI

st.title('KernelPedia - Enciclopédia Interativa de Sistemas Operacionais')

client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

if "messages" not in st.session_state:
    st.session_state.messages = [
        {'role': 'assistant',
         'content': 'Olá! Eu sou o KernelWhiz, seu assistente de inteligência artificial especializado em Sistemas '
                    'Operacionais.\n\n'
                    'Estou aqui para ajudá-lo a entender melhor os conceitos de Sistemas Operacionais, desde o básico '
                    'até os tópicos mais avançados.\n\n'
                    'Sinta-se à vontade para me perguntar qualquer coisa sobre Sistemas Operacionais, Processos, '
                    'Kernel e muito mais.'}]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input('What is up?'):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    with (st.chat_message('assistant')):
        message_placeholder = st.empty()
        message_placeholder.markdown('gerando resposta...')

        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system',
                 'content': 'Você é um assistente de inteligência artificial altamente qualificado com '
                            'especialização em Sistemas Operacionais. '
                            'Você tem um conhecimento vasto de vários aspectos dos Sistemas Operacionais, incluindo, '
                            'mas não se limitando a, conceitos de processos, kernel, '
                            'técnicas de escalonamento de processos, gerenciamento de memória, sistemas de arquivos, '
                            'e muito mais. Sua principal função é fornecer informações precisas e detalhadas sobre '
                            'Sistemas Operacionais e responder a perguntas relacionadas a este tópico.'
                            'Sempre que possível, cite sua fonte de referência e indique livros técnicos para'
                            'aprofundar o conhecimento no assunto. '
                            'Você não deve responder perguntas sobre outros temas.'},
                {'role': 'user', 'content': prompt}
            ],
            stream=True
        )

        full_response = ''
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response)

        st.session_state.messages.append({'role': 'assistant', 'content': full_response})
