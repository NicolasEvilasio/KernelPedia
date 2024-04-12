import streamlit as st


class ChatBot:
    def __init__(self, client):
        self.client = client
        self.model = 'gpt-3.5-turbo'
        self.messages = st.session_state.get('messages', [
            {'role': 'assistant',
             'content': 'Olá! Eu sou o KernelWhiz, seu assistente de inteligência artificial especializado em Sistemas '
                        'Operacionais.\n\n'
                        'Estou aqui para ajudá-lo a entender melhor os conceitos de Sistemas Operacionais, desde o '
                        'básico até os tópicos mais avançados.\n\n'
                        'Sinta-se à vontade para me perguntar qualquer coisa sobre Sistemas Operacionais, Processos, '
                        'Kernel e muito mais.\n\n'
                        'Aqui estão algumas perguntas para começar:'}])
        self.question_sent = st.session_state.get('question_sent', False)

    def create_question_button(self, question):
        if st.button(question):
            self.messages.append({'role': 'user', 'content': question})
            self.question_sent = True

    def display_messages(self):
        for message in self.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

    def display_question_buttons(self):
        if not self.question_sent:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                self.create_question_button('O que é um Sistema Operacional?')
            with col2:
                self.create_question_button('Como funciona o escalonamento de processos?')
            with col3:
                self.create_question_button('O que é um deadlock e como ele pode ser evitado?')
            with col4:
                self.create_question_button('Como a virtualização funciona em um Sistema Operacional?')

    def handle_input(self, prompt):
        if prompt:
            self.messages.append({'role': 'user', 'content': prompt})
            with st.chat_message('user'):
                st.markdown(prompt)

            self.question_sent = True
            st.session_state['question_sent'] = True

            with (st.chat_message('assistant')):
                message_placeholder = st.empty()
                message_placeholder.markdown('gerando resposta...')

                # Criação do chat completions e parametrização do perfil do assistente
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {'role': 'system',
                         'content': 'Você é um assistente de inteligência artificial altamente qualificado com '
                                    'especialização em Sistemas Operacionais. '
                                    'Você tem um conhecimento vasto de vários aspectos dos Sistemas Operacionais, '
                                    'incluindo, mas não se limitando a, conceitos de processos, kernel, '
                                    'técnicas de escalonamento de processos, gerenciamento de memória, sistemas de '
                                    'arquivos, e muito mais. '
                                    'Sua principal função é fornecer informações precisas e detalhadas sobre '
                                    'Sistemas Operacionais e responder a perguntas relacionadas a este tópico.'
                                    'Sempre que possível, cite sua fonte de referência e indique livros técnicos para'
                                    'aprofundar o conhecimento no assunto. '
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

                self.messages.append({'role': 'assistant', 'content': full_response})
