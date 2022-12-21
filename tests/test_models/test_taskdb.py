from app.models.movie import Movie, MovieDB

# By using the parameter db_test_client, we automatically get access to our test
#   database provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).
def test_movie_insert(db_test_client):
    # The test fixture only setups the 
    conn, cursor = db_test_client
    moviedb = MovieDB(conn, cursor)

    moviedb.insert_movie(Movie("test movie", "test genre", "2022", "1"))
    
    result = moviedb.select_director_by_id(1)
    assert result['director_id'] == "1"
    conn.commit()


def test_movie_delete(db_test_client):
    conn, cursor = db_test_client
    moviedb = MovieDB(conn, cursor)
    
    moviedb.insert_movie(Movie("Delete me!", "test genre", "2022", "2"))

    result = moviedb.select_director_by_id(2)
    assert result['director_id'] == "2"

    moviedb.delete_movie_by_id(2)
    result = moviedb.select_movie_by_id(2)
    assert len(result) == 0
    conn.commit()
