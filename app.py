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

#Start engine
load_dotenv()
password=os.getenv('data_base_password')
bd = "food"
connection_string = 'mysql+pymysql://root:' + password + '@localhost/'+bd
engine = create_engine(connection_string)
engine

##select botton for food_category
#query_food_category=text('select distinct branded_food_category from branded_u')
#with engine.connect() as com:
#    food_category=pd.read_sql(query_food_category,com)
#category_selector=st.multiselect('select food categories',food_category,default=[])
#
#if category_selector==[] or category_selector==[None]:
#    query_brand_name=text(f'select distinct brand_name from branded_u')
#    with engine.connect() as com:
#            brand_category=pd.read_sql(query_brand_name,com)
#    brand_selector_1=st.multiselect('select brand',brand_category,default=[])
#
#
##select botton for food_category
#if category_selector:
#    query_brand_name=text(f'select distinct brand_name from branded_u where branded_food_category in {category_selector}'.replace('[','(').replace(']',')'))
#    with engine.connect() as com:
#        brand_category=pd.read_sql(query_brand_name,com)
#    brand_selector=st.multiselect('select brand',brand_category,default=[])
#    if brand_selector==[]:
#        query_food=text(f'select * from branded_u where branded_food_category in {category_selector}'.replace('[','(').replace(']',')'))
#        with engine.connect() as com:
#            food_avai=pd.read_sql(query_food,com)
#        st.dataframe(food_avai)
#    else:
#        query_food=text(f'select * from branded_u where branded_food_category in {category_selector} and brand_name in {brand_selector}'.replace('[','(').replace(']',')'))
#        with engine.connect() as com:
#            food_avai=pd.read_sql(query_food,com)
#        st.dataframe(food_avai)
#
#test
        
 #select botton for food_category

query_dict_selector={}
query_start_selector='select distinct column_name from branded_u'

def selector():

    if len(query_dict_selector)>0:
        query_food_category=query_start_selector+' where '+' and '.join(query_dict_selector.values())
    else:
       query_food_category=query_start_selector
    return query_food_category

query_food_category=selector()

with engine.connect() as com:
    food_category=pd.read_sql(text(query_food_category.replace('column_name','branded_food_category')),com)
category_selector=st.multiselect('select food categories',food_category,default=[])

if category_selector:
    query_dict_selector['branded_food_category']=f'branded_food_category in {category_selector}'.replace('[','(').replace(']',')')
else:
    query_dict_selector.pop('branded_food_category',None)

query_food_category=selector()

with engine.connect() as com:
   brand_category=pd.read_sql(text(query_food_category.replace('column_name','brand_name')),com)
brand_selector=st.multiselect('select brand',brand_category,default=[])

if brand_selector:
    query_dict_selector['brand_name']=f'brand_name in {brand_selector}'.replace('[','(').replace(']',')')
else:
    query_dict_selector.pop('brand_name',None)


st.write(query_food_category)
st.write(query_dict_selector)
query_start='select brand_name, branded_food_category, description, serving_size, serving_size_unit, Calories, Fat, Cholesterol, Sodium, Carbohydrate, Fiber, Total_sugars, Sugars_added, Protein from branded_u join food_f using(fdc_id)'
query_list=[]

#select botton for food_category
if category_selector:
    query_list.append(f'branded_food_category in {category_selector}'.replace('[','(').replace(']',')'))
 
         
if brand_selector:
    query_list.append(f'brand_name in {brand_selector}'.replace('[','(').replace(']',')'))
   
             

if st.button('show result'):
    if query_list:
        query_food=text(query_start+' where '+' and '.join(query_list))
        
    else:
        query_food=text(query_start)
       
    
    st.write(query_food)
   

    with engine.connect() as com:
        food_avai=pd.read_sql(query_food,com)
    st.dataframe(food_avai)

    st.bar_chart(data=food_avai,x='description', y=['Protein','Fat'])


    
Protein = food_avai['Protein'] 
Fat= food_avai['Fat']
 
 
# Make the plot
plt.bar( Protein, color ='r',label ='Protein') 
plt.bar(Fat, color ='g', label ='Fat')
st.plt.show() 



#if category_selector:
#    query_food=text(f'select * from branded_u where branded_food_category in {category_selector}'.replace('[','(').replace(']',')'))
#    with engine.connect() as com:
#        food_avai=pd.read_sql(query_food,com)
#    st.dataframe(food_avai)
#
    
