import pandas as pd
import streamlit as st

st.set_page_config(layout='wide')
st.title('Is this good?')
st.markdown('_Prototype v0.0.0.0.1_')

@st.cache_data
def load_data(path: str):
    data=pd.read_csv(path)

uploaded_file= st.sidebar.file_uploader('Choose a file')

if uploaded_file is None:
    st.info('Upload a file though config', incon='i')
    st.stop()

df= load_data(uploaded_file)
st.dataframe(df)
