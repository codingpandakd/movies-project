import random
from thefuzz import fuzz # for the name match
from data import movie_storage_sql as storage
import movie_api as call_api

def user_menu():
    """ user menu to get input and explain what does what """
    loop_menu = True
    while loop_menu:
        print(f"{'*' * 10} My Movies Database {'*' * 10}\n")
        print(f"Menu: \n0. Exit\n1. List movie\n2. Add movie\n3. Delete movie\n4. "
              f"Update movie\n5. Stats\n6. Random movie\n7. Search movies\n8. "
              f"Movies sorted by rating\n9. Movie sorted by year\n10. Filter movies"
              f"\n11. Generate Website")
        user_input = input("Enter choice (1-11): ")
        print()
        if user_input == "1": #if user type 1,2,3 etc call the function depends by number
            command_list_movies() #for example when user type 1 calling the list function
            show_enter_to_continue() #to show press enter to continue message
        elif user_input == "2":
            command_add_movie()
            show_enter_to_continue()
        elif user_input == "3":
            command_delete_movie()
            show_enter_to_continue()
        elif user_input == "4":
            command_update_movie()
            show_enter_to_continue()
        elif user_input == "5":
            command_statistics()
            show_enter_to_continue()
        elif user_input == "6":
            command_random_movie()
            show_enter_to_continue()
        elif user_input == "7":
            command_search_movie()
            show_enter_to_continue()
        elif user_input == "8":
            command_movies_sorted("rate")
            show_enter_to_continue()
        elif user_input == "9":
            command_movies_sorted("year")
            show_enter_to_continue()
        elif user_input == "10":
            command_filter_movies()
            show_enter_to_continue()
        elif user_input == "11":
            get_website_name = input("Enter website name: ")
            command_generate_website(get_website_name)
            show_enter_to_continue()
        elif user_input == "0":
            print("Bye!")
            return

def command_add_movie():
    """ if conditions meet by giving input add movie to data """
    #first get movie title from user
    get_movie_name = input("Enter new movie name: ")

    # Get the data from the API
    movie = call_api.api_call(get_movie_name)
    if movie:
        movie_title = movie["Title"]
        movie_year = movie["Year"]
        movie_rate = movie["Rate"]
        movie_poster = movie["Poster"]
        storage.add_movie(movie_title, movie_year, movie_rate, movie_poster)
    else:
        print(f"Movie '{get_movie_name}' not found.")

def command_list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    #to count total we check how much key,value exist in the dict
    for movie_name, infos in movies.items():
        #.items return key and value which we used 2 values to save seperately
        #for one is key second one is value
        year = infos.get("year", "N/A")
        rate = infos.get("rating", "N/A")
        print(f"{movie_name} ({year}): {rate}")


def command_delete_movie():
    """ when user input match with movie, delete it """
    # Get the data from DB
    movies = storage.list_movies()
    get_movie_name = input("Enter movie name to delete: ")

    if get_movie_name in movies: #if match the user input name with the key
        storage.delete_movie(get_movie_name)
    else:
        print(f"Movie {get_movie_name} doesn't exist!")

def command_update_movie():
    """ when user input match with a movie, update by user rating """
    # Get the data from DB
    movies = storage.list_movies()

    get_movie_name = input("Enter movie name: ")
    if get_movie_name in movies:
        while True:
            try:
                get_new_star = float(input("Enter new movie rating: "))
                for movie, infos in movies.items():
                    if get_movie_name.lower() == movie.lower(): #case sensetive
                        storage.update_movie(get_movie_name, get_new_star)
                break
            except ValueError:
                print("Please enter number")
    else:
        print(f"Movie {get_movie_name} doesn't exist!")


def command_statistics():
    """ to show some statistics of films best film, worst, averate rating etc """

    # Get the data from the JSON file
    movies = storage.list_movies()

    # create temporary list
    movie_rates_list = []

    for movie, infos in movies.items():
        rate = infos["rating"]
        movie_rates_list.append(rate)

    average_rating = sum(movie_rates_list) / len(movie_rates_list)
    print(f"Average rating: {average_rating:.2f}") #:.2f for two decimal places
    reordered_movie_rates_list = sorted(movie_rates_list) #for sorting
    # at least 3 films to show median.
    if len(reordered_movie_rates_list) > 2:
      if len(reordered_movie_rates_list) % 2 == 0: #to check if its even
          calculate_median_for_even = (reordered_movie_rates_list[len(movie_rates_list) // 2] + reordered_movie_rates_list[len(movie_rates_list) // 2 + 1]) / 2 #method to find the median
          print(f"Median rating: {calculate_median_for_even}")
      else: # if not even so its odd and do for odd
          calculate_median_for_odd = reordered_movie_rates_list[len(movie_rates_list) // 2]
          print(f"Median rating: {calculate_median_for_odd}")
    best_movie = max(reordered_movie_rates_list) # to use the
    worst_movie = min(reordered_movie_rates_list)
    worst_movies_list = {}
    best_movies_list = {}
    #create new dict in order to show in one line if exist more than 1 highest rate.
    for movie, infos in movies.items():
        rate = infos["rating"]
        if rate == best_movie:
            if rate not in best_movies_list:
                best_movies_list[rate] = [movie]
            else:
                best_movies_list[rate].append(movie)
        elif rate == worst_movie:
            if rate not in worst_movies_list:
                worst_movies_list[rate] = [movie]
            else:
                worst_movies_list[rate].append(movie)

    for best_rate, best_movies in best_movies_list.items():
        if len(best_movies) > 1:
            print(f"Best movies: {', '.join(best_movies)} - {best_rate}")
        else:
            print(f"Best movie: {', '.join(best_movies)} - {best_rate}")

    for worst_rate, worst_movies in worst_movies_list.items():
        if len(worst_movies) > 1:
            print(f"Worst movies: {', '.join(worst_movies)} - {worst_rate}")
        else:
            print(f"Worst movie: {', '.join(worst_movies)} - {worst_rate}")


def show_enter_to_continue():
    """ just print to screen message """
    print()
    input("Press Enter to continue")


def command_random_movie():
    """
    works with random module, imported ,
    create a random number beetwen 0 and movies length then print random movie
    """
    movies = storage.list_movies()

    random_movie_id = random.randint(0,len(movies)-1)
    #because len(movies) return without counting 0 and indexes start from 0 we do -1
    rate_list = list(movies.keys())
    choose_random_movie = rate_list[random_movie_id] #choosing random key with indexing method
    for name, infos in movies.items():
        rate = infos["rating"]
        if name == choose_random_movie: #if name match with the random name then print it.
            print(f"Your movie for tonight: {name}, it's rated {rate}")


def command_search_movie():
    """ search movie by name """

    # Get the data from the JSON file
    movies = storage.list_movies()

    get_movie_name = input("Enter part of movie name: ")
    movie_name_list = []
    #everytime when runs also make the list empty
    for movie_name, infos in movies.items():
        rate = infos["rating"]
        # remove sensetive typing even its lowercase or uppercase match
        if get_movie_name.lower() in movie_name.lower():
            # add it to the list as tupple to includ key and value
            movie_name_list.append((movie_name, rate))
    if len(movie_name_list) > 0: #if added to the list show it
        for movie in movie_name_list:
            print(f"{movie[0]}, {movie[1]}")
    else: #if nothing founded and not added to list so list is 0 then show error message
        print(f"The movie {get_movie_name} doesn't exist.")
        suggest_similar_movies(movies, get_movie_name)


def suggest_similar_movies(movies, get_movie_name):
    """
    used fuzz module to show if has
    typing error suggest the films
    """
    suggestions = []
    for movie_name in movies.keys():
        score = fuzz.partial_ratio(movie_name.lower(), get_movie_name.lower())
        if score >= 75:  # at least match %
            suggestions.append((movie_name, score))
    if suggestions:
        print("Did you mean:")
        for name, score in suggestions:
            print(f"- {name}")
    else:
        print("No similar movie names found.")

def command_movies_sorted(sort_type):
    """
    sort type, by type sort the movies
    """

    movies = storage.list_movies()

    if sort_type == "rate":
        for movie_name, infos in sorted(movies.items(), key=lambda item: item[1][sort_type], reverse=True):
            rate = infos.get("rating", "N/A")
            year = infos.get("year", "N/A")
            print(f"{movie_name} ({year} - {rate})")
    elif sort_type == "year":
        while True:
            get_sorted_order = input("Do you want the latest movie first? (Y/N) ")
            if get_sorted_order.lower() == "y":
                is_reserved = True
                break
            elif get_sorted_order.lower() == "n":
                is_reserved = False
                break
        for movie_name, infos in sorted(movies.items(), key=lambda item: item[1][sort_type], reverse=is_reserved):
            rate = infos.get("rating", "N/A")
            year = infos.get("year", "N/A")
            print(f"{movie_name} ({year} - {rate})")

def command_filter_movies():
    """filtering movies and print them"""
    # Get the data from the JSON file
    movies = storage.list_movies()

    #default: True if check conditions
    get_rate = True
    is_start_year = True
    is_end_year = True

    # default: True for check conditions
    has_rating = True
    has_start_year = True
    has_end_year = True

    while get_rate:
        try:
            get_minimum_rate = input("Enter minimum rating (leave blank for no minimum rating): ")
            if get_minimum_rate == "":
                has_rating = False
                minimum_rate = 0
                get_rate = False
            else:
                minimum_rate = float(get_minimum_rate)
                get_rate = False
        except ValueError:
            print("Invalid input. Please enter a valid rating.")


    while is_start_year:
        try:
            get_start_year = input("Enter start year (leave blank for no start year): ")
            if get_start_year == "":
                has_start_year = False
                is_start_year = False
            else:
                start_year = int(get_start_year)
                is_start_year = False
        except ValueError:
                print("Invalid input. Please enter a valid start year.")

    while is_end_year:
        try:
            get_end_year = input("Enter end year (leave blank for no start year): ")
            if get_end_year == "":
                has_end_year = False
                is_end_year = False
            else:
                end_year = int(get_end_year)
                is_end_year = False
        except ValueError:
                print("Invalid input. Please enter a valid end year.")
    print("Filtered Movies:")
    for movie_name, infos in movies.items():
        rate = infos.get("rating", "N/A")
        year = infos.get("year", "N/A")
        if has_rating:
            if rate >= minimum_rate:
                if has_start_year:
                    if year >= start_year:
                        if has_end_year:
                            if year <= end_year:
                                print(f"{movie_name}({year}), {rate}")
                        else:
                            print(f"{movie_name}({year}), {rate}")
                else:
                    if has_end_year:
                        if year <= end_year:
                            print(f"{movie_name}({year}), {rate}")
                    else:
                        print(f"{movie_name}({year}), {rate}")
        else:
            if has_start_year:
                if year >= start_year:
                    if has_end_year:
                        if year <= end_year:
                            print(f"{movie_name}({year}), {rate}")
                    else:
                        print(f"{movie_name}({year}), {rate}")
            else:
                if has_end_year:
                    if year <= end_year:
                        print(f"{movie_name}({year}), {rate}")
                else:
                    print(f"{movie_name}({year}), {rate}")

def command_generate_website(website_title):
    #function for design of html
    movie_grid = html_movie_grid()

    #filepath for base html as a template and a new generated html file.
    new_html_name = "./website/index.html"
    html_template_path = "website/index_template.html"

    with open(html_template_path, "r") as html_theme:
        html_template = html_theme.read()

    with open(new_html_name, "w") as new_index:
        replace_template = html_template.replace("__TEMPLATE_TITLE__", website_title)
        replace_template = replace_template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
        new_index.write(replace_template)
    #a message after a page is successfully generated.
    print("Website was generated successfully.")

def html_movie_grid():
    movies = storage.movies_data()
    """
    <li>
            <div class="movie">
                <img class="movie-poster" src="https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg">
                <div class="movie-title">The Dark Knight</div>
                <div class="movie-year">2008</div>
            </div>
    </li>
    """
    output = ''

    for movie in movies:
        movie_title = movie["title"]
        movie_year = movie["year"]
        movie_rate = movie["rating"]
        movie_poster = movie["poster"]

        output += '<li>'
        output += '<div class="movie">'
        output += f'<img class="movie-poster" src="{movie_poster}">'
        output += f'<div class="movie-title">{movie_title}</div>'
        output += f'<div class="movie-year">{movie_year}</div>'
        output += f'<div class="movie-rate">IMDB: {movie_rate}</div>'
        output += '</div>'
        output += '</li>'

    return output


def main():
    """
    classic main folder to run the program from here also data included.
    """
    user_menu() #call function user menu with parameter movies to get dict in function

if __name__ == "__main__":
    main()
