
import pandas as pd
import streamlit as st
# from streamlit_option_menu import option_menu #--- NEEDED FOR THE FIRST NAVBAR
import streamlit_antd_components as sac #--- NEEDED FOR THE 2ND NAVBAR
import matplotlib #--- USED FOR THE COLOR GRADIENT ON THE PLAYER ANALYSIS TABLE

excel_file = "data/latest_data.xlsx"
st.set_page_config(page_title="Statistics", page_icon="images/marlowdukesicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

# --- HIDE STREAMLIT HEADER/FOOTER MENUS ---
hide_st_style = """ 
	<style>MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>
	"""
st.markdown(hide_st_style, unsafe_allow_html=True)
# ----

# --- BANNER IMAGE
st.image("images/marlowdukesbannerSTATS.png", use_column_width="auto") # --- CREATE NEW BANNER FOR STATS PAGE
st.divider()

# --- MENU NAVBAR ---
stat_selection = sac.buttons(
   items=[
    sac.ButtonsItem(label="Most Appearances"),
    sac.ButtonsItem(label="Most Wins"),
    sac.ButtonsItem(label="Most Draws"),
    sac.ButtonsItem(label="Most Losses"),
    sac.ButtonsItem(label="Best Goal Difference"),
    sac.ButtonsItem(label="Win Ratio"),
    sac.ButtonsItem(label="Loss Ratio"),
    sac.ButtonsItem(label="Points per match"),
    sac.ButtonsItem(label="Goals per match"),
    sac.ButtonsItem(label="MOTM votes per match"),
    sac.ButtonsItem(label="Full Table"),
    #sac.ButtonsItem(label="Board Room visits per match"),
    sac.ButtonsItem(label="Player Analysis"),
], label=None, format_func=None, align="center", size="xs", radius=2, color="#4682b4", use_container_width=True)


miss_rows = [0,1,3,39,40]
# --- PANDAS DATA EXTRACTS ---
# --- APEARANCES
df_appear = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,54])
df_appear = df_appear.sort_values(by=["PLAYED", "PLAYER"], ascending=[False, True])

# --- MOST WINS
df_wins = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,55])
df_wins = df_wins.sort_values(by=["WON", "PLAYER"], ascending=[False, True])

# --- MOST DRAWS
df_draws = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,56])
df_draws = df_draws.sort_values(by=["DRAWN", "PLAYER"], ascending=[False, True])

# --- MOST LOSSES
df_losses = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,57])
df_losses = df_losses.sort_values(by=["LOST", "PLAYER"], ascending=[False, True])

# --- BEST GOAL DIFFERENCE
df_goal_diff = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,59])
df_goal_diff = df_goal_diff.sort_values(by=["G/D", "PLAYER"], ascending=[False, True])

# --- WIN RATIO
df_win_ratio = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,54,55])
df_win_ratio["WIN RATIO"] = (df_win_ratio["WON"]/df_win_ratio["PLAYED"])
df_win_ratio = df_win_ratio.drop("WON", axis=1)  # --- REMOVING COLUMNS FROM DISPLAY
df_win_ratio = df_win_ratio.sort_values(by=["WIN RATIO", "PLAYED"], ascending=[False, False])
df_win_ratio = df_win_ratio.style.format({"WIN RATIO": "{:.3f}"})

# --- LOSS RATIO
df_loss_ratio = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,54,57])
df_loss_ratio["LOSS RATIO"] = (df_loss_ratio["LOST"]/df_loss_ratio["PLAYED"])
df_loss_ratio = df_loss_ratio.drop("LOST", axis=1)  # --- REMOVING COLUMNS FROM DISPLAY
df_loss_ratio = df_loss_ratio.sort_values(by=["LOSS RATIO", "PLAYED"], ascending=[False, False])
df_loss_ratio = df_loss_ratio.style.format({"LOSS RATIO": "{:.3f}"})

# --- POINTS/MATCH
df_pts_match = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,54,58])
df_pts_match["PTS/MATCH"] = (df_pts_match["PTS"]/df_pts_match["PLAYED"])
df_pts_match = df_pts_match.drop("PTS", axis=1)  # --- REMOVING COLUMNS FROM DISPLAY
df_pts_match = df_pts_match.sort_values(by=["PTS/MATCH", "PLAYED"], ascending=[False, False])
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
df_goals_match = df_goals_match.style.format({"GOALS/MATCH": "{:.3f}"})


# --- MOTM VOTES/MATCH
df_motm = pd.read_excel(excel_file, skiprows=[1,35,36,37,38,39], sheet_name='MOTM', usecols=[0,52])
df_MOTM_match = df_appear.join(df_motm.set_index("PLAYER"), on="PLAYER")
df_MOTM_match = df_MOTM_match.fillna(0) #--- FILL ALL NULL VALUES WITH ZERO
df_MOTM_match["VOTES/MATCH"] = (df_MOTM_match["VOTES"]/df_MOTM_match["PLAYED"])
df_MOTM_match = df_MOTM_match.drop("VOTES", axis=1)  # --- REMOVING COLUMNS FROM DISPLAY
df_MOTM_match = df_MOTM_match.sort_values(by=["VOTES/MATCH", "PLAYED"], ascending=[False, False])
df_MOTM_match = df_MOTM_match.style.format({"VOTES/MATCH": "{:.3f}"})

# --- BOARD ROOM/MATCH
#df_broom = pd.read_excel(excel_file, skiprows=7, nrows=19, sheet_name="Board Room", usecols=[12,13])
#df_broom["Unnamed: 12"] = df_broom["Unnamed: 12"].str.upper() # --- NEEDS TO UPPER HERE FOR THE JOIN COLUMN MATCH
#df_broom_match = df_broom.set_index("Unnamed: 12").join(df_appear.set_index("PLAYER"), lsuffix="left", rsuffix="right")

#df_broom_match = pd.merge(df_broom, df_appear, how="left", on=["Unnamed: 12","PLAYER"])
#df_broom_match = pd.concat([df_broom,df_appear], axis=1)

# --- FULL TABLE
df_full_tab = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name='League Table', usecols=[0,52,54,55,56,57,58,59])

# --- PLAYER ANALYSIS
df_result_like = pd.read_excel(excel_file, skiprows=miss_rows, sheet_name="League Table", usecols=[0,54,55,56,57])
df_result_like["WIN %"] = (df_result_like["WON"]/df_result_like["PLAYED"])
df_result_like["DRAW %"] = (df_result_like["DRAWN"]/df_result_like["PLAYED"])
df_result_like["LOSS %"] = (df_result_like["LOST"]/df_result_like["PLAYED"])
df_play_anal = df_result_like.join(df_goals_anal.set_index("PLAYER"), on="PLAYER") #--- JOINING GOALS/MATCH TO INCLUDE GOAL RATIO
df_play_anal = df_play_anal.drop(["WON","DRAWN","LOST"], axis=1) # --- REMOVING UNECESSARY COLUMNS FROM DISPLAY
df_play_anal = df_play_anal.sort_values(by="PLAYER", ascending=True)

df_play_anal = df_play_anal.style.background_gradient(cmap="Greens", subset="WIN %")\
.background_gradient(cmap="Greens_r", subset="LOSS %")\
.format({"WIN %": "{:.3f}", "DRAW %": "{:.3f}", "LOSS %": "{:.3f}", "GOALS/MATCH": "{:.3f}"})  #--- IMPORT MATPLOTLIB


frame_size = 1275
# --- STREAMLIT DATAFRAME SELECTION ---
if stat_selection == "Most Appearances":
	st.dataframe(df_appear, width=None, height=frame_size, use_container_width=True, hide_index=True, column_config={"PLAYED": "APPEARANCES"})

if stat_selection == "Most Wins":
	st.dataframe(df_wins, width=None, height=frame_size, use_container_width=True, hide_index=True, column_config={"WON": "WINS"})

if stat_selection == "Most Draws":
   st.dataframe(df_draws, width=None, height=frame_size, use_container_width=True, hide_index=True, column_config={"DRAWN": "DRAWS"})

if stat_selection == "Most Losses":
	st.dataframe(df_losses, width=None, height=frame_size, use_container_width=True, hide_index=True, column_config={"LOST": "LOSSES"})

if stat_selection == "Best Goal Difference":
	st.dataframe(df_goal_diff, width=None, height=frame_size, use_container_width=True, hide_index=True, column_config={"G/D": "GD"})

if stat_selection == "Win Ratio":
	st.dataframe(df_win_ratio, width=None, height=frame_size, use_container_width=True, hide_index=True)

if stat_selection == "Loss Ratio":
	st.dataframe(df_loss_ratio, width=None, height=frame_size, use_container_width=True, hide_index=True)

if stat_selection == "Points per match":
	st.dataframe(df_pts_match, width=None, height=frame_size, use_container_width=True, hide_index=True)

if stat_selection == "Goals per match":
	st.dataframe(df_goals_match, width=None, height=frame_size, use_container_width=True, hide_index=True)

if stat_selection == "MOTM votes per match":
	st.dataframe(df_MOTM_match, width=None, height=frame_size, use_container_width=True, hide_index=True)

#if stat_selection == "Board Room visits per match":
#	st.dataframe(df_broom_match, width=None, height=frame_size, use_container_width=True, hide_index=True)

if stat_selection == "Full Table":
	st.dataframe(df_full_tab, width=None, height=frame_size, use_container_width=True, hide_index=True, column_order=["POSITION","PLAYER","PLAYED","WON","DRAWN","LOST","G/D","PTS"], column_config={"POSITION": " ", "PLAYER": " ", "PLAYED": "P", "WON": "W", "DRAWN": "D", "LOST": "L", "G/D": "GD", "PTS": "Pts"})

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
