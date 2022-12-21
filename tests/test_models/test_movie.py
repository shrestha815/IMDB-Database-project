import pytest
from app.models.movie import Movie
from app.models.director import Director

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

def test_director_constructor():
    director_first_name = "test"
    director_last_name = "director"
    director_num_awards = "4"
    director_age = "2"
    d = Director(director_first_name, director_last_name, director_num_awards, director_age)
    assert d.first_name == director_first_name
    assert d.last_name == director_last_name
    assert d.num_awards == director_num_awards
    assert d.age == director_age