# Class to model Director objects
class Director:
    def __init__(self, first_name, last_name, num_awards, age):
        self._first_name = first_name
        self._last_name = last_name
        self._num_awards = num_awards
        self._age = age
    
    @property
    def name(self):
        return_value = first_name + " " + last_name
        return return_value
    
    @name.setter
    def name(self, new_name):
        self._first_name, self._last_name = new_name.split()
    
    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def num_awards(self):
        return self._num_awards
    
    @num_awards.setter
    def num_awards(self, new_num_awards):
        self._num_awards = new_num_awards
    
    @property
    def age(self):
        return self._age

    @age.setter
    def year(self, new_age):
        self._age = new_age


# Class to support reading/writing Director objects with the database
class DirectorDB:
    def __init__(self, db_conn, db_cursor):
        """
        Initialized an instance of the DirectorDB class

        :param db_conn: connection to the databse
        :param rating: databse cursor
        :returns: instance of the class is created
        """
        self._db_conn = db_conn
        self._cursor = db_cursor
    
    #selects director_id, first_name, and last_name from the directors table
    def select_all_directors(self):
        """
        Selects all information by director within the director table
        
        :returns: director_id, first_name, last_name, num_awards, age from the director table
        """
        select_all_query = """
            SELECT director_id, first_name, last_name, num_awards, age  from director_table;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()