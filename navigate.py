import streamlit as st

st.set_page_config(page_title="Marlow Dukes", page_icon="images/marlowdukesicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

home_page = st.Page("HOME.py", title="HOME", icon=":material/sports_and_outdoors:")
stats_page = st.Page("6_STATISTICS.py", title="STATISTICS", icon=":material/bar_chart:")
hof_page = st.Page("HALL_OF_FAME.py", title="HALL OF FAME", icon=":material/trophy:")
page_2024 = st.Page("9_2024_SEASON.py", title="2024", icon=":material/stars:")


with st.sidebar:
	st.subheader("Current Season")
	st.page_link(home_page, label=home_page.title, icon=home_page.icon)
	st.page_link(stats_page, label=stats_page.title, icon=stats_page.icon)
	st.page_link(hof_page, label=hof_page.title, icon=hof_page.icon)

	st.subheader("Past Seasons")
	st.page_link(page_2024, label=page_2024.title, icon=page_2024.icon)

	st.subheader("Other")
	st.page_link(page="https://www.marlowdukes.co.uk", label="BRAND PAGE", icon=":material/sell:")
	st.page_link(page="https://marlow-merch.myspreadshop.co.uk/", label="SHOP", icon=":material/storefront:")

	st.write("---")

pg = st.navigation([home_page, stats_page, hof_page, page_2024], position="hidden")
pg.run()


# --- ICONS ... 📕, 📚, 📖, 📘, 📈, 📊, 📋, 🗄️, 🛒, 🏪,🏅, 🚩, 💼, 
