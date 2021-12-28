import streamlit as st
import pandas as pd 
import numpy as np 

def make_positions(df):
	position_list = []
	
	for p in df.player_positions.unique():
		str_list = p.split(", ")
		for i in str_list:
			position_list.append(i)

	return list(set(position_list))


def show_players(df, age_range, val, nation, league, club=None, position=None):

	# Filter Age 
	df = df[(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])]
	

	# Filter position 
	if len(position) > 0:
		df_res = pd.DataFrame()
		for p in position:	
			df_res = df_res.append(df[df['player_positions'].str.contains(p)])
		df_res.sort_values(by='overall')

		df = df_res	

	#Filter nation
	if nation is not "All":
		df = df[df['nationality_name'] == nation] 	

	# Filter league 
	if league is not "All":
		df = df[df['league_name'] == league] 	

	# Filter Club
	if club is not None:
		if club != 'All':
			df = df[df['club_name'] == club] 	

	# Filter market value 
	lower_bound = val[0] * 1000000
	upper_bound = val[1] * 1000000
	df = df[(df['value_eur'] >= lower_bound) & (df['value_eur'] <= upper_bound)]
	
	df.set_index('short_name', inplace=True)
	df.round({'value_eur': 0, 'wage_eur': 0})
	st.dataframe(df[['overall','potential','age','player_positions','value_eur','wage_eur','club_name']])
	st.markdown("")


	return df

# Callback function 
def update_df(df_updated):
	if st.session_state.traits:
		st.session_state.df = df_updated[st.session_state.traits]

	return st.session_state.df
	
