import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import text
import os
import seaborn as sns

load_dotenv()
password=os.getenv('data_base_password')
bd = "food"
connection_string = 'mysql+pymysql://root:' + password + '@localhost/'+bd
engine = create_engine(connection_string)

st.session_state.query_dict_selector={}
query_start_selector='select distinct column_name from branded_u'
def sql_multiselect(column_name , engine):
    with engine.connect() as com:
        if len([values for key,values  in st.session_state.query_dict_selector.items() if key != column_name])>0:
            st.session_state.query_food_category=query_start_selector+' where '+' AND '.join([values for key,values  in st.session_state.query_dict_selector.items() if key != column_name ]) 
            if st.session_state.query_dict_selector.get(column_name):
                st.session_state.query_food_category+= " OR " +st.session_state.query_dict_selector.get(column_name)
        else:
           st.session_state.query_food_category=query_start_selector
        df = pd.read_sql(text(st.session_state.query_food_category.replace('column_name',column_name)),com)
    return df

def selector():
    try:

        if st.session_state.category_selector:
            st.session_state.query_dict_selector['branded_food_category']=f'branded_food_category in {st.session_state.category_selector}'.replace('[','(').replace(']',')')
        else:
            st.session_state.query_dict_selector.pop('branded_food_category',None)
        if st.session_state.brand_selector:
            st.session_state.query_dict_selector['brand_name']=f'brand_name in {st.session_state.brand_selector}'.replace('[','(').replace(']',')')
        else:
            st.session_state.query_dict_selector.pop('brand_name',None)

  
    except:
        pass
    
    
selector()    

food_category=sql_multiselect('branded_food_category',engine)

category_selector=st.multiselect('select food categories',
                                 food_category,
                                 default=st.session_state.get('category_selector') if st.session_state.get('category_selector') else []                            ,
                                 key='category_selector',
                                 on_change=selector)






brand_category=  sql_multiselect('brand_name' , engine)
brand_selector=st.multiselect('select brand',
                              brand_category,
                              default=st.session_state.get('brand_selector') if st.session_state.get('brand_selector') else [],
                              key='brand_selector',
                              on_change= selector)


st.write(st.session_state.query_food_category)
st.write(st.session_state.query_dict_selector)

# Add a title to the sidebar
st.sidebar.title("Select Nutrients: ")

features = [
    'Calories',
    'Fat',
    'Cholesterol',
    'Sodium',
    'Carbohydrate',
    'Fiber',
    'Total_sugars',
    'Sugars_added',
    'Protein'
]

selected_features = {}
st.write(selected_features)

for feature in features:
    toggle_state = st.sidebar.checkbox(f'Activate {feature}')
    if toggle_state:
        # Add a slider for selecting a range
        min_value, max_value = st.sidebar.slider(f'Select range for {feature}', 0.0, 100.0, (0.0, 100.0))
        selected_features[feature] = (min_value, max_value)

# Construct the SELECT statement dynamically
select_clause = ', '.join(selected_features.keys())
selected_features_query = 'and '.join([f'"{feature}" >= {min_value} AND "{feature}" <= {max_value}' 
                                     for feature, (min_value, max_value) in selected_features.items()])

query_start = 'select brand_name, branded_food_category, description, serving_size, serving_size_unit, '
query_end = f' from branded_u join food_f using(fdc_id) WHERE {selected_features_query} and '.replace('"','')
full_query = query_start + select_clause + query_end

st.write("Generated SQL query:", full_query)


sql_query = "SELECT " + ", ".join(selected_features) + " FROM data;"
st.write(sql_query)

query_start='select brand_name, branded_food_category, description, serving_size, serving_size_unit, ' + ', '.join(selected_features) +  ' from branded_u join food_f using(fdc_id)'
query_list=st.session_state.get('query_dict_selector').values() if st.session_state.get('query_dict_selector') else []

#query graph

features_graph=list(selected_features.keys())
st.write(features_graph)
query_graph=f' select description, nutrient_id, amount from branded join food_f using(fdc_id) join food_nutrient using(fdc_id) where nutrient_id in {features_graph}'.replace('[','(').replace(']',')')
st.write(query_graph)


#select botton for st.session_state.food_category
         

if st.button('show result'):
    if query_list:
        query_food=text(full_query +' and '.join(query_list))
        
    else:
        query_food=text(full_query)
       
    
    st.write(query_food)
   

    with engine.connect() as com:
        food_avai=pd.read_sql(query_food,com)
    st.dataframe(food_avai)


query_test=text(query_graph)
with engine.connect() as com:
       food_graph=pd.read_sql(query_test,com)



sns.set(style="whitegrid")
fig = sns.catplot(data=food_graph,x="nutrient_id", y="amount",kind='bar',height=6)

         
st.pyplot(fig)
