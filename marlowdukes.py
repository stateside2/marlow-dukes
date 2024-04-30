
# in terminal > pip install pandas openpyxl streamlit streamlit-option-menu
# pip install pipreqs ... installs whats needed to createt the reqirements.txt
# excel sheet names = League Table, Captains, MOTM, Goals, Board Room
# icons from bootstrap

# import os
import time
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

excel_file = "data/latest_data.xlsx"
st.set_page_config(page_title="Marlow Dukes", page_icon="images/marlowdukesicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

# --- HIDE STREAMLIT HEADER/FOOTER MENUS ---
hide_st_style = """ 
	<style>MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>
	"""
st.markdown(hide_st_style, unsafe_allow_html=True)
# ----

st.image("images/marlowdukesbanner.png", use_column_width="auto")
st.divider()


# --- MENU NAVBAR ---
menu_selection = option_menu(menu_title=None,
	options=["League Table", "Goals", "MOTM", "Board Room"],
	icons=["trophy-fill", "life-preserver", "person-arms-up", "bank"],
	default_index=0,
	orientation="horizontal")

st.divider()

# --- PANDAS DATA FRAME SELECTION ---
df_ltable = pd.read_excel(excel_file, skiprows=[0,1,3,37,38], sheet_name='League Table', usecols=[0,52,54,58,59])
df_goals = pd.read_excel(excel_file, skiprows=[0,1,3,37,38,39,40], sheet_name='Goals', usecols=[0,52])
df_broom = pd.read_excel(excel_file, skiprows=7, sheet_name='Board Room', usecols=[12,13])
df_motm = pd.read_excel(excel_file, skiprows=[1,35,36,37,38,39], sheet_name='MOTM', usecols=[0,52])


if menu_selection == "League Table":
	st.dataframe(df_ltable, width=None, height=1225, use_container_width=True, hide_index=True, column_order=["POSITION","PLAYER","PLAYED","G/D","PTS"], column_config={"POSITION": " ", "PLAYED": "P", "G/D": "GD", "PTS": "Pts"})
if menu_selection == "Goals":
	st.dataframe(df_goals, width=None, height=1225, use_container_width=True, hide_index=True, column_config={"TOTAL": "GOALS"})
if menu_selection == "Board Room":
	st.dataframe(df_broom, width=None, height=1225, use_container_width=True, hide_index=True, column_config={"Unnamed: 12": "PLAYER", "Unnamed: 13": "VISITS"})
if menu_selection == "MOTM":
	st.dataframe(df_motm, width=None, height=1225, use_container_width=True, hide_index=True)

# --- EXCEL SOURCE FILE DATE ---
# file_totalsecs = os.stat(excel_file).st_mtime
# file_year = str(time.gmtime(file_totalsecs).tm_year)
# file_month = str(time.gmtime(file_totalsecs).tm_mon)
# file_day = str(time.gmtime(file_totalsecs).tm_mday)
# st.write(file_day,"/",file_month,"/",file_year)

st.write("15/4/2024")

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
