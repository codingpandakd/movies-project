from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL) #echo=True helps for debugging during development.

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            user_id INTEGER NOT NULL,
            poster TEXT NOT NULL
        )
    """))
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    """))
    connection.execute(text("""
            INSERT OR IGNORE INTO users (username) VALUES ('default_user'
            )
        """))
    connection.commit()

def movies_data(user_id):
    """Retrieve all movies from the database."""
    params = {"user_id": user_id}
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM movies WHERE user_id = :user_id"), params)
        movies = result.mappings().all()
    return [
    {
        "title": movie["title"],
        "year": movie["year"],
        "rating": movie["rating"],
        "poster": movie["poster"]
    }
    for movie in movies
]

def create_user(username):
    """Add a new user to the database."""
    params = {"username": username}
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO users (username) VALUES (:username)"), params)
            connection.commit()
            print(f"User '{username}' created successfully.")
        except Exception as e:
            print(f"Error: {e}")

def users_data():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT user_id, username FROM users"))
        users = result.mappings().all()
    return {order+1: {"username": user["username"], "user_id": user["user_id"]} for order, user in enumerate(users)}

def delete_user(username):
    """ Delete user from database """
    params = {"username": username}
    with engine.connect() as connection:
        try:
            # Check if user exists
            result = connection.execute(
                text("SELECT username FROM users WHERE username = :username"), params
            ).first()

            if not result:
                print(f"User '{username}' does not exist.")
                return

            # Delete the user
            connection.execute(text("DELETE FROM users WHERE users.username = :username"), params)
            connection.commit()
            print(f"User '{username}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def list_movies(user_id):
    """Retrieve all movies from the database."""
    params = {"user_id": user_id}
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster, user_id FROM movies WHERE user_id = :user_id"), params)
        movies = result.fetchall()
    return {movie[0]: {"year": movie[1], "rating": movie[2], "user_id": movie[4]} for movie in movies}

def add_movie(title, year, rating, poster, user_id):
    """Add a new movie to the database."""
    params = {"title": title, "year": year, "rating": rating, "user_id": user_id, "poster": poster}
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, user_id, poster) VALUES (:title, :year, :rating, :user_id, :poster)"), params)
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")

def delete_movie(title, user_id):
    """Delete a movie from the database."""
    params = {"title": title, "user_id": user_id}
    with engine.connect() as connection:
      try:
        connection.execute(text("DELETE FROM movies WHERE movies.title = :title AND movies.user_id = :user_id"), params)
        connection.commit()
      except Exception as e:
        print(f"Error: {e}")

def update_movie(title, rating, user_id):
    """Update a movie's rating in the database."""
    params = {"title": title, "rating": rating, "user_id": user_id}
    with engine.connect() as connection:
      try:
        connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title AND user_id = :user_id"), params)
        connection.commit()
      except Exception as e:
        print(f"Error: {e}")

