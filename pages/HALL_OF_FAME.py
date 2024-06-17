
# import os #--- NEEDED FOR THE FILE DATE CALCULATION
# import time
import pandas as pd
import streamlit as st
# from streamlit_option_menu import option_menu #--- NEEDED FOR THE FIRST NAVBAR
import streamlit_antd_components as sac #--- NEEDED FOR THE 2ND NAVBAR


excel_file = "data/hall_of_fame.xlsx"
st.set_page_config(page_title="Hall Of Fame", page_icon="images/marlowdukesicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

# --- HIDE STREAMLIT HEADER/FOOTER MENUS ---
hide_st_style = """ 
	<style>MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>
	"""
st.markdown(hide_st_style, unsafe_allow_html=True)
# ----

# --- BANNER IMAGE
st.image("images/marlowdukesbannerHOF.png", use_column_width="auto")
st.divider()


# --- MENU NAVBAR --- 
hof_selection = sac.buttons(
   items=[
    sac.ButtonsItem(label="Champions", icon="award"),
    sac.ButtonsItem(label="Podiums", icon="list-ol"),
], label=None, format_func=None, align="center", size="md", radius="md", color="#4682b4", use_container_width=True)
# ---


# --- PANDAS DATA FRAME SELECTION ---
if hof_selection == "Champions":
	hof_champs = pd.read_excel(excel_file, sheet_name="CHAMPIONS", skiprows=None, usecols=[0,1,2,6])
	hof_champs["SEASON"] = hof_champs["SEASON"].astype(str) #--- CONVERTS 2,023 TO 2023
	st.dataframe(hof_champs, width=None, height=458, use_container_width=True, hide_index=True, column_order=["SEASON","CHAMPION","PLAYED","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

if hof_selection == "Podiums":

	hof_2023 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=None, nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2023, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2023","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

	hof_2022 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=[0,1,2,3], nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2022, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2022","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

	hof_2021 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=[0,1,2,3,4,5,6,7], nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2021, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2021","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

	hof_2020 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11], nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2020, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2020","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

	hof_2019 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2019, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2019","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

	hof_2018 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2018, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2018","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

	hof_2017 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2017, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2017","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

	hof_2016 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27], nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2016, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2016","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

	hof_2015 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31], nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2015, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2015","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

	hof_2014 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35], nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2014, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2014","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

	hof_2013 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39], nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2013, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2013","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

	hof_2012 = pd.read_excel(excel_file, sheet_name="TOP3", skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43], nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(hof_2012, width=None, height=142, use_container_width=True, hide_index=True, column_order=["2012","PLAYER","PLAYED","GD","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})


# --- PANDAS DATA FRAME SELECTION ---
# df_ltable = pd.read_excel(excel_file, skiprows=[0,1,3,37,38], sheet_name='League Table', usecols=[0,52,54,58,59])
# df_goals = pd.read_excel(excel_file, skiprows=[0,1,3,37,38,39,40], sheet_name='Goals', usecols=[0,52])
# df_broom = pd.read_excel(excel_file, skiprows=7, sheet_name='Board Room', usecols=[12,13])
# df_motm = pd.read_excel(excel_file, skiprows=[1,35,36,37,38,39], sheet_name='MOTM', usecols=[0,52])


# if menu_selection == "League Table":
# 	st.dataframe(df_ltable, width=None, height=1225, use_container_width=True, hide_index=True, column_order=["POSITION","PLAYER","PLAYED","G/D","PTS"], column_config={"POSITION": " ", "PLAYED": "P", "G/D": "GD", "PTS": "Pts"})
# if menu_selection == "Goals":
# 	st.dataframe(df_goals, width=None, height=1225, use_container_width=True, hide_index=True, column_config={"TOTAL": "GOALS"})
# if menu_selection == "Board Room":
# 	st.dataframe(df_broom, width=None, height=1225, use_container_width=True, hide_index=True, column_config={"Unnamed: 12": "PLAYER", "Unnamed: 13": "VISITS"})
# if menu_selection == "MOTM":
# 	st.dataframe(df_motm, width=None, height=1225, use_container_width=True, hide_index=True)


st.divider()


# --- HALL OF FAME LINK NEEDED ---

# --- FUTURE ADDITIONS
# st.markdown("##")
# st.snow() # --- WINTER / XMAS UPDATE --- DOES IT WORK ON CELLPHONE?
# st.balloons() # --- END OF SEASON CELEBRATION --- DOES IT WORK ON CELLPHONE?
# st.toast("xxxxxxx is the winner", icon="🔥") # --- WINNER ANNOUNCEMENT --- DOES IT WORK ON CELLPHONE?
# time.sleep(1) --- ALSO HAVE TO import time

# st.title("Title Marlow Dukes") --- st.header("This is a header") --- st.subheader("Sub Header") --- st.markdown("data correct as of ...")

# col_list=df_broom.columns
# st.markdown(col_list)
