from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from models.movie import MovieDB
from models.movie import Movie
from models.director import DirectorDB

movies_blueprint = Blueprint('movies_blueprint', __name__)

#blueprints for the home page, displays list of all movies and their corresponding rating from the ratings table
@movies_blueprint.route('/', methods=["GET"])
def index():
    database = MovieDB(g.mysql_db, g.mysql_cursor)
    if request.method == "POST":
        movie_ids = request.form.get("movie_title")
        for movie_id in movie_ids:
            database.delete_movie_by_id(id)


    return render_template('index.html', movie_list=database.select_title_and_rating())    



#
@movies_blueprint.route('/movie-entry', methods=["GET"])
def movie_entry():
    """
    Blueprint for the movie entry route which allows a user to enter a new movie into the database
        
    :returns: movie-entry.html is created and presented to the user allowing them to enter a movie
    """
    database = DirectorDB(g.mysql_db, g.mysql_cursor)
    return render_template("movie-entry.html",directors = database.select_all_directors())

#
@movies_blueprint.route('/movie-delete', methods=["GET"])
def movie_delete():
    """
    Blueprint for the movie delete route which allows a user to delete a movie from the database
        
    :returns: movie-delete.html is created and presented to the user allowing them to delete a movie
    """
    database = MovieDB(g.mysql_db, g.mysql_cursor)
    return render_template("movie-delete.html",movies = database.select_all_movies())

#blueprint for the update movie route which allows a user to update a rating for a specified movie
@movies_blueprint.route('/update-rating', methods=["GET"])
def update_rating():
    """
    Blueprint for the update movie route which allows a user to update a rating for a specified movie
        
    :returns: update-rating.html is created and presented to the user allowing them to update a movie rating
    """
    database = MovieDB(g.mysql_db, g.mysql_cursor)
    return render_template("update-rating.html",movies = database.select_all_movies())


@movies_blueprint.route('/add-movie', methods=["POST"])
def add_movie():
    """
    Function that adds a movie to the databse using input forms provided to the user
        
    :returns: Redirects back to main page
    """
    movie_title = request.form.get("movie_title")
    genre = request.form.get("genre")
    year = request.form.get("year")
    director_id = request.form.get("director_id")
    
    new_movie = Movie(movie_title, genre, year, director_id)
    
    database = MovieDB(g.mysql_db, g.mysql_cursor)

    database.insert_movie(new_movie)

    return redirect('/')

#
@movies_blueprint.route('/delete-movie', methods=["POST"])
def delete_movie():
    """
    Function that deletes a movie specified by an input form
        
    :returns: Redirects back to main page
    """
    print("delete")
    movie_id = request.form.get("movie_id")
    database = MovieDB(g.mysql_db, g.mysql_cursor)

    database.delete_movie_by_id(movie_id)

    return redirect('/')

@movies_blueprint.route('/update-rating', methods=["POST"])
def rate_movie():
    """
    Function that updates the rating of a chosen movie
        
    :returns: Redirects back to main page
    """
    movie_id = request.form.get("movie_id")
    new_rating = request.form.get("rating")
    
    database = MovieDB(g.mysql_db, g.mysql_cursor)

    database.update_rating_by_id(movie_id,new_rating)

    return redirect('/')