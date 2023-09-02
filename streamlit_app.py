import streamlit
import pandas

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
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index)) 

# display da tabela na pagina
streamlit.dataframe(my_fruit_list)
