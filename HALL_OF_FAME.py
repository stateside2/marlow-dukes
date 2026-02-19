
import pandas as pd
import streamlit as st
import streamlit_antd_components as sac


excel_file_hof: str = "data/hall_of_fame.xlsx"
excel_file_season: str = "data/latest_data.xlsx"

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

# --- MENU BUTTONS
hof_selection = sac.buttons(
   items=[
    sac.ButtonsItem(label="All-time League Table", icon="bar-chart-fill"),
    sac.ButtonsItem(label="All-time Goals", icon="bar-chart-fill"), #--- 1.4
    sac.ButtonsItem(label="All-time MOTM Votes", icon="bar-chart-fill"), #--- 1.4
    sac.ButtonsItem(label="All-time Appearances", icon="bar-chart-fill"),
    sac.ButtonsItem(label="All-time Wins", icon=None),
    sac.ButtonsItem(label="All-time Draws", icon=None),
    sac.ButtonsItem(label="All-time Losses", icon="bar-chart-fill"),
    sac.ButtonsItem(label="All-time Goal Difference", icon=None),
    sac.ButtonsItem(label="All-time Win Ratio", icon=None),
    sac.ButtonsItem(label="All-time Loss Ratio", icon=None),
    sac.ButtonsItem(label="All-time Points per Match", icon=None),
    sac.ButtonsItem(label="Previous Podiums", icon=None),
], label=None, format_func=None, align="center", size="xs", radius="2", color="#4682b4", use_container_width=True)


# --- ALL-TIME TABLE BUILD FUNCTION
@st.cache_data
def df_at_full_tab_build() -> None:
	miss_rows: list[int] = [0,1,3]
	df_season_full_tab = pd.read_excel(excel_file_season, skiprows=miss_rows, nrows=35, sheet_name='League Table', usecols=[0,51,52,53,54,55,56]) # --- DROP POSITION COLUMN
	df_hof_full_tab = pd.read_excel(excel_file_hof, sheet_name="ALL TIME TABLE", skiprows=[0], usecols=[1,2,3,4,5,6,7,8,9])
	df_at_full_tab = df_season_full_tab.join(df_hof_full_tab.set_index("PLAYER"), on="PLAYER", how="outer", lsuffix="_season", rsuffix="_hof")

	df_at_full_tab = df_at_full_tab.fillna(0)
	df_at_full_tab["PLAYED"] = (df_at_full_tab["PLAYED_season"]+df_at_full_tab["PLAYED_hof"])
	df_at_full_tab["WON"] = (df_at_full_tab["WON_season"]+df_at_full_tab["WON_hof"])
	df_at_full_tab["DRAWN"] = (df_at_full_tab["DRAWN_season"]+df_at_full_tab["DRAWN_hof"])
	df_at_full_tab["LOST"] = (df_at_full_tab["LOST_season"]+df_at_full_tab["LOST_hof"])
	df_at_full_tab["Pts"] = (df_at_full_tab["PTS_season"]+df_at_full_tab["PTS_hof"])
	df_at_full_tab["GD"] = (df_at_full_tab["G/D_season"]+df_at_full_tab["G/D_hof"])
	df_at_full_tab["WIN RATIO"] = (df_at_full_tab["WON"]/df_at_full_tab["PLAYED"])
	df_at_full_tab["LOSS RATIO"] = (df_at_full_tab["LOST"]/df_at_full_tab["PLAYED"])
	df_at_full_tab["PTS/MATCH"] = (df_at_full_tab["Pts"]/df_at_full_tab["PLAYED"])
	return df_at_full_tab
# ----
df_at_full_tab = df_at_full_tab_build()

#--- 1.4
@st.cache_data
def df_at_var_tab_build(sheet_name: str) -> None:
	if sheet_name == "Goals":
		df_season_goals_tab = pd.read_excel(excel_file_season, skiprows=[0,1,3], nrows=31, sheet_name='Goals', usecols=[0,52])
		df_hof_goals_tab = pd.read_excel(excel_file_hof, sheet_name="ALL TIME TABLE", skiprows=[0], usecols=[1,2,8])
		df_at_goals_tab = df_season_goals_tab.join(df_hof_goals_tab.set_index("PLAYER"), on="PLAYER", how="outer", lsuffix="_season", rsuffix="_hof")
		
		df_at_goals_tab = df_at_goals_tab.fillna(0)
		df_at_goals_tab["ALL-TIME GOALS"] = (df_at_goals_tab["TOTAL"]+df_at_goals_tab["GOALS"])
		return df_at_goals_tab

	elif sheet_name == "MOTM":
		df_season_MOTM_tab = pd.read_excel(excel_file_season, skiprows=0, nrows=20, sheet_name='MOTM', usecols=[0,52])
		df_hof_MOTM_tab = pd.read_excel(excel_file_hof, sheet_name="ALL TIME TABLE", skiprows=[0], usecols=[1,2,9])
		df_at_MOTM_tab = df_season_MOTM_tab.join(df_hof_MOTM_tab.set_index("PLAYER"), on="PLAYER", how="outer", lsuffix="_season", rsuffix="_hof")

		df_at_MOTM_tab = df_at_MOTM_tab.fillna(0)
		df_at_MOTM_tab["ALL-TIME VOTES"] = (df_at_MOTM_tab["VOTES"]+df_at_MOTM_tab["MOTM"])
		return df_at_MOTM_tab
# ---
df_at_goals_tab = df_at_var_tab_build("Goals")
df_at_MOTM_tab = df_at_var_tab_build("MOTM")
# ---

# --- RACE CHART LINK FUNCTION ---
def race_chart(button_name: str, target_link: str) -> None:
	sac.buttons(
   	items=[
    		sac.ButtonsItem(label=button_name, icon="bar-chart-fill", href=target_link),
    		], label=None, format_func=None, align="center", variant="filled", size="sm", radius="2", color="#4682b4", use_container_width=False)
# ---

# --- PODIUM PAGE TABLES BUILD FUNCTION ---
@st.cache_data
def podium_table_build(skip_row_list: list[int]) -> None:
	df_hof_podium = pd.read_excel(excel_file_hof, sheet_name="TOP3", skiprows=skip_row_list, nrows=3, usecols=[0,1,2,6,7])
	st.dataframe(df_hof_podium, width=None, height=142, use_container_width=True, hide_index=True, column_config={"PLAYED": "P", "POINTS": "Pts"})
# ---

# --- RATIO TABLE BUILD FUNCTION ---
@st.cache_data
def ratio_table_build(ratio: str, new_col_name: str) -> None:
	global df_at_full_tab
	df_at_full_tab = df_at_full_tab.sort_values(by=[ratio, "PLAYER"], ascending=[False, True])
	df_at_full_tab.insert(0, "POSITION", range(1, 1 + len(df_at_full_tab)))
	if ratio in ["WIN RATIO", "LOSS RATIO", "PTS/MATCH"]:
		df_at_full_tab = df_at_full_tab.style.format({ratio: "{:.3f}"})
	st.dataframe(df_at_full_tab, width=None, height=2335, use_container_width=True, hide_index=True, column_order=["POSITION","PLAYER",ratio], column_config={"POSITION": " ",ratio: new_col_name})
# ---


# --- PANDAS DATA FRAME SELECTION & DISPLAY ---

if hof_selection == "All-time League Table":
	race_chart("2012-23 POINTS RACE CHART", "https://public.flourish.studio/visualisation/18936682/")
	df_at_full_tab = df_at_full_tab.sort_values(by=["Pts", "GD"], ascending=[False, False])
	df_at_full_tab.insert(0, "POSITION", range(1, 1 + len(df_at_full_tab)))
	st.dataframe(df_at_full_tab, width=None, height=2400, use_container_width=True, hide_index=True, column_order=["POSITION","PLAYER","PLAYED","WON","DRAWN","LOST","GD","Pts"], column_config={"POSITION": " ","PLAYER": " ", "PLAYED": "P", "WON": "W", "DRAWN": "D", "LOST": "L"})
	
if hof_selection == "All-time Goals": #--- 1.4
	race_chart("2012-23 GOALS RACE CHART", "https://public.flourish.studio/visualisation/19245477/")
	df_at_goals_tab = df_at_goals_tab.sort_values(by=["ALL-TIME GOALS", "PLAYER"], ascending=[False, False])
	df_at_goals_tab.insert(0, "POSITION", range(1, 1 + len(df_at_goals_tab)))
	st.dataframe(df_at_goals_tab, width=None, height=2400, use_container_width=True, hide_index=True, column_order=["POSITION","PLAYER","ALL-TIME GOALS"], column_config={"POSITION": " ","ALL-TIME GOALS": "GOALS"})

if hof_selection == "All-time MOTM Votes": #--- 1.4
	race_chart("2012-23 MOTM RACE CHART", "https://public.flourish.studio/visualisation/19244438/")
	df_at_MOTM_tab = df_at_MOTM_tab.sort_values(by=["ALL-TIME VOTES", "PLAYER"], ascending=[False, False])
	df_at_MOTM_tab.insert(0, "POSITION", range(1, 1 + len(df_at_MOTM_tab)))
	st.dataframe(df_at_MOTM_tab, width=None, height=2245, use_container_width=True, hide_index=True, column_order=["POSITION","PLAYER","ALL-TIME VOTES"], column_config={"POSITION": " ","ALL-TIME VOTES": "VOTES"})

if hof_selection == "All-time Appearances":
	race_chart("2012-23 APPEARANCES RACE CHART", "https://public.flourish.studio/visualisation/18900148/")
	ratio_table_build("PLAYED", "APPEARANCES")
		
if hof_selection == "All-time Wins":
	ratio_table_build("WON", "WINS")
	
if hof_selection == "All-time Draws":
	ratio_table_build("DRAWN", "DRAWS")
	
if hof_selection == "All-time Losses":
	race_chart("2012-23 BIGGEST LOSER RACE CHART", "https://public.flourish.studio/visualisation/18921440/")
	ratio_table_build("LOST", "LOSSES")

if hof_selection == "All-time Goal Difference":
	ratio_table_build("GD", "GD")

if hof_selection == "All-time Win Ratio":
	ratio_table_build("WIN RATIO", "WIN RATIO")

if hof_selection == "All-time Loss Ratio":
	ratio_table_build("LOSS RATIO", "LOSS RATIO")

if hof_selection == "All-time Points per Match":
	ratio_table_build("PTS/MATCH", "PTS/MATCH")

if hof_selection == "Previous Podiums":
	podium_table_build(None)
	season: list[int] = range(2024,2011,-1) # --- NEED TO MODIFY FOR A NEW SEASON
	skip_row_list_max: int = 4
	for i in season:
		podium_table_build(range(0,skip_row_list_max))
		skip_row_list_max: int = skip_row_list_max + 4

st.divider()

