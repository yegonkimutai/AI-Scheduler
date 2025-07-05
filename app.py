from agents import main_agent
from arm import Swarm
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == '__main__':
    swarm_client = Swarm()
    agent = main_agent

    st.title('Google Calendar AI Agent')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if prompt := st.chat_input('Enter your prompt here'):
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        with st.chat_message('user', avatar='👨🏻‍💻'):
            st.markdown(prompt)

        with st.chat_message('ai', avatar='🤖'):
            response = swarm_client.run(
                agent=agent,
                debug=False,
                messages=st.session_state.messages
            )
            st.markdown(response.messages[-1]['content'])
        st.session_state.messages.append({'role': 'assistant', 'content': response.messages[-1]['content']})
