
import pandas as pd
import streamlit as st
import streamlit_antd_components as sac #--- NEEDED FOR THE NAVBAR
import time # --- USED IN THE miles_notif NOTIFICATION FUNCTION
import numpy as np #--- USED FOR ABS() ON THE TOTP UP/DOWN ARROW
from variables import *

excel_file_season: str = "data/latest_data.xlsx"
excel_file_prev: str = "data/latest_data_prev.xlsx"
excel_file_hof: str = "data/hall_of_fame.xlsx" # --- NEEDED FOR THE miles_notif NOTIFICATION FUNCTION

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
st.image("images/marlowdukesbanner.png", use_container_width="auto")
#st.success("Congratulation to the 2023 WINNERS!!", icon=None)
#st.success("League: xxx, Goals: xxx, MOTM: xxx, Board Room: xxx", icon=None)
st.divider()

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
# --- HOME/LEAGUE TABLE DF BUILD

# --- WEEK5UPDATE --- REMOVED UNTIL WEEK 5
# formguide_home_cols=[0,52,54,58,59,(game_week-4),(game_week-3),(game_week-2),(game_week-1),game_week] #--- THIS WILL BREAK WHEN GAME_WEEK < 5

formguide_home_cols=[0,50,51,55,56]
df_ltable = pd.read_excel(excel_file_season, skiprows=[0,1,3,40,41], sheet_name='League Table', usecols=formguide_home_cols)

# --- WEEK5UPDATE --- REMOVED UNTIL WEEK 5
# def form_guide_league(game_week):
# 	i = game_week - 4
# 	match = 5
# 	while i <= game_week:
# 		df_ltable.loc[df_ltable["WK "+str(i)] > 0, "WK-"+str(match)] = "🟢"
# 		df_ltable.loc[df_ltable["WK "+str(i)] < 0, "WK-"+str(match)] = "🔴"
# 		df_ltable.loc[df_ltable["WK "+str(i)] == 0, "WK-"+str(match)] = "⚪"
# 		df_ltable.loc[df_ltable["WK "+str(i)].isnull(), "WK-"+str(match)] = "➖"
# 		i = i + 1
# 		match = match - 1
# 	return
	
# form_guide_league(game_week)

# df_ltable["FORM"] = df_ltable["WK-1"]+"  "+df_ltable["WK-2"]+df_ltable["WK-3"]+df_ltable["WK-4"]+df_ltable["WK-5"]
# ----

# ----
# CREATING THE TOTP UP/DOWN COLUMN
# PULL THE PREVIOUS FULL TABLE, JOIN IT TO THE CURRENT FULL TABLE AND ADD THE TOTP_CHANGE/DELTA COLUMN
df_tab_prev = pd.read_excel(excel_file_prev, skiprows=[0,1,3,40,41], sheet_name='League Table', usecols=[0,50])
df_ltable = df_ltable.join(df_tab_prev.set_index("PLAYER"), on="PLAYER", how="outer", lsuffix="_curr", rsuffix="_prev")
df_ltable["TOTP_CHANGE"] = (df_ltable["POSITION_prev"]-df_ltable["POSITION_curr"])

# IDENTIFY UP OR DOWN ARROW TO USE
df_ltable.loc[df_ltable["TOTP_CHANGE"] > 0, "TOTP_DIR"] = "⬆"
df_ltable.loc[df_ltable["TOTP_CHANGE"] < 0, "TOTP_DIR"] = "⬇"

# IDENTIFY HOW MANY POSITIONS RISEN OR FALLEN AND MERGE WITH THE UP/DOWN ARROW
df_ltable["TOTP_CHANGE_ABS"] = np.abs(df_ltable["TOTP_CHANGE"])
df_ltable.loc[df_ltable["TOTP_CHANGE_ABS"] != 0, "TOTP_FINAL"] = df_ltable["TOTP_DIR"] + df_ltable["TOTP_CHANGE_ABS"].astype(str)
df_ltable.loc[df_ltable["TOTP_CHANGE_ABS"] == 0, "TOTP_FINAL"] = "➖"

df_ltable = df_ltable.sort_values(by=["POSITION_curr", "PLAYER"], ascending=[True, False])
df_ltable.insert(0, "POSITION", range(1, 1 + len(df_ltable)))


# ADD CONDITIONAL COLOR TO THE TOTP COLUMN
def totp_highlight(series):
	red = "color: #EA3323"
	green = "color: #75FB4C"
	grey = "color: grey"
	return [green if value.startswith("⬆") else red if value.startswith("⬇") else grey for value in series]
df_ltable = df_ltable.style.apply(totp_highlight, subset="TOTP_FINAL")
# ----


# ---  MENU SELECTION AND DF DISPLAY
if menu_selection == "League Table":
	st.dataframe(df_ltable, width=None, height=1300, use_container_width=True, hide_index=True, column_order=["POSITION","TOTP_FINAL","PLAYER","PLAYED","G/D","PTS","FORM"], column_config={"POSITION": " ", "TOTP_FINAL": " ", "PLAYED": "P", "G/D": "GD", "PTS": "Pts"})

	# --- MILESTONE NOTIFICATION FUNCTION ---
	def miles_notif(col_metric: str) -> str:
		# --- ALL-TIME DATAFRAME BUILD FOR NOTIFICATION FUNCTION
		miss_rows: list[int] = [0,1,3,39,40]
		df_season_full_tab = pd.read_excel(excel_file_season, skiprows=miss_rows, sheet_name='League Table', usecols=[0,50,51,52,53,54,55]) # --- DROP POSITION COLUMN
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


# ---- GOALS DF BUILD
df_goals = pd.read_excel(excel_file_season, skiprows=[0,1,3,37,38,39,40], sheet_name='Goals', usecols=[0,52])
df_goals = df_goals.sort_values(by=["TOTAL", "PLAYER"], ascending=[False, True])
df_goals.insert(0, "POSITION", range(1, 1 + len(df_goals)))

# ---- MOTM DF BUILD
df_motm = pd.read_excel(excel_file_season, skiprows=[1,35,36,37,38,39], sheet_name='MOTM', usecols=[0,52])
df_motm = df_motm.sort_values(by=["VOTES", "PLAYER"], ascending=[False, True])
df_motm.insert(0, "POSITION", range(1, 1 + len(df_motm)))

# ---- BOARDROOM DF BUILD
df_broom = pd.read_excel(excel_file_season, skiprows=7, nrows=22, sheet_name='Board Room', usecols=[12,13]).fillna(0)
df_broom["Unnamed: 12"] = df_broom["Unnamed: 12"].str.upper() # --- MAKES THE BOARD ROOM PLAYER COLUMN UPPER CASE ---
df_broom = df_broom.sort_values(by=["Unnamed: 13", "Unnamed: 12"], ascending=[False, True])
df_broom.insert(0, "POSITION", range(1, 1 + len(df_broom)))


if menu_selection == "Goals":
	st.dataframe(df_goals, width=None, height=1225, use_container_width=True, hide_index=True, column_config={"POSITION": " ","TOTAL": "GOALS"})

if menu_selection == "MOTM":
	st.dataframe(df_motm, width=None, height=1225, use_container_width=True, hide_index=True, column_config={"POSITION": " "})
if menu_selection == "Board Room":
	st.dataframe(df_broom, width=None, height=185, use_container_width=True, hide_index=True, column_config={"POSITION": " ","Unnamed: 12": "PLAYER", "Unnamed: 13": "VISITS"})

st.divider()

# --- FUTURE ADDITIONS
# st.markdown("##")
# st.snow() # --- WINTER / XMAS UPDATE --- DOES IT WORK ON CELLPHONE?
# st.balloons() # --- END OF SEASON CELEBRATION --- DOES IT WORK ON CELLPHONE?
# st.toast("xxxxxxx is the winner", icon="🔥") # --- WINNER ANNOUNCEMENT --- DOES IT WORK ON CELLPHONE?
# time.sleep(1) --- ALSO HAVE TO import time
# POSSIBLE ICONS = [🔥, 🚨, 💩, 💥, 🔆, 😎, 😖, 😟, 🥇, 🏅, ☠️, ⚠️, ⚽, ⭐, 💯, ✅, ❗, 🏆]

# st.title("Title Marlow Dukes") --- st.header("This is a header") --- st.subheader("Sub Header") --- st.markdown("data correct as of ...")

# MODIFYING A COLUMN WIDTH (small, medium or large)
# "WON": st.column_config.Column(width="small"), 
