import mysql.connector
import csv



def connect_db(config):
    """
    Connect to MySQL and the task database

    :param config: environment configuration for the databse
    :returns: connection to mysql database
    """
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"],
        database=config["DATABASE"]
    )
    return conn

def populate_tables(csvfile, config):
    """
    Inserts data into tables from the csv file

    :param config: environment configuration for the databse
    :param csvfile: csv file to have initial data in databse
    :returns: database tables populated using csv data
    """
    conn = connect_db(config)
    cursor = conn.cursor(dictionary=True)
    
    sql_main_insert = """INSERT INTO main_table (movie_title,genre,year,director_id) 
        VALUES (%s, %s, %s, %s)"""
    sql_director_find = "SELECT director_id FROM director_table WHERE first_name=%s AND last_name=%s"
    sql_director_insert = "INSERT INTO director_table (first_name, last_name, num_awards, age) VALUES (%s, %s, %s, %s)"
    sql_ratings_insert = """INSERT INTO ratings_table (movie_id, rating, num_ratings)
        VALUES (%s, %s, %s)"""

    with open(csvfile, "r") as csv_input:
        reader = csv.DictReader(csv_input)
        for row in reader:
            cursor.execute(sql_director_find, (row['first_name'], row['last_name']))
            director_id = cursor.fetchone()
            if not director_id:
                cursor.execute(sql_director_insert, (row['first_name'], row['last_name'], row['num_awards'], row['age']))
                cursor.execute("SELECT LAST_INSERT_ID() director_id")
                director_id = cursor.fetchone()
            
            cursor.execute(sql_main_insert, 
                (row["title"], row["genre"], row["year"], director_id["director_id"]))
            
            cursor.execute(sql_ratings_insert,
                (row["movie_id"], row["rating"], row["num_ratings"]))

            

    conn.commit()
    cursor.close()
    conn.close()

def init_db(config):
    """
    Setup for the Database

    :param config: environment configuration for the databse
    :returns: database is initialized, will erase the database if it exists
    """
    conn = mysql.connector.connect (
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"]
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']};")
    cursor.execute(f"CREATE DATABASE {config['DATABASE']};")
    cursor.execute(f"use {config['DATABASE']};")
    cursor.execute(
        f""" 
        CREATE TABLE director_table
        (
            director_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            num_awards TINYINT UNSIGNED,
            age TINYINT UNSIGNED,
            CONSTRAINT pk_director PRIMARY KEY (director_id)
        );
        """
    )

    cursor.execute(
        f""" 
        CREATE TABLE main_table
        (
            movie_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            movie_title VARCHAR(100),
            genre VARCHAR(100),
            year SMALLINT(255),
            director_id SMALLINT UNSIGNED,
            CONSTRAINT pk_main PRIMARY KEY (movie_id),
            CONSTRAINT fk_director FOREIGN KEY (director_id)
                REFERENCES director_table (director_id)
        );
        """
    )

    cursor.execute(
        f""" 
        CREATE TABLE ratings_table
        (
            rating_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            movie_id SMALLINT UNSIGNED,
            rating SMALLINT(255),
            num_ratings SMALLINT(255),
            CONSTRAINT pk_rating PRIMARY KEY (rating_id),
            CONSTRAINT fk_movie_id FOREIGN KEY (movie_id)
                REFERENCES main_table (movie_id)
        );
        """
    )
    
    populate_tables("10_row_dataset.csv", config)
    cursor.close()
    conn.close()
