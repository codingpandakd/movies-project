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
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT NOT NULL
        )
    """))
    connection.commit()

def movies_data():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM movies"))
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

def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()
    return {movie[0]: {"year": movie[1], "rating": movie[2]} for movie in movies}

def add_movie(title, year, rating, poster):
    """Add a new movie to the database."""
    params = {"title": title, "year": year, "rating": rating, "poster": poster}
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"), params)
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

def delete_movie(title):
    """Delete a movie from the database."""
    params = {"title": title}
    with engine.connect() as connection:
      try:
        connection.execute(text("DELETE FROM movies WHERE movies.title = :title"), params)
        connection.commit()
        print(f"Movie '{title}' deleted successfully.")
      except Exception as e:
        print(f"Error: {e}")

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    params = {"title": title, "rating": rating}
    with engine.connect() as connection:
      try:
        connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"), params)
        connection.commit()
        print(f"Movie {title} updated successfully")
      except Exception as e:
        print(f"Error: {e}")


print(movies_data())