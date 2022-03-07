import json
import logging

from tmdbv3api import TMDb
from tmdbv3api import Movie

from model_handler import model_loader, predict_result
from prepare_for_database import prepare_for_insert, execute_insert

model_path = 'model/LSTM_model.hdf5'
model = model_loader(model_path)

tmdb = TMDb()
tmdb.api_key = '5378e4a5747235021f6f923ea12b8117'
tmdb.language = 'en'

movie = Movie()
popular = movie.popular()
results_path = "results.json"


def run_analysis():

    movieData = []
    for p in popular:
        objectDict = {}
        idm = p.id

        review = movie.reviews(idm)
        review_details = [predict_result(item.content, model) for item in review]

        info = movie.details(idm)
        genres = [genre.name for genre in info.genres]
        actors = [actor.name for actor in info.casts.cast]
        directors = [director.name for director in info.casts.crew if director.job == 'Director']

        objectDict['original_title'] = p.original_title
        objectDict['genre'] = genres
        objectDict['release_date'] = p.release_date
        objectDict['actors'] = actors
        objectDict['directors'] = directors
        objectDict['review_results'] = review_details
        movieData.append(objectDict)
        logging.info(f"Finished analysis for movie: {p.original_title}")

    with open(results_path, "w") as outfile:
        json.dump(movieData, outfile, indent=2)
        logging.info(f"Saved results to json file results.json")

    sql_command = prepare_for_insert(results_path)

    return movieData, sql_command


if __name__ == '__main__':
    _, sql_sequence = run_analysis()
    execute_insert(sql_sequence)
