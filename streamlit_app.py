import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title("My parents New Healthy Diner")

streamlit.header("Breakfast Favorites")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Acovado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

# Vamos colocar uma lista de seleção aqui para que eles possam escolher as frutas que desejam incluir 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index)) 
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display da tabela na pagina
streamlit.dataframe(fruits_to_show)

# nova seção para fazer o display da api fruityvice

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)


# normalizando o response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# dataframe normalizado
streamlit.dataframe(fruityvice_normalized)

# consultando metadados no snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)





