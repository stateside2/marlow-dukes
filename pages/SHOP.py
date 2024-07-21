import streamlit as st

st.set_page_config(page_title="Shop", page_icon="images/marlowdukesicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

# --- HIDE 1) STREAMLIT HEADER/FOOTER MENUS, 2) POP-UP DOWNLOAD, SEARCH, EXPAND DATAFRAME ELEMENTS, 3) EXPAND IMAGE  ---
hide_st_style = """ 
	<style>MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} 
	[data-testid="stElementToolbar"] {display: none;} 
	button[title="View fullscreen"] {visibility: hidden;} 
	</style>
	"""
st.markdown(hide_st_style, unsafe_allow_html=True)
# ----


#one, two, three = st.columns([0.2,0.6,0.2])
#two.image("images/shop_offsidegarbbannerlight.png", width=400)

st.image("images/shop_marlowmerchbanner.png", use_column_width=True)

st.link_button(":white[CLICK HERE TO VISIT THE STORE]", url="https://marlow-merch.myspreadshop.co.uk", use_container_width=True)
#st.button(":grey[COMING SOON!!]", use_container_width=True)

left, middle, right = st.columns(3)
left.image("images/shop_marlowdukesbaseballcap.png", caption="Contrast Snapback Cap")
middle.image("images/shop_marlowdukestshirt.png", caption="Mens T-shirt")
right.image("images/shop_marlowdukesbuckethat.png", caption="Bucket Hat")

st.link_button(":white[CLICK HERE TO VISIT THE STORE]", url="https://marlow-merch.myspreadshop.co.uk/", use_container_width=True)

st.divider()
