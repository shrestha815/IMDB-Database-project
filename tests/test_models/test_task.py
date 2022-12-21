import pytest
from app.models.movie import Movie

def test_movie_constructor():
    movie_title = "test movie"
    genre = "test genre"
    year = "2022"
    director_id = "1"
    m = Movie(movie_title, genre, year, director_id)
    assert m.title == movie_title
    assert m.genre == genre
    assert m.year == year
    assert m.director_id == director_id


def test_movie_properties():
    movie_title = "test movie"
    genre = "test genre"
    year = "2022"
    director_id = "1"
    m = Movie(movie_title, genre, year, director_id)
    
    rename = "new movie name"
    m.title = rename
    assert m.title == rename
