import openai
import streamlit as st
from openai import OpenAI

# Importação do style sheet em CSS
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Título da página
st.title('KernelPedia - Enciclopédia Interativa de Sistemas Operacionais')

# APIKEY
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])


# Função para criar um botão e processar a pergunta
def create_question_button(question):
    if st.button(question):
        st.session_state['selected_question'] = question
        st.session_state['question_sent'] = True
        ## código aqui
        st.rerun()
    else:
        st.session_state['selected_question'] = False


# Verificar se uma pergunta foi enviada ou se o usuário digitou algo
if 'question_sent' not in st.session_state:
    st.session_state['question_sent'] = False

# Definir o modelo do GPT
if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

# Definir a mensagem inicial
if "messages" not in st.session_state:
    st.session_state.messages = [
        {'role': 'assistant',
         'content': 'Olá! Eu sou o KernelWhiz, seu assistente de inteligência artificial especializado em Sistemas '
                    'Operacionais.\n\n'
                    'Estou aqui para ajudá-lo a entender melhor os conceitos de Sistemas Operacionais, desde o básico '
                    'até os tópicos mais avançados.\n\n'
                    'Sinta-se à vontade para me perguntar qualquer coisa sobre Sistemas Operacionais, Processos, '
                    'Kernel e muito mais.\n\n'
                    'Aqui estão algumas perguntas para começar:'}]

# Exibir a mensagem inicial
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Criação dos botões de perguntas sugeridas
prompt_button = False
if not st.session_state['question_sent']:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        create_question_button('O que é um Sistema Operacional?')
    with col2:
        create_question_button('Como funciona o escalonamento de processos?')
    with col3:
        create_question_button('O que é um deadlock e como ele pode ser evitado?')
    with col4:
        create_question_button('Como a virtualização funciona em um Sistema Operacional?')


# Criação do campo de input
def process_input(prompt, client):
    if prompt:
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)

        with (st.chat_message('assistant')):
            message_placeholder = st.empty()
            message_placeholder.markdown('gerando resposta...')

            st.session_state['question_sent'] = True

            # Criação do chat completions e parametrização do perfil do assistente
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
                                'Você não deve responder perguntas sobre outros temas.'},
                    {'role': 'user', 'content': prompt}
                ],
                stream=True  # habilita a exibição da resposta por 'partes'
            )

            # Exibição da resposta em stream
            full_response = ''
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response)

            st.session_state.messages.append({'role': 'assistant', 'content': full_response})


if st.session_state['selected_question']:
    process_input(st.session_state['selected_question'], client)
    st.session_state['selected_question'] = False
    st.rerun()

else:
    # Criação do campo de input
    if prompt := st.chat_input('What is up?'):
        process_input(prompt, client)
        st.rerun()
