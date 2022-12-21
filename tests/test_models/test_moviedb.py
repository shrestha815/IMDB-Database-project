from app.models.movie import Movie, MovieDB
from app.models.director import Director, DirectorDB

# By using the parameter db_test_client, we automatically get access to our test
#   database provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).
def test_movie_insert(db_test_client):
    conn, cursor = db_test_client
    moviedb = MovieDB(conn, cursor)

    moviedb.insert_movie(Movie("test movie", "test genre", "2022", "1"))
    
    moviedb.update_rating_by_id(1,4)
    movie_list = moviedb.select_title_and_rating()
    
    assert len(movie_list) == 11
    assert movie_list[10]["movie_id"] == 11
    assert movie_list[10]["movie_title"] == "test movie"
    assert movie_list[0]["rating"] == 4
    conn.commit()

def test_rating_update(db_test_client):
    conn, cursor = db_test_client
    moviedb = MovieDB(conn, cursor)
    moviedb.update_rating_by_id(1,4)
    movie_list = moviedb.select_title_and_rating()
    
    assert len(movie_list) == 11
    assert movie_list[10]["movie_id"] == 11
    assert movie_list[0]["rating"] == 4
    conn.commit()


def test_movie_delete(db_test_client):
    conn, cursor = db_test_client
    moviedb = MovieDB(conn, cursor)
    moviedb.insert_movie(Movie("Delete me!", "test genre", "2022", "2"))
    moviedb.delete_movie_by_id(12)
    movie_list = moviedb.select_title_and_rating()
    assert len(movie_list) == 11
    conn.commit()

def test_select_all_movies(db_test_client):
    conn, cursor = db_test_client
    moviedb = MovieDB(conn, cursor)
    movie_list = moviedb.select_all_movies()
    assert len(movie_list) == 11
    assert movie_list[10]["movie_id"] == 11
    assert movie_list[10]["genre"] == "test genre"
    assert movie_list[10]["year"] == 2022
    assert movie_list[10]["director_id"] == 1
    conn.commit()

def test_director(db_test_client):
    conn, cursor = db_test_client
    directordb = DirectorDB(conn, cursor)
    director_list = directordb.select_all_directors()
    
    assert len(director_list) == 10
    assert director_list[0]["director_id"] == 1
    assert director_list[0]["first_name"] == "Doralynne"
    assert director_list[0]["last_name"] == "Ryott"
    assert director_list[0]["num_awards"] == 5
    assert director_list[0]["age"] == 33
    conn.commit()
