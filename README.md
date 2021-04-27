#### Name: Hang Song ####
#### unique: hangsong ###



# IMDB Top Movies and Create Your Favorite Movie Database Program

## Data Sources:

IMDB Top 250: [https://www.imdb.com/chart/top/][https://www.imdb.com/chart/top/]

## Packages required:
bs4, requests, sqlite3, json

## Description:
This code will show the top IMDb movies (ranging from 0 to 250). You can find detailed information of the movie, plot summary of the movie, and more representative movies of the stars in that movie using iTunes API requests. And also you can save the top 250 movies in your personalized movie database.

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

_interactive_design()_: Main interactive program code



## User Guide:

### final_project.py:

Simply run the program. The instructions is also embedded in the interactive program as well.

#### Step 1:
Enter a number to tell the program how many results top movies to show.
Or enter "exit" to end the program.

#### Step 2:
Enter a specific number to show the detailed information of the movie.
Or enter "return" to go back to the upper level Step 1;
Or enter "exit" to end the program.
#### Step 3:
Enter "summary" for plot summary
Or enter "stars" for more movies of the related stars
Or enter "save" to save the movie in your favorite movie database called "favmovie.sqlite"
Or enter "return" to go back to the upper level Step 2;
Or enter "exit" to end the program.

Afterwards, you got a sqlite movie database stored the movies for your information.
