import random
from thefuzz import fuzz  # for the name match
from data import movie_storage_sql as storage
import movie_api as call_api

def user_menu(selected_uid, selected_username):
    """ User menu to get input and explain what does what """
    loop_menu = True
    while loop_menu:
        print(f"Welcome back, {selected_username}! 🎬\n")
        print("Menu: \n0. Exit\n1. List movie\n2. Add movie\n3. Delete movie\n4. Update movie\n"
              "5. Stats\n6. Random movie\n7. Search movie\n8. Movies sorted by rating\n9. Generate website")

        user_input = input("Enter choice: ")
        print()
        if user_input == "1":
            command_list_movies(selected_uid, selected_username)
            show_enter_to_continue()
        elif user_input == "2":
            command_add_movie(selected_uid, selected_username)
            show_enter_to_continue()
        elif user_input == "3":
            command_delete_movie(selected_uid, selected_username)
            show_enter_to_continue()
        elif user_input == "4":
            command_update_movie(selected_uid, selected_username)
            show_enter_to_continue()
        elif user_input == "5":
            command_statistics(selected_uid)
            show_enter_to_continue()
        elif user_input == "6":
            command_random_movie(selected_uid)
            show_enter_to_continue()
        elif user_input == "7":
            command_search_movie(selected_uid)
            show_enter_to_continue()
        elif user_input == "8":
            command_movies_sorted(selected_uid)
            show_enter_to_continue()
        elif user_input == "9":
            command_generate_website(selected_uid, selected_username)
            show_enter_to_continue()
        elif user_input == "0":
            print("Bye!")
            return

def command_add_movie(selected_uid, username):
    """ If conditions meet by giving input add movie to data """
    get_movie_name = input("Enter new movie name: ")
    movie = call_api.api_call(get_movie_name)
    if movie:
        movie_title = movie["Title"]
        movie_year = movie["Year"]
        movie_rate = movie["Rate"]
        movie_poster = movie["Poster"]
        movie_user_id = selected_uid
        storage.add_movie(movie_title, movie_year, movie_rate, movie_poster, movie_user_id)
        print(f"✅Movie {movie_title} added to {username}'s collection!")
    else:
        print(f"❌Movie '{get_movie_name}' not found.")

def command_list_movies(selected_uid, username):
    """ Retrieve and display all movies from the database """
    movies = storage.list_movies(selected_uid)
    if len(movies) > 0:
        print(f"{len(movies)} movies in total in {username}'s collection!")
        for movie_name, infos in movies.items():
            year = infos.get("year", "N/A")
            rate = infos.get("rating", "N/A")
            print(f"{movie_name} ({year}): {rate}")
    else:
        print(f"📢 {username}, your movie collection is empty. Add some movies!")

def command_delete_movie(selected_uid, username):
    """ When user input match with movie, delete it """
    movies = storage.list_movies(selected_uid)
    selected_uid = int(selected_uid)
    get_movie_name = input("Enter movie name to delete: ")
    if get_movie_name in movies and selected_uid == movies[get_movie_name]["user_id"]:
        storage.delete_movie(get_movie_name, selected_uid)
        print(f"✅Movie '{get_movie_name}' deleted successfully from {username}'s collection!")
    else:
        print(f"❌Movie '{get_movie_name}' doesn't exist in {username}'s collection!")

def command_update_movie(selected_uid, username):
    """ When user input match with a movie, update by user rating """
    movies = storage.list_movies(selected_uid)
    get_movie_name = input("Enter movie name: ")
    if get_movie_name in movies:
        while True:
            try:
                new_rating = float(input("Enter new rating (0-10): "))
                if 0 <= new_rating <= 10:
                    storage.update_movie(get_movie_name, new_rating, selected_uid)
                    print(f"✅Movie '{get_movie_name}' updated successfully in {username}'s collection!")
                    break
                else:
                    print("Rating must be between 0 and 10.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        print(f"❌Movie '{get_movie_name}' not exist in {username}'s collection!")

def command_statistics(selected_uid):
    """ Show statistics of films: best, worst, average, and median rating """
    movies = storage.list_movies(selected_uid)
    if not movies:
        print("No movies available.")
        return
    movie_rates = [float(infos["rating"]) for infos in movies.values()]
    avg_rating = sum(movie_rates) / len(movie_rates)
    sorted_rates = sorted(movie_rates)
    median_rating = (sorted_rates[len(movie_rates) // 2] if len(movie_rates) % 2 else
                     (sorted_rates[len(movie_rates) // 2 - 1] + sorted_rates[len(movie_rates) // 2]) / 2)
    best_rate = max(movie_rates)
    worst_rate = min(movie_rates)
    best_movies = [name for name, infos in movies.items() if float(infos["rating"]) == best_rate]
    worst_movies = [name for name, infos in movies.items() if float(infos["rating"]) == worst_rate]
    print(f"Average rating: {avg_rating:.1f}")
    print(f"Median rating: {median_rating:.1f}")
    print(f"Best movie{'s' if len(best_movies) > 1 else ''}: {', '.join(best_movies)} ({best_rate})")
    print(f"Worst movie{'s' if len(worst_movies) > 1 else ''}: {', '.join(worst_movies)} ({worst_rate})")

def command_random_movie(selected_uid):
    """ Select and display a random movie """
    movies = storage.list_movies(selected_uid)
    if not movies:
        print("No movies available.")
        return
    movie_name, infos = random.choice(list(movies.items()))
    print(f"Your random movie for tonight is {movie_name}, it's rated {infos['rating']}")

def command_search_movie(selected_uid):
    """ Search movie by partial name """
    movies = storage.list_movies(selected_uid)
    if not movies:
        print("No movies available.")
        return
    search_term = input("Enter part of movie name: ").lower()
    results = [f"{name} ({infos['year']}): {infos['rating']}" for name, infos in movies.items()
               if search_term in name.lower()]
    if results:
        print("\n".join(results))
    else:
        print("No movies found.")
        suggestions = [(name, fuzz.partial_ratio(name.lower(), search_term)) for name in movies.keys()
                      if fuzz.partial_ratio(name.lower(), search_term) >= 75]
        if suggestions:
            print("Did you mean:")
            for name, score in sorted(suggestions, key=lambda x: x[1], reverse=True):
                print(f"- {name}")

def command_movies_sorted(selected_uid):
    """ Sort movies by rating in descending order with optional limit """
    movies = storage.list_movies(selected_uid)
    if not movies:
        print("No movies available.")
        return
    limit = input("Enter number of movies to show (e.g., 3 or 10), or press Enter for all: ")
    limit = int(limit) if limit.isdigit() else None
    sorted_movies = sorted(movies.items(), key=lambda x: float(x[1]["rating"]), reverse=True)
    if limit:
        sorted_movies = sorted_movies[:limit]
    for name, infos in sorted_movies:
        print(f"{name} ({infos['year']}): {infos['rating']}")

def command_generate_website(user_id, username):
    movie_grid = html_movie_grid(user_id)
    website_title = f"{username}'s Movies Collection!"
    new_html_name = f"./website/{username}.html"
    html_template_path = "website/index_template.html"
    with open(html_template_path, "r") as html_theme:
        html_template = html_theme.read()
    with open(new_html_name, "w") as new_index:
        replace_template = html_template.replace("__TEMPLATE_TITLE__", website_title)
        replace_template = replace_template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
        new_index.write(replace_template)
    print(f"✅Website was generated successfully for {username}'s collection! as '{username}.html'")

def html_movie_grid(user_id):
    """ Output for HTML """
    movies = storage.movies_data(user_id)
    output = ''
    for movie in movies:
        movie_title = movie["title"]
        movie_year = movie["year"]
        movie_rate = movie["rating"]
        movie_poster = movie["poster"]
        movie_note = movie["note"]
        output += '<li>'
        output += '<div class="movie-block">'
        output += '<div class="movie">'
        output += f'<img class="movie-poster" src="{movie_poster}">'
        output += f'<div class="movie-title">{movie_title}</div>'
        output += f'<div class="movie-year">{movie_year}</div>'
        output += f'<div class="movie-rate">IMDB: {movie_rate}</div>'
        output += '</div>'
        if len(movie_note) > 0:
            output += f'<div class="movie-note">{movie_note}</div>'
        output += '</div>'
        output += '</li>'
    return output

def select_user_list():
    users = storage.users_data()
    print("\nSelect a user:")
    for user_order, username in users.items():
        user_username = username["username"]
        print(f"{user_order}. {user_username}")
    command_create_user = max(user for user in users) + 1
    command_delete_user = command_create_user + 1
    print(f"{command_create_user}. Create a new user")
    print(f"{command_delete_user}. Delete a user\n")
    return command_create_user, command_delete_user

def select_user():
    print(f"Welcome to the Movie App! 🎬")
    users = storage.users_data()
    command_create_user, command_delete_user = select_user_list()
    loop_menu = True
    while loop_menu:
        get_user_choice = input("Enter choice: ")
        if not get_user_choice.isdigit():
            print("Please enter a number.")
            continue
        get_user_choice = int(get_user_choice)
        if get_user_choice in users:
            selected_username = users[get_user_choice]["username"]
            selected_uid = users[get_user_choice]["user_id"]
            return selected_uid, selected_username
        elif get_user_choice == command_create_user:
            get_new_username = input("Please enter your new username: ")
            storage.create_user(get_new_username)
            users = storage.users_data()  # refresh data
            command_create_user, command_delete_user = select_user_list()  # refresh create_user number
            continue
        elif get_user_choice == command_delete_user:
            get_delete_username = input("Please enter a username to delete: ")
            storage.delete_user(get_delete_username)
            users = storage.users_data()  # refresh data
            command_create_user, command_delete_user = select_user_list()  # refresh create_user number
        else:
            print("Please select one of the options")

def main():
    selected_uid, selected_username = select_user()
    user_menu(selected_uid, selected_username)

def show_enter_to_continue():
    """ Just print to screen message """
    print()
    input("Press Enter to continue")

if __name__ == "__main__":
    main()