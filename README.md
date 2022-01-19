# [Streamlit] FIFA22 Player Databases

Searching players can be cumbersome on FIFA22. I wanted to be able to find talents faster and easier, so I decided to create an app that caters to my (and preferably to other FIFA users') needs. The app provides two functionalities:

### 1) Search players by filtering
  - Adjust age, market value, player country, league and positions to find top talents under your criteria.
### 2) Look up particular player 
  - Find a particular player and see basic info including the player's top traits. Also, see list of players with similar traits. 
  
The Streamlit App can be accessed [here](https://share.streamlit.io/jayhoneylee527/fifa22-playerdb/main/fifa.py)

### Data Source
players.csv has been downloaded from [Kaggle](https://www.kaggle.com/stefanoleone992/fifa-22-complete-player-dataset?select=players_22.csv)

### How are the players of "similar traits" selected?

Based on 36 traits of each player, PCA reduces the trait dimensions down to 15. (~98% explained variance)
Then, using Euclidean distance, the app prints out players of the minimum distances in the ascending order. 
