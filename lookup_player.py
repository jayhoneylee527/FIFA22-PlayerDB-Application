import streamlit as st
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

from bokeh.plotting import figure
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances


def currency_convert(val):
	val = val.values[0]

	if val > 1000000:
		res = round(val / 1000000, 1)
		res = "€{:,.1f} Mil".format(res) 
	else:
		res = "€{:,.0f}".format(val)

	return res

def radar_chart(player):
	traits = [player.pace.values[0], player.shooting.values[0], player.passing.values[0], player.dribbling.values[0],\
		player.defending.values[0], player.physic.values[0]]

	traits = np.concatenate((traits,[traits[0]]))

	trait_names = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physique"] 

	label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(trait_names), endpoint=False)
	
	label_loc = np.concatenate((label_loc,[label_loc[0]]))	

	fig = plt.figure()
	ax = fig.add_subplot(111, polar=True)
	ax.plot(label_loc, traits, '-o')
	ax.fill(label_loc, traits, alpha=0.2, linewidth=0.5)
	ax.set_thetagrids(label_loc[:-1] * 180/np.pi, labels=trait_names)
	ax.axes.yaxis.set_ticklabels([])

	st.pyplot(fig)

def top_traits(player):
	# Columns with all the attributes
	tmp = ["attacking_","skill_","movement_","power_","mentality_","defending_","goalkeeping_"]
	trait_cols = [c for c in player.columns if any(i in c for i in tmp)]
	trait_cols.remove('skill_moves')

	ind = player.index.values[0]
	top_traits = player[trait_cols].T.sort_values(ind, ascending=False).head(20).sort_values(ind)
	
	#st.write(top_traits[ind].tolist())

	fig = figure(title="<Top Traits>", y_range=top_traits.index.tolist(), width=600, height=500)
	fig.title.text_font_size = '14pt'
	fig.title.align = 'center'
	fig.hbar(top_traits.index.tolist(), right=top_traits[ind].tolist(), height=0.2)
	st.bokeh_chart(fig)


@st.cache
def PCA_reduction(df):
	tmp = ["attacking_","skill_","movement_","power_","mentality_","defending_","goalkeeping_","overall"]
	trait_cols = [c for c in df.columns if any(i in c for i in tmp)] 
	X = df[trait_cols].copy()
	X.fillna(0, inplace=True)

	pca = PCA(n_components=15)
	X_reduced = pd.DataFrame(pca.fit_transform(X))
	X_reduced['name'] = df.short_name
	X_reduced.set_index('name', inplace=True)

	return X_reduced

def update_traits():
	if st.session_state.traits_select_2:
		st.session_state.traits_2 = st.session_state.traits_select_2

def show_similar_players(df, X_reduced, player_name, player_fullname, trait_cols):
	dist = euclidean_distances(X_reduced[X_reduced.index == player_name], X_reduced)
	dist = pd.DataFrame(dist).T
	dist['name'] = X_reduced.index
	similar_name_index = dist.sort_values(by=0).head(30).name.index

	select_traits = st.multiselect("Add Attributes", trait_cols, default=None, key='traits_select_2')

	df_show = df.copy()
	df_show = df_show.iloc[similar_name_index]
	df_show.set_index('short_name', inplace=True)
	st.dataframe(df_show[['overall','age','player_positions'] + select_traits])


def player_result(df, player_name, player_fullname):
	player = df[(df['short_name'] == player_name) & (df['long_name'] == player_fullname)]
	st.markdown("## %s" %player_name)

	col1, col2, col3, col4 = st.columns(4)

	with col1:
		st.metric(label="Overall", value=player.overall)

	with col2:
		lis = player.player_positions.values
		positions = ""
		for s in lis:
		    positions += s

		st.metric("Position", positions)	

	with col3:
		st.metric("Age", player.age)

	with col4:
		st.metric("Preferred Foot", player.preferred_foot.values[0])

	col1, col2, col3 = st.columns([2,4,2])

	with col1:
		val = currency_convert(player.value_eur)
		st.metric(label="Value", value=val)

	with col2:
		st.metric("Current Team", player.club_name.values[0])	

	with col3:
		st.metric("Nationality", player.nationality_name.values[0])


	st.text("")
	st.text("")
	st.markdown("###")

	col1, col2 = st.columns([1,1.5])

	with col1:
		st.text("")
		st.text("")
		radar_chart(player)

	with col2:
		top_traits(player)


