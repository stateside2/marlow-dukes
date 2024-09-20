

import pandas as pd
import streamlit as st
import streamlit_antd_components as sac #--- NEEDED FOR THE 2ND NAVBAR
import time # --- USED IN THE miles_notif NOTIFICATION FUNCTION

excel_file_season: str = "data/latest_data.xlsx"
excel_file_hof: str = "data/hall_of_fame.xlsx" # --- NEEDED FOR THE miles_notif NOTIFICATION FUNCTION


st.set_page_config(page_title="Marlow Dukes", page_icon="images/marlowdukesicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

# --- HIDE STREAMLIT HEADER/FOOTER MENUS ---
hide_st_style = """ 
	<style>MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} 
	[data-testid="stElementToolbar"] {display: none;} 
	button[title="View fullscreen"] {visibility: hidden;} 
	</style>
	"""
st.markdown(hide_st_style, unsafe_allow_html=True)
# ----

# --- BANNER IMAGE
st.image("images/marlowdukesbanner.png", use_column_width="auto")
#st.success("Congratulation to the 2023 WINNERS!!", icon=None)
#st.success("League: xxx, Goals: xxx, MOTM: xxx, Board Room: xxx", icon=None)
st.divider()

# st.write("Week 16 - 23/4/2024")
File_Date = "Week 38 - 18th September 2024"


# --- MENU NAVBAR --- 
menu_selection = sac.buttons(
   items=[
    	sac.ButtonsItem(label="League Table", icon="trophy-fill"),
    	sac.ButtonsItem(label="Goals", icon="life-preserver"),
    	sac.ButtonsItem(label="MOTM", icon="person-arms-up"),
    	sac.ButtonsItem(label="Board Room", icon="bank"),
], label=File_Date, format_func=None, align="center", size="md", radius="md", color="#4682b4", use_container_width=True)
# ---


# --- PANDAS DATA FRAME SELECTION ---
df_ltable = pd.read_excel(excel_file_season, skiprows=[0,1,3,39,40], sheet_name='League Table', usecols=[0,52,54,58,59])

df_goals = pd.read_excel(excel_file_season, skiprows=[0,1,3,37,38,39,40], sheet_name='Goals', usecols=[0,52])
df_goals = df_goals.sort_values(by=["TOTAL", "PLAYER"], ascending=[False, True])

df_motm = pd.read_excel(excel_file_season, skiprows=[1,35,36,37,38,39], sheet_name='MOTM', usecols=[0,52])
df_motm = df_motm.sort_values(by=["VOTES", "PLAYER"], ascending=[False, True])

df_broom = pd.read_excel(excel_file_season, skiprows=7, nrows=19, sheet_name='Board Room', usecols=[12,13]).fillna(0)
df_broom["Unnamed: 12"] = df_broom["Unnamed: 12"].str.upper() # --- MAKES THE BOARD ROOM PLAYER COLUMN UPPER CASE ---
df_broom = df_broom.sort_values(by=["Unnamed: 13", "Unnamed: 12"], ascending=[False, True])


# ---  MENU SELECTION AND DF DISPLAY
if menu_selection == "League Table":
	st.dataframe(df_ltable, width=None, height=1275, use_container_width=True, hide_index=True, column_order=["POSITION","PLAYER","PLAYED","G/D","PTS"], column_config={"POSITION": " ", "PLAYED": "P", "G/D": "GD", "PTS": "Pts"})

	# --- MILESTONE NOTIFICATION FUNCTION ---
	def miles_notif(col_metric: str) -> str:
		# --- ALL-TIME DATAFRAME BUILD FOR NOTIFICATION FUNCTION
		miss_rows: list[int] = [0,1,3,39,40]
		df_season_full_tab = pd.read_excel(excel_file_season, skiprows=miss_rows, sheet_name='League Table', usecols=[0,54,55,56,57,58,59]) # --- DROP POSITION COLUMN
		df_hof_full_tab = pd.read_excel(excel_file_hof, sheet_name="ALL TIME TABLE", skiprows=[0], usecols=[1,2,3,4,5,6,7])
		df_at_full_tab = df_season_full_tab.join(df_hof_full_tab.set_index("PLAYER"), on="PLAYER", how="outer", lsuffix="_season", rsuffix="_hof")
		df_at_full_tab = df_at_full_tab.fillna(0)
		df_at_full_tab["PLAYED"] = (df_at_full_tab["PLAYED_season"]+df_at_full_tab["PLAYED_hof"])
		df_at_full_tab["WON"] = (df_at_full_tab["WON_season"]+df_at_full_tab["WON_hof"])
		df_at_full_tab["LOST"] = (df_at_full_tab["LOST_season"]+df_at_full_tab["LOST_hof"])
		# ---
		# --- PLAYER AND MESSAGE NOTIFICATION
		milestones: list[int] = range(50, 601, 50)
		mst_name: str = df_at_full_tab[df_at_full_tab[col_metric].isin(milestones)]["PLAYER"].tolist()
		number: int = df_at_full_tab[df_at_full_tab["PLAYER"].isin(mst_name)][col_metric].tolist()
		for mst_name, number in zip(mst_name, number):
			if col_metric == "PLAYED":
				st.toast(f"Congratulations, {mst_name} ... {number:.0f} all-time appearances!", icon="⭐")
				time.sleep(2)
			if col_metric == "LOST":
				st.toast(f"UH-OH {mst_name} ... {number:.0f} all-time losses.", icon="❗")
				time.sleep(2)
			if col_metric == "WON":
				st.toast(f"Congratulations, {mst_name} ... {number:.0f} all-time wins!", icon="🏅")

	miles_notif(col_metric = "PLAYED")
	miles_notif(col_metric = "LOST")
	miles_notif(col_metric = "WON")

if menu_selection == "Goals":
	st.dataframe(df_goals, width=None, height=1225, use_container_width=True, hide_index=True, column_config={"TOTAL": "GOALS"})
if menu_selection == "MOTM":
	st.dataframe(df_motm, width=None, height=1225, use_container_width=True, hide_index=True)
if menu_selection == "Board Room":
	st.dataframe(df_broom, width=None, height=750, use_container_width=True, hide_index=True, column_config={"Unnamed: 12": "PLAYER", "Unnamed: 13": "VISITS"})


st.divider()

# --- FUTURE ADDITIONS
# st.markdown("##")
# st.snow() # --- WINTER / XMAS UPDATE --- DOES IT WORK ON CELLPHONE?
# st.balloons() # --- END OF SEASON CELEBRATION --- DOES IT WORK ON CELLPHONE?
# st.toast("xxxxxxx is the winner", icon="🔥") # --- WINNER ANNOUNCEMENT --- DOES IT WORK ON CELLPHONE?
# time.sleep(1) --- ALSO HAVE TO import time
# POSSIBLE ICONS = [🔥, 🚨, 💩, 💥, 🔆, 😎, 😖, 😟, 🥇, 🏅, ☠️, ⚠️, ⚽, ⭐, 💯, ✅, ❗, 🏆]

# st.title("Title Marlow Dukes") --- st.header("This is a header") --- st.subheader("Sub Header") --- st.markdown("data correct as of ...")

