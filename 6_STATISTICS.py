
import pandas as pd
import streamlit as st
# from streamlit_option_menu import option_menu #--- NEEDED FOR THE FIRST NAVBAR
import streamlit_antd_components as sac #--- NEEDED FOR THE 2ND NAVBAR
import matplotlib #--- USED FOR THE COLOR GRADIENT ON THE PLAYER ANALYSIS TABLE
import numpy as np #--- USED FOR ABS() ON THE TOTP UP/DOWN ARROW
import sys
from variables import *

# --- SETTING THE PYTHON PATH SO THAT VARIABLES CAN BE IMPORTED FROM variables.py
sys.path.insert(0, "../")


excel_file = "data/latest_data.xlsx"
excel_file_prev: str = "data/latest_data_prev.xlsx"

# --- THIS IS NOW SET IN THE NAVIGATE.py PAGE
# st.set_page_config(page_title="Statistics", page_icon="images/marlowdukesicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

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
st.image("images/marlowdukesbannerSTATS.png", use_container_width="auto") # --- CREATE NEW BANNER FOR STATS PAGE
st.divider()

# --- MENU NAVBAR ---
stat_selection = sac.buttons(
   items=[
    sac.ButtonsItem(label="Full Table"),
    sac.ButtonsItem(label="Win Ratio"),
    sac.ButtonsItem(label="Loss Ratio"),
    sac.ButtonsItem(label="Points per match"),
    sac.ButtonsItem(label="Goals per match"),
    sac.ButtonsItem(label="MOTM votes per match"),
    #sac.ButtonsItem(label="Board Room visits per match"),
    sac.ButtonsItem(label="Player Analysis", icon="person-fill"),
], label=None, format_func=None, align="center", size="xs", radius=2, color="#4682b4", use_container_width=True)


miss_rows = [0,1,3,40,41]
# --- PANDAS DATA EXTRACTS ---
# --- FULL TABLE WITH TOTP UP/DOWN ARROW

# --- WEEK 5 UPDATE
#formguide_stat_cols=[0,50,51,52,53,54,55,56,(game_week-4),(game_week-3),(game_week-2),(game_week-1),game_week] #--- THIS WILL BREAK WHEN GAME_WEEK < 5

formguide_stat_cols=[0,50,51,52,53,54,55,56]
df_full_tab = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name='League Table', usecols=formguide_stat_cols)

# def form_guide(game_week):
# 	i = game_week - 4
# 	match = 5
# 	while i <= game_week:
# 		df_full_tab.loc[df_full_tab["WK "+str(i)] > 0, "WK-"+str(match)] = "🟢"
# 		df_full_tab.loc[df_full_tab["WK "+str(i)] < 0, "WK-"+str(match)] = "🔴"
# 		df_full_tab.loc[df_full_tab["WK "+str(i)] == 0, "WK-"+str(match)] = "⚪"
# 		df_full_tab.loc[df_full_tab["WK "+str(i)].isnull(), "WK-"+str(match)] = "➖"
# 		i = i + 1
# 		match = match - 1
# 	return

# form_guide(game_week)

# df_full_tab["FORM"] = df_full_tab["WK-1"]+"  "+df_full_tab["WK-2"]+df_full_tab["WK-3"]+df_full_tab["WK-4"]+df_full_tab["WK-5"]


# ----
# CREATING THE TOTP UP/DOWN COLUMN
# PULL THE PREVIOUS FULL TABLE, JOIN IT TO THE CURRENT FULL TABLE AND ADD THE TOTP_CHANGE/DELTA COLUMN
df_tab_prev = pd.read_excel(excel_file_prev, skiprows=miss_rows, sheet_name='League Table', usecols=[0,50])
df_full_tab = df_full_tab.join(df_tab_prev.set_index("PLAYER"), on="PLAYER", how="outer", lsuffix="_curr", rsuffix="_prev")
df_full_tab["TOTP_CHANGE"] = (df_full_tab["POSITION_prev"]-df_full_tab["POSITION_curr"])

# IDENTIFY UP OR DOWN ARROW TO USE
df_full_tab.loc[df_full_tab["TOTP_CHANGE"] > 0, "TOTP_DIR"] = "⬆"
df_full_tab.loc[df_full_tab["TOTP_CHANGE"] < 0, "TOTP_DIR"] = "⬇"

# IDENTIFY HOW MANY POSITIONS RISEN OR FALLEN AND MERGE WITH THE UP/DOWN ARROW
df_full_tab["TOTP_CHANGE_ABS"] = np.abs(df_full_tab["TOTP_CHANGE"])
df_full_tab.loc[df_full_tab["TOTP_CHANGE_ABS"] != 0, "TOTP_FINAL"] = df_full_tab["TOTP_DIR"] + df_full_tab["TOTP_CHANGE_ABS"].astype(str)
df_full_tab.loc[df_full_tab["TOTP_CHANGE_ABS"] == 0, "TOTP_FINAL"] = "➖"

df_full_tab = df_full_tab.sort_values(by=["POSITION_curr", "PLAYER"], ascending=[True, False])
df_full_tab.insert(0, "POSITION", range(1, 1 + len(df_full_tab)))

# ADD CONDITIONAL COLOR TO THE COLUMN
def totp_highlight(series):
	red = "color: #EA3323"
	green = "color: #75FB4C"
	grey = "color: grey"
	return [green if value.startswith("⬆") else red if value.startswith("⬇") else grey for value in series]
df_full_tab = df_full_tab.style.apply(totp_highlight, subset="TOTP_FINAL")
# ----

# --- APEARANCES --- NEEDED FOR RATIO STATS
df_appear = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,51])
df_appear = df_appear.sort_values(by=["PLAYED", "PLAYER"], ascending=[False, True])

# --- WIN RATIO
df_win_ratio = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,51,52])
df_win_ratio["WIN RATIO"] = (df_win_ratio["WON"]/df_win_ratio["PLAYED"])
df_win_ratio = df_win_ratio.drop("WON", axis=1)  # --- REMOVING COLUMNS FROM DISPLAY
df_win_ratio = df_win_ratio.sort_values(by=["WIN RATIO", "PLAYED"], ascending=[False, False])
df_win_ratio.insert(0, "POSITION", range(1, 1 + len(df_win_ratio)))
df_win_ratio = df_win_ratio.style.format({"WIN RATIO": "{:.3f}"})

# --- LOSS RATIO
df_loss_ratio = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,51,54])
df_loss_ratio["LOSS RATIO"] = (df_loss_ratio["LOST"]/df_loss_ratio["PLAYED"])
df_loss_ratio = df_loss_ratio.drop("LOST", axis=1)  # --- REMOVING COLUMNS FROM DISPLAY
df_loss_ratio = df_loss_ratio.sort_values(by=["LOSS RATIO", "PLAYED"], ascending=[False, False])
df_loss_ratio.insert(0, "POSITION", range(1, 1 + len(df_loss_ratio)))
df_loss_ratio = df_loss_ratio.style.format({"LOSS RATIO": "{:.3f}"})


# --- POINTS/MATCH
df_pts_match = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,51,55])
df_pts_match["PTS/MATCH"] = (df_pts_match["PTS"]/df_pts_match["PLAYED"])
df_pts_match = df_pts_match.drop("PTS", axis=1)  # --- REMOVING COLUMNS FROM DISPLAY
df_pts_match = df_pts_match.sort_values(by=["PTS/MATCH", "PLAYED"], ascending=[False, False])
df_pts_match.insert(0, "POSITION", range(1, 1 + len(df_pts_match)))
df_pts_match = df_pts_match.style.format({"PTS/MATCH": "{:.3f}"})


# --- GOALS/MATCH
#df_goal_appear = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,54])
df_goals = pd.read_excel(excel_file, skiprows=[0,1,3,37,38,39,40], sheet_name="Goals", usecols=[0,52])
df_goals_match = df_appear.join(df_goals.set_index("PLAYER"), on="PLAYER") #--- JOINING 2 DATAFRAMES (USING DF_APPEAR FROM ABOVE)
df_goals_match = df_goals_match.fillna(0) #--- FILL ALL NULL VALUES WITH ZERO
df_goals_match["GOALS/MATCH"] = (df_goals_match["TOTAL"]/df_goals_match["PLAYED"])
df_goals_match = df_goals_match.drop("TOTAL", axis=1)  # --- REMOVING COLUMNS FROM DISPLAY
df_goals_match = df_goals_match.sort_values(by=["GOALS/MATCH", "PLAYED"], ascending=[False, False])

df_goals_anal = df_goals_match.drop("PLAYED", axis=1) #--- DROPPING THE PLAYED COLUMN SO THE DATAFRAME CAN BE USED IN THE PLAYER ANALYSIS DATAFRAME BELOW
df_goals_match.insert(0, "POSITION", range(1, 1 + len(df_goals_match)))
df_goals_match = df_goals_match.style.format({"GOALS/MATCH": "{:.3f}"})



# --- MOTM VOTES/MATCH
df_motm = pd.read_excel(excel_file, skiprows=[1,35,36,37,38,39], sheet_name='MOTM', usecols=[0,52])
df_MOTM_match = df_appear.join(df_motm.set_index("PLAYER"), on="PLAYER")
df_MOTM_match = df_MOTM_match.fillna(0) #--- FILL ALL NULL VALUES WITH ZERO
df_MOTM_match["VOTES/MATCH"] = (df_MOTM_match["VOTES"]/df_MOTM_match["PLAYED"])
df_MOTM_match = df_MOTM_match.drop("VOTES", axis=1)  # --- REMOVING COLUMNS FROM DISPLAY
df_MOTM_match = df_MOTM_match.sort_values(by=["VOTES/MATCH", "PLAYED"], ascending=[False, False])
df_MOTM_match.insert(0, "POSITION", range(1, 1 + len(df_MOTM_match)))
df_MOTM_match = df_MOTM_match.style.format({"VOTES/MATCH": "{:.3f}"})


# --- BOARD ROOM/MATCH
#df_broom = pd.read_excel(excel_file, skiprows=7, nrows=19, sheet_name="Board Room", usecols=[12,13])
#df_broom["Unnamed: 12"] = df_broom["Unnamed: 12"].str.upper() # --- NEEDS TO UPPER HERE FOR THE JOIN COLUMN MATCH
#df_broom_match = df_broom.set_index("Unnamed: 12").join(df_appear.set_index("PLAYER"), lsuffix="left", rsuffix="right")

#df_broom_match = pd.merge(df_broom, df_appear, how="left", on=["Unnamed: 12","PLAYER"])
#df_broom_match = pd.concat([df_broom,df_appear], axis=1)

# --- PLAYER ANALYSIS
df_result_like = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,51,52,53,54])
df_result_like["WIN %"] = (df_result_like["WON"]/df_result_like["PLAYED"])
df_result_like["DRAW %"] = (df_result_like["DRAWN"]/df_result_like["PLAYED"])
df_result_like["LOSS %"] = (df_result_like["LOST"]/df_result_like["PLAYED"])
df_play_anal = df_result_like.join(df_goals_anal.set_index("PLAYER"), on="PLAYER") #--- JOINING GOALS/MATCH TO INCLUDE GOAL RATIO
df_play_anal = df_play_anal.drop(["WON","DRAWN","LOST"], axis=1) # --- REMOVING UNECESSARY COLUMNS FROM DISPLAY
df_play_anal = df_play_anal.sort_values(by="PLAYER", ascending=True)

df_play_anal = df_play_anal.style.background_gradient(cmap="Greens", subset="WIN %")\
.background_gradient(cmap="Greens_r", subset="LOSS %")\
.format({"WIN %": "{:.3f}", "DRAW %": "{:.3f}", "LOSS %": "{:.3f}", "GOALS/MATCH": "{:.3f}"})  #--- IMPORT MATPLOTLIB


frame_size = 1300
# --- STREAMLIT DATAFRAME SELECTION ---
if stat_selection == "Full Table":
	st.dataframe(df_full_tab, width=None, height=frame_size, use_container_width=True, hide_index=True, column_order=["POSITION","TOTP_FINAL","PLAYER","PLAYED","WON","DRAWN","LOST","G/D","PTS","FORM"], column_config={"POSITION": " ", "TOTP_FINAL": " ", "PLAYER": " ", "PLAYED": "P", "WON": "W", "DRAWN": "D", "LOST": "L", "G/D": "GD", "PTS": "Pts"})

if stat_selection == "Win Ratio":
	st.dataframe(df_win_ratio, width=None, height=frame_size, use_container_width=True, hide_index=True, column_config={"POSITION": " "})

if stat_selection == "Loss Ratio":
	st.dataframe(df_loss_ratio, width=None, height=frame_size, use_container_width=True, hide_index=True, column_config={"POSITION": " "})

if stat_selection == "Points per match":
	st.dataframe(df_pts_match, width=None, height=frame_size, use_container_width=True, hide_index=True, column_config={"POSITION": " "})

if stat_selection == "Goals per match":
	st.dataframe(df_goals_match, width=None, height=frame_size, use_container_width=True, hide_index=True, column_config={"POSITION": " "})

if stat_selection == "MOTM votes per match":
	st.dataframe(df_MOTM_match, width=None, height=frame_size, use_container_width=True, hide_index=True, column_config={"POSITION": " "})

#if stat_selection == "Board Room visits per match":
#	st.dataframe(df_broom_match, width=None, height=frame_size, use_container_width=True, hide_index=True)

if stat_selection == "Player Analysis":
	st.caption("For WIN % and LOSS % the darker the green the better. Click on column headers to sort.")
	st.dataframe(df_play_anal, width=None, height=frame_size, use_container_width=True, hide_index=True, column_order=["PLAYER","WIN %","DRAW %","LOSS %","GOALS/MATCH","PLAYED"])

st.divider()


# --- FUTURE ADDITIONS
# st.markdown("##")
# st.snow() # --- WINTER / XMAS UPDATE --- DOES IT WORK ON CELLPHONE?
# st.balloons() # --- END OF SEASON CELEBRATION --- DOES IT WORK ON CELLPHONE?
# st.toast("xxxxxxx is the winner", icon="🔥") # --- WINNER ANNOUNCEMENT --- DOES IT WORK ON CELLPHONE?
# time.sleep(1) --- ALSO HAVE TO import time

# st.title("Title Marlow Dukes") --- st.header("This is a header") --- st.subheader("Sub Header") --- st.markdown("data correct as of ...")

# col_list=df_broom.columns
# st.markdown(col_list)

#.map("{:,.3f}".format)

# MODIFYING A COLUMN WIDTH (small, medium or large)
# "WON": st.column_config.Column(width="small"), 
