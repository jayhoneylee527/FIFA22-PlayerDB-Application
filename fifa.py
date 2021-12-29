import streamlit as st
import pandas as pd 
import numpy as np 

from load_data import *
from lookup_player import *
from search_talent import *

st.set_page_config(layout="wide", page_title="FIFA 22 Player Database")

df = load_players("players_22.csv")

# List columns with player traits 
tmp = ["attacking_","skill_","movement_","power_","mentality_","defending_","goalkeeping_","overall"]
trait_cols = [c for c in df.columns if any(i in c for i in tmp)] + ['age', 'player_positions']

options = ["Search Talent", "Look up Player"]
view = st.sidebar.radio("View", options)

	
if view == "Search Talent":
	st.header("[FIFA22] Search Players by Criteria")
	st.markdown("Adjust the filters below to find the types of players you are looking for. Also, you may click on the column names to sort.")
	st.text("")

	col1, col2 = st.columns(2)

	age_range = col1.select_slider("Age", options=np.arange(16,51), value=(16,50))
	
	position_list = make_positions(df)
	position = col1.multiselect("Position", position_list, default=None)

	nation_list = list(df.nationality_name.unique())
	nation_list.sort()
	nation_list.insert(0,"All")
	nation = col1.selectbox("Country", nation_list, index=0)

	val = col2.select_slider("Value(Million €)", options=np.arange(0, 201), value=(0,200))	
	
	league_list = list(df.league_name.unique())
	league_list.insert(0,"All")
	league = col2.selectbox("League", league_list, index=0)

	club = None

	if league is not "All":
		club_list = list(df[df['league_name'] == league].club_name.unique())
		club_list.sort()
		club_list.insert(0,"All")
		club = col2.selectbox("Current Club", club_list, index=0)

	st.text("")
	st.text("")
	df_updated = show_players(df, age_range, val, nation, league, club, position)

	st.markdown("### Search Players' Specific Traits")

	select_traits = st.multiselect("Add Attributes", trait_cols, default=None, key='traits_select')
	st.dataframe(df_updated[['overall','age','player_positions'] + select_traits])

if view == "Look up Player":
	st.header("[FIFA22] Player Search Engine")
	player_name = st.sidebar.selectbox('Search Player', df['short_name'])
	player_fullname = st.sidebar.selectbox('Player Fullname', df[df['short_name'] == player_name]['long_name'])

	player_result(df, player_name, player_fullname)
	st.markdown("### Players with Similar Traits")
	
	X_reduced = PCA_reduction(df)

	show_similar_players(df, X_reduced, player_name, player_fullname, trait_cols)
