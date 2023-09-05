import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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


def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  streamlit.dataframe(fruityvice_normalized)

# New section to display api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.stop()

# consultando metadados no snowflake
streamlit.header("The fruit load list contais:")
# Snowflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

# adicionando uma fruta
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+ new_fruit + "')")
    return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button("Add a Fruit to the list"):
  my_cnx = snowflake.connector.connect("**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)





