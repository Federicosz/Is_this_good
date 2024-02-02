import streamlit as st 
import requests
import pymysql
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy import VARCHAR, TEXT, FLOAT, DATE, BIGINT, INTEGER, INT
import pandas as pd
import os

#Start engine
load_dotenv()
password=os.getenv('data_base_password')
bd = "food"
connection_string = 'mysql+pymysql://root:' + password + '@localhost/'+bd
engine = create_engine(connection_string)
engine

#select botton for food_category
query_food_category=text('select distinct branded_food_category from branded_u')
with engine.connect() as com:
    food_category=pd.read_sql(query_food_category,com)
category_selector=st.multiselect('select food categories',food_category)

#select botton for food_categor
query_brand_name=text('select distinct brand_name from branded_u')
with engine.connect() as com:
    brand_category=pd.read_sql(query_brand_name,com)
brand_selector=st.multiselect('select brand',brand_category)

if category_selector:
    query_food=text(f'select * from branded_u where branded_food_category in {category_selector}'.replace('[','(').replace(']',')'))
    with engine.connect() as com:
        food_avai=pd.read_sql(query_food,com)
    st.dataframe(food_avai)
