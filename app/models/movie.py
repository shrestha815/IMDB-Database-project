# Class to model Movie objects
class Movie:
    def __init__(self, title, genre, year, director_id):
        self._title = title
        self._genre = genre
        self._year = year
        self._director_id = director_id
        self._rating = 0
        self._num_ratings = 0
    
    @property
    def director_id(self):
        return self._director_id
    
    @director_id.setter
    def director_id(self, new_director):
        self._director_id = new_director
    
    @property
    def genre(self):
        return self._genre
    
    @genre.setter
    def genre(self, new_genre):
        self._genre = genre
    
    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, new_year):
        self._year = new_year

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @property
    def rating(self):
        return self._rating

    @property
    def num_ratings(self):
        return self._num_ratings


# Class to support reading/writing Movie objects with the database
class MovieDB:
    def __init__(self, db_conn, db_cursor):
        """
        Initialized an instance of the MovieDB class

        :param db_conn: connection to the databse
        :param rating: databse cursor
        :returns: instance of the class
        """
        self._db_conn = db_conn
        self._cursor = db_cursor

    def select_all_movies(self):
        """
        Selects all information by movie within the main table
        
        :returns: all data from the main table sorted by movie
        """
        select_all_query = """
            SELECT * from main_table;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()

    def select_title_and_rating(self):
        """
        Selects a movie title from the main table and its corresponding rating from the ratings table

        :returns: movie title from main_table and its corresponding rating from the ratings table
        """
        sel_query= """
            SELECT main_table.movie_title, ratings_table.rating, main_table.movie_id
            FROM main_table
                INNER JOIN ratings_table
                    ON main_table.movie_id = ratings_table.movie_id
        """
        self._cursor.execute(sel_query)
        return self._cursor.fetchall()

    def insert_movie(self, movie):
        """
        Inserts a movie into the main table, also inserts rating of 0 and num_ratings of 0 in the ratings table

        :param movie: object of class Movie with attributes movie_title, genre, year, director_id
        :returns: movie id of the newly created movie
        """
        insert_query = """
            INSERT INTO main_table (movie_title, genre, year, director_id)
            VALUES (%s, %s, %s, %s);
            
        """

        insert_query2 = """
            INSERT INTO ratings_table (rating, num_ratings, movie_id) VALUES (%s, %s, %s);
            
        """
            
        self._cursor.execute(insert_query, (movie.title, movie.genre, movie.year, movie.director_id))
        self._cursor.execute("SELECT LAST_INSERT_ID() movie_id")
        movie_id = self._cursor.fetchone()
        self._cursor.execute(insert_query2, (movie.rating, movie.num_ratings, movie_id['movie_id']))
        self._db_conn.commit()
        return movie_id

    #
    def delete_movie_by_id(self, movie_id):
        """
        Deletes a movie by corresponding movie_id, additionally deletes rating by corresponding movie_id

        :param movie_id: movie_id of the movie that is going to be deleted
        :returns: specified movie is deleted from the database
        """
        delete_query = """
            DELETE from main_table
            WHERE movie_id=%s;
        """

        delete_query2 = """
            DELETE from ratings_table
            WHERE movie_id=%s;
        """
        self._cursor.execute(delete_query2, (movie_id,))
        self._cursor.execute(delete_query, (movie_id,))
        self._db_conn.commit()

    #
    def update_rating_by_id(self,movie_id,rating):
        """
        Changes the rating in the ratings table to a specified value using rating_id

        :param movie_id: movie_id of the movie that is going to be deleted
        :param rating: the rating that the movie rating will be changed to
        :returns: specified movie rating is changed to the desired rating
        """
        update_query = """
            update ratings_table
            SET rating=%s
            WHERE rating_id=%s;
        """
        self._cursor.execute(update_query, (rating, movie_id))
        self._db_conn.commit()
        