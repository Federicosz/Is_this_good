import streamlit as st 
import requests
import pymysql
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy import VARCHAR, TEXT, FLOAT, DATE, BIGINT, INTEGER, INT
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

load_dotenv()
password=os.getenv('data_base_password')
bd = "food"
connection_string = 'mysql+pymysql://root:' + password + '@localhost/'+ bd
engine = create_engine(connection_string)
engine

col1, col2 = st.columns([3, 1])
data = np.random.randn(10, 1)


df = pd.DataFrame(
    [
       {"command": "st.selectbox", "rating": 4, "is_widget": True},
       {"command": "st.balloons", "rating": 5, "is_widget": False},
       {"command": "st.time_input", "rating": 3, "is_widget": True},
   ]
)
edited_df = st.data_editor(df)

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")



row1= st.columns(3)
row2= st.columns(2)

with row1:
   st.toggle('Protein') 
   st.toggle('d')
   st.toggle('b')

with row2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg")








query_food='select * from branded'

with engine.connect() as com:
    food_avai=pd.read_sql(query_food,com)
st.dataframe(food_avai)