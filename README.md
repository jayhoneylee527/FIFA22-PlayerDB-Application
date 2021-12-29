# [Streamlit] FIFA22 Player Databases

The app provides two functionalities:
1) Find players by filtering
2) Look up particular player 

The Streamlit App can be accessed [here](https://share.streamlit.io/jayhoneylee527/fifa22-playerdb/main/fifa.py)

### How are the players of "similar traits" selected?

Based on 36 traits of each player, PCA reduces the trait dimensions down to 15. (~98% explained variance)
Then, using Euclidean distance, the app prints out players of the minimum distances in the ascending order. 
