import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
import pymysql
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import text
import os


load_dotenv()
password=os.getenv('data_base_password')
bd = "food"
connection_string = 'mysql+pymysql://root:' + password + '@localhost/'+bd
engine = create_engine(connection_string)
engine

with engine.connect() as com:
    df=pd.read_sql(text('select * from branded_u'),com)


dynamic_filters = DynamicFilters(df, filters=['branded_food_category','brand_name'])

with st.sidebar:
    st.write("Apply filters in any order 👇")

dynamic_filters.display_filters(location='sidebar')

dynamic_filters.display_df()