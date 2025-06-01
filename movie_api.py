import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_URL = f"https://www.omdbapi.com/?apikey={API_KEY}&t="


def api_call(movie_by_title):
    res = requests.get(API_URL + movie_by_title)
    if res.status_code == requests.codes.ok:
        res = res.json()
        try:
            movie_title = res["Title"]
            movie_year = res.get("Year", "N/A")
            movie_rating = res.get("imdbRating", "N/A")
            movie_poster = res.get("Poster", "N/A")
            return {"Title": movie_title, "Year": movie_year, "Rate": movie_rating, "Poster": movie_poster}
        except KeyError:
            return False
    else:
        print("Error:", res.status_code, res.text)