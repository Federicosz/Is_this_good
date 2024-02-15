import streamlit as st
import pandas as pd
pip install pymysql
import pymysql
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import text
import os
import seaborn as sns
import plotly.express as px
import sys

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
    
st.set_page_config(layout='wide')
st.title('Is this good?')
st.markdown('_Prototype v0.0.0.0.1_')
col1, col2, col3 = st.columns(3)

selector()    

food_category=sql_multiselect('branded_food_category',engine)

with col1:
    st.subheader("Select Food categories: ")
    category_selector=st.multiselect(label='branded_food_category',label_visibility='hidden',
                                     options=food_category,
                                     default=st.session_state.get('category_selector') if st.session_state.get('category_selector') else []                            ,
                                     key='category_selector',
                                     on_change=selector)






brand_category=  sql_multiselect('brand_name' , engine)
with col2:
    st.subheader("Select Food brand: ")
    brand_selector=st.multiselect(label='brand_name',label_visibility='hidden',
                                  options=brand_category,
                                  default=st.session_state.get('brand_selector') if st.session_state.get('brand_selector') else [],
                                  key='brand_selector',
                                  on_change= selector)



#Ingridient avoid

query_condition= ' AND '
with col3:
    st.subheader("Ingredient to avoid: ")

    ingredient= st.toggle('yes')

    if ingredient:
        ingredient_input = st.text_input('Enter ingredients (separated by commas, in capital letters)')
        ingredients_list = [ingredient.strip().upper() for ingredient in ingredient_input.split(',')]

        conditions = []

        # Add conditions to exclude ingredients
        if ingredients_list:
            for ingredient in ingredients_list:
                if ingredient != '':
                    conditions.append(f" and ingredients NOT LIKE '%{ingredient}%'")
            query_condition =  ' AND '.join(conditions)
        else:
            query_conditon=' '
    else:
        query_condition= ' '

    


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



for feature in features:
    toggle_state = st.sidebar.checkbox(f'Activate {feature}')
    if toggle_state:
        # Set range up to 1000 for Cholesterol, Sodium, and Calories, and up to 100 for the rest
        if feature in ['Cholesterol', 'Sodium', 'Calories']:
            max_range = 1000.0
        else:
            max_range = 100.0
        # Add a slider for selecting a range
        min_value, max_value = st.sidebar.slider(f'Select range for {feature}', 0.0, max_range, (0.0, max_range))
        selected_features[feature] = (min_value, max_value)

# Construct the SELECT statement dynamically
select_clause = ', '.join(selected_features.keys())
selected_features_query = 'and '.join([f'"{feature}" >= {min_value} AND "{feature}" <= {max_value}' 
                                     for feature, (min_value, max_value) in selected_features.items()])

if len(selected_features)==0:
    st.write('Please select one or more Nutrients')
    sys.exit()

query_start = 'select fdc_id, brand_name, branded_food_category, description, serving_size, serving_size_unit, '
query_end = f' from branded_u join food_f using(fdc_id) WHERE {selected_features_query}'.replace('"','')
full_query = query_start + select_clause + query_end + query_condition

sql_query = "SELECT " + ", ".join(selected_features) + " FROM data;"


query_list=st.session_state.get('query_dict_selector').values() if st.session_state.get('query_dict_selector') else []

#query graph

features_graph=list(selected_features.keys())

query_graph=f' select branded.fdc_id, description, nutrient_id, amount from branded join food_f using(fdc_id) join food_nutrient using(fdc_id) where nutrient_id in {features_graph} and '.replace('[','(').replace(']',')')



#select botton for st.session_state.food_category
col1_s, col2_s= st.columns(2)        

#if st.button('show result'):
if query_list:
    query_food=text(full_query +' and ' +' and '.join(query_list))
        
else:
    query_food=text(full_query)
       
with engine.connect() as com:
    food_avai=pd.read_sql(query_food,com)
food_avai['select'] = [True] * 1 + [False] * (len(food_avai) - 1)
food_avai = food_avai[['select'] + [col for col in food_avai if col != 'select']]
with col1_s:
    st.subheader("Produts Avalailable: ")
    edit_food_avai= st.data_editor(food_avai,use_container_width=True,hide_index=True,column_config={'fdc_id':None})


selected_fdc_ids = edit_food_avai.loc[edit_food_avai['select'], 'fdc_id'].tolist()
query_fdc_ids=f' branded.fdc_id in {selected_fdc_ids} and '.replace('[','(').replace(']',')')



query_test=text(query_graph + query_fdc_ids + ' and '.join(query_list))
with engine.connect() as com:
       food_graph=pd.read_sql(query_test,com)


sns.set(style="whitegrid")
fig = px.histogram(food_graph, x="nutrient_id", y="amount", barmode='group',color='description', height=400,)
fig.update_layout(
    legend=dict(title='product', orientation='h', yanchor='bottom', y=-0.8, xanchor='right', x=.8),
    margin=dict(l=2, r=2, t=2, b=2),
    width=1200
)
with col2_s:
    st.subheader("Produts Avalailables selected: ")
    st.plotly_chart(fig)



description=list(food_avai['brand_name'] + ' - ' + food_avai['description'])

st.subheader("What product would you like to see ? ")
option = st.selectbox(label='a',label_visibility='hidden',options=description)


selected_brand_name, selected_description = option.split(' - ', 1)

# Filter the food_avai DataFrame based on the selected brand name and description
selected_product = food_avai[(food_avai['brand_name'] == selected_brand_name) & 
                             (food_avai['description'] == selected_description)]


fdc_item = selected_product['fdc_id'].iloc[0]
query_product=f'select fdc_id, Calories, Fat, Cholesterol, Sodium, Carbohydrate, Fiber, Total_sugars, Sugars_added, Protein, ingredients from branded_u where fdc_id={fdc_item}'

query_p=text(query_product)
with engine.connect() as com:
    selected_product_details=pd.read_sql(query_p,com)

# Display the details of the selected product
lastcol1, lastcol2, lastcol3=st.columns(3)

columns = ['Calories', 'Fat', 'Cholesterol', 'Sodium', 'Carbohydrate', 
           'Fiber', 'Total_sugars', 'Sugars_added', 'Protein']

# Display metrics for each column
with lastcol1:
    for column in columns:
        value = selected_product_details[column].iloc[0]
        unit = "g"  # Default unit is gram
        if column == 'Calories':
            unit = "kcal"
        elif column in ['Sodium', 'Cholesterol']:
            unit = "mg"
        value_f=f'{value}{unit}'
        st.metric(label=column,value=value_f)


ingredient_product_selected = selected_product_details['ingredients'].iloc[0]
with lastcol2:
    st.subheader("ingredients: ")
    st.markdown('- '+ ingredient_product_selected.replace(",","\n- "))


#pie

query_pie=f" select fdc_id, nutrient_id, amount from branded join food_f using(fdc_id) join food_nutrient using(fdc_id) where fdc_id={fdc_item} and nutrient_id in ('Fat','Fiber','Total_sugars','Protein')"
query_p_pie=text(query_pie)

with engine.connect() as com:
    selected_product_details_pie=pd.read_sql(query_p_pie,com)

pie = px.pie(selected_product_details_pie, values='amount', names='nutrient_id')
with lastcol3:
    st.subheader("Nutrients %: ")
    st.plotly_chart(pie)