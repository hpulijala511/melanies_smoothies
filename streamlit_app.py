# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('name on smoothie:')
st.write("The name on smoothie", name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
    'choose upto 5:'
    ,my_dataframe

)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen
    #st.write(ingredients_string)  
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    time_to_insert = st.button("submit order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('your smoothie ordered')



     

