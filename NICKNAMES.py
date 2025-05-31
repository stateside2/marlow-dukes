
import streamlit as st


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
st.divider()


nickname_data = [["CARL", "CARLOS, CARLITO, SMUDGE"], 
["CHRIS", "POSH"], 
["COLIN", "DWARF"], 
["DAN", "INSPECTOR GADGET"], 
["DAVID C", "CARZOLA"], 
["DAVID M", "DOGGER"], 
["DAVID T", "PRESTON"], 
["EMIN", "CAPTAIN KIRK"], 
["ESPEN", "FLO"], 
["MARK L", "ARTIST"], 
["MATT B", "KRYTON"], 
["MICK", "DITCH"], 
["MO", "KERMIT"], 
["PHIL M", "FATHER TED"], 
["PHIL S", "FRED"], 
["ROB G", "ZIGZAG"], 
["ROB O", "STRAIGHT ROB"], 
["STEVE P", "TOY BOY"], 
["TERRY", "STEPTOE"], 
["TONY", "ELBOW"]]


st.dataframe(nickname_data, width=None, height=750, use_container_width=True, hide_index=True, column_config={1: "PLAYER", 2: "AKA"})

st.divider()

