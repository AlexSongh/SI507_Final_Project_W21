#### Name: Hang Song ####
#### unique: hangsong ###



# IMDB Top Movies and Create Your Favorite Movie Database Program

## Data Sources:

IMDB Top 250: Main page[https://www.imdb.com/chart/top/] + 250 individual movie pages
(challenge score 8: Crawling [and scraping] multiple pages in a site you haven’t used before)
iTunes API
(challenge score 2: Web API you’ve used before)

## Packages required:
bs4, requests, sqlite3, json

## Description:
This code will show the top IMDb movies (ranging from 0 to 250). You can find detailed information of the movie, plot summary of the movie, and more representative movies of the stars in that movie using iTunes API requests. And also you can save the top 250 movies in your personalized movie database. Also a graphic summary (bar plot) will be provided for your database. For example, how many movies are in 1990s, how many movies are R rated, how many movies is starred by Tim Robbins, how may movies is directed by Christopher Nolan. 

## final_project.py:
Description: contains interactive program and other project code. 

### PROCESSING FUNCTIONS:

_init_fav_db()_: This function deletes any previous database containing tables "Movies", "MovieRatings", and reconstructs the tables with different necessary fields.

_insert_fav_db_: This function will update the information of the Movie instance in the Table "Movies". 

_open_cache()_: open the cache json file.

_save_cache()_: update the cache file when fetching new information that is not saved in the cache json previously.

_make_request_with_cache()_: Check the cache for a saved result for this baseurl+params:values combo. If the result is found, return it. Otherwise send a new request, save it, then return it

_build_movie_url_dict()_: Make a dictionary that maps ranking to movie page url

_create_movie_instance()_: Make a Movie instance from movie URL

_display_top()_: Display the top <num> results of the top movies in IMDb

_get_itunes_data()_: Get iTunes data from iTunes API based on the search and limit query

_show_star_more()_: Show more movies of the stars from the movie

_plot_time()_, _plot_rating()_,_plot_stars()_,_plot_director()_: draw barplot from a list of movie instances for diffrent categories.

_interactive_design()_: Main interactive program code



## User Guide:

### final_project.py:

Simply run the program. The instructions is also embedded in the interactive program as well.

#### Step 1:
Enter a number to tell the program how many results top movies to show.
Or enter "exit" to end the program.
#### Step 2:
Enter a specific number to show the detailed information of the movie;
Or enter "return" to go back to the upper level Step 1;
Or enter "exit" to end the program.
#### Step 3:
Enter "summary" for plot summary;
Or enter "stars" for more movies of the related stars;
Or enter "save" to save the movie in your favorite movie database called "favmovie.sqlite";
Or enter "showdb" to continue Step 4.
#### Step 4:
Enter "time" to show how many movies in each decade in your current database to get an insight of your movie taste;
Or enter "rating" to show movie_ratings of your favorite movies in movie database;
Or enter "stars" to show number of movies associated with the stars of the movies you saved in movie database;
Or enter "director" to show number of movies associated with directors of the movies you saved in movie database;
Or enter "return" to go back to the upper level Step 2;
Or enter "exit" to end the program.

Afterwards, you got a sqlite movie database stored the movies for your information.
