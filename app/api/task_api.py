"""
task_api.py

Routes for the API and logic for managing Tasks.
"""

from flask import g, request, jsonify, Blueprint

from models.movie import Movie, MovieDB

# Establish the blueprint to link it to the flask app file (main_app.py)
#   Need to do this before you create your routes
movie_api_blueprint = Blueprint("movie_api_blueprint", __name__)


# Define routes for the API
#   Note that we can stack the decorators to associate similar routes to the same function.
#   In the case below we can optionally add the id number for a task to the end of the url
#   so we can retrieve a specific task or the entire list of tasks as a JSON object
@movie_api_blueprint.route('/api/v1/movies/', defaults={'movie_id':None}, methods=["GET"])
@movie_api_blueprint.route('/api/v1/movies/<int:movie_id>/', methods=["GET"])
def get_movies(movie_id):
    """
    get_tasks can take urls in a variety of forms:
        * /api/v1/task/ - get all tasks
        * /api/v1/task/1 - get the task with id 1 (or any other valid id)
        * /api/v1/task/?search="eggs" - find all tasks with the string "eggs" anywhere in the description
            * The ? means we have a query string which is essentially a list of key, value pairs
                where the ? indicates the start of the query string parameters and the pairs are separated
                by ampersands like so:
                ?id=10&name=Sarah&job=developer
            * The query string is optional 
    """

    # To access a query string, we need to get the arguments from our web request object
    args = request.args
    
    # setup the TaskDB object with the mysql connection and cursor objects
    moviedb = MovieDB(g.mysql_db, g.mysql_cursor)

    result = None
    
    # If an ID for the task is not supplied then we are either returning all
    #   tasks or any tasks that match the search query string.
    if movie_id is None:
        # Logic to find all or multiple tasks

        # Since the args for the query string are in the form of a dictionary, we can
        #   simply check if the key is in the dictionary. If not, the web request simply
        #   did not supply this information.
        if not 'search' in args:
            result = moviedb.select_all_movies()
        # All tasks matching the query string "search"
        else:
            #changes required here - Safal
            result = moviedb.select_all_tasks_by_description(args['search'])
    
    else:
        # Logic to request a specific task
        # We get a specific tasks based on the provided task ID

        #changes required here as well select_all_movies_by_id needs to be made -Safal
        result = moviedb.select_all_movies(movie_id)

    # Sending a response of JSON including a human readable status message,
    #   list of the tasks found, and a HTTP status code (200 OK).
    return jsonify({"status": "success", "tasks": result}), 200


@movie_api_blueprint.route('/api/v1/movies/', methods=["POST"])
def add_movie():
    moviedb = MovieDB(g.mysql_db, g.mysql_cursor)
    #posisble syntax error here -safal    
    movie = Movie(request.json['description'])
    result = moviedb.insert_task(movie)
    
    return jsonify({"status": "success", "id": result['movie_id']}), 200


@movie_api_blueprint.route('/api/v1/movies/<int:movie_id>/', methods=["PUT"])
def update_movie(movie_id):
    moviedb = MovieDB(g.mysql_db, g.mysql_cursor)
    # line 84 'description' probably needs to be changed -Safal
    movie = Movie(request.json['movie_title'])
    moviedb.update_task(movie_id, movie)
    
    return jsonify({"status": "success", "movie_id": movie_id}), 200


@movie_api_blueprint.route('/api/v1/movies/<int:task_id>/', methods=["DELETE"])
def delete_movie(movie_id):
    moviedb = MovieDB(g.mysql_db, g.mysql_cursor)

    moviedb.delete_movie_by_id(movie_id)
        
    return jsonify({"status": "success", "id": movie_id}), 200
