# Import python packages
#import streamlit as st
#from snowflake.snowpark.functions import col

#import requests

# Write directly to the app
#st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
#st.write(
 # """ Choose the fruits yoy want in your custom Smoothie
  #"""
#)

#import streamlit as st

#name_on_order = st.text_input("Name on Smoothe:")
#st.write("The name on your smoothie will be:", name_on_order)

#cnx = st.connection("snowflake")
#session = cnx.session()
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the Snowpark Dataframe to a Pandas Datafraame so we can use the LOC function
#pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

#ingredients_list = st.multiselect(
 #   'choose up to 5 ingredients:'
  #  , my_dataframe
   # , max_selections=5
#)

#if ingredients_list:
    #ingredients_string = ''
    
    #for fruit_chosen in ingredients_list:
        #ingredients_string += fruit_chosen + ' '
        #search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        #st.subheader(fruit_chosen + 'Nutrition Information')
        #smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        #smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{SEARCH_ON}")
        #sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

        
    #st.write(ingredients_string)

    #my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            #values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()


    
   # time_to_insert = st.button ('Submit Order')

    #if time_to_insert:

    #st.write(my_insert_stmt)
    #if ingredients_string:
        #session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")

#import requests
#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
#sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)




# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# App title and description
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Input for name on order
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert Snowpark DataFrame to Pandas for local lookups
pd_df = my_dataframe.to_pandas()

# Multiselect widget for choosing ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

# Process selected ingredients
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Safely retrieve SEARCH_ON value
        if pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].notnull().any():
            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        else:
            search_on = fruit_chosen  # fallback if null

        # Show nutrition information section
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # Call SmoothieFroot API using the correct search_on variable
        try:
            smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
            if smoothiefroot_response.status_code == 200:
                sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
            else:
                st.warning(f"Could not find data for {search_on}.")
        except Exception as e:
            st.error(f"Error fetching data for {fruit_chosen}: {e}")

    # Build SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    # Submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success('✅ Your Smoothie is ordered!')
        except Exception as e:
            st.error(f"❌ Error placing order: {e}")

