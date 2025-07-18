# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
# from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:"
    ,my_dataframe
    ,max_selections=5
)
if ingredients_list:
    st.write("You selected:", ingredients_list)
    st.text(ingredients_list)
    
    ingredients_string =''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) 
    values ('""" + ingredients_string + """', '""" + name_on_order + """' ) """
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order + '!', icon='✅')
      
#new section to display smoothie froot nutrition info
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

