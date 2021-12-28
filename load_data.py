import streamlit as st
import pandas as pd 
import numpy as np 

@st.cache
def load_players(file_name):
	df = pd.read_csv(file_name)
	
	# Remove any columns with url
	url_c = [c for c in df.columns if "url" in c]
	df.drop(url_c, axis=1, inplace=True)
	
	# Convert dtypes of value and wage into int64 
	df.fillna(0, inplace=True)
	df = df.astype({'value_eur': 'int64', 'wage_eur': 'int64'})

	return df
