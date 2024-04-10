from kernelpedia import KernelPedia
import streamlit as st


app = KernelPedia(st.secrets['OPENAI_API_KEY'])
app.display_ui()
