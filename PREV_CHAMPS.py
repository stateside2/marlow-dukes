
import pandas as pd
import streamlit as st
import streamlit_antd_components as sac


excel_file_hof: str = "data/hall_of_fame.xlsx"

# --- THIS IS NOW SET IN THE NAVIGATE.py PAGE
# st.set_page_config(page_title="Marlow Dukes", page_icon="images/marlowdukesicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

# --- HIDE 1) STREAMLIT HEADER/FOOTER MENUS, 2) POP-UP DOWNLOAD, SEARCH, EXPAND DATAFRAME ELEMENTS, 3) EXPAND IMAGE  ---
hide_st_style = """ 
	<style>MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} 
	[data-testid="stElementToolbar"] {display: none;} 
	button[title="View fullscreen"] {visibility: hidden;} 
	</style>
	"""
st.markdown(hide_st_style, unsafe_allow_html=True)
# ----

# --- BANNER IMAGE
st.image("images/marlowdukesbannerHOF.png", use_container_width="auto")
st.divider()

# --- CHAMPIONS DF
df_hof_champs = pd.read_excel(excel_file_hof, sheet_name="CHAMPIONS", skiprows=None, usecols=[0,1,2,6])
df_hof_champs["SEASON"] = df_hof_champs["SEASON"].astype(str) #--- CONVERTS 2,023 TO 2023


st.dataframe(df_hof_champs, width=None, height=493, use_container_width=True, hide_index=True, column_order=["SEASON","CHAMPION","PLAYED","POINTS"], column_config={"PLAYED": "P", "POINTS": "Pts"})

st.divider()

