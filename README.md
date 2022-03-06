# sentimentAnalysisIMDB

A python program that downloads the information about the most popular movies from IMDB via API The Movie Database (TMDB),

gets info about original name, genres, actors, directors, and release date.

Additionaly it gets the reviewes for each movies and does a sentiment analysis on them using the LSTM model.

The results are saved in json for each movie and also processed to postgreSQL commands so that they can be stored in database

Database and the app can be made into docker containers so that the process goes automatically, the instructions are writen in the **docker_readme_file.txt**

To run the app locally just run the **main.py**
