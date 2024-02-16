# This is a module from Python’s standard library. It contains code related to working with your computer’s operating system.
import os
# You’ll need this to load the data in data/movies.json. Feel free to research the Python “JSON” module.
import json
# choice is a function that takes in a list and returns a random element in the list.
# randint will return a random number within a certain range. You’ll use both to generate fake users and rating
from random import choice, randint
# We’ll use datetime.strptime to turn a string into a Python datetime object.
from datetime import datetime
# These are all files that you wrote (or will write) — crud.py, model.py, and server.py
import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')


model.connect_to_db(server.app)


with server.app.app_context():
    model.db.create_all()
# Load movie data from JSON file
    with open('data/movies.json') as f:
        movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
        
        movies_in_db = []

        for movie in movie_data:
            title = movie["title"]
            overview = movie["overview"]
            poster_path = movie["poster_path"]

            release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

            new_movie = crud.create_movie(title, overview, release_date, poster_path)
            movies_in_db.append(new_movie)
    
        model.db.session.add_all(movies_in_db)
        model.db.session.commit()

        for n in range(10):
            email = f"user{n}@test.com"  # Voila! A unique email!
            password = "test"

            new_user = crud.create_user(email, password)
            model.db.session.add(new_user)

            for _ in range(10):
                random_movie = choice(movies_in_db)
                score = randint(1, 5)

                new_rating = crud.create_rating(new_user, random_movie, score)
                model.db.session.add(new_rating)

        model.db.session.commit()