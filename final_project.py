###     Name: Hang Song   ###
### Unique Name: hangsong ###
from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains my API key
import sqlite3

TOP250_URL = "https://www.imdb.com/chart/top/"
BASE_URL = "https://www.imdb.com"
CACHE_FILENAME = "fp_cache.json"
CACHE_DICT = {}
# consumer_key = secrets.CONSUMER_KEY
# consumer_secret = secrets.CONSUMER_SECRET

# Part 1: Read data from a database called IMDB.sqlite
DBNAME = 'favmovie.sqlite'
movie_history = []

def init_fav_db():
    '''
    Create a database with Table "Movies", "MovieRatings"
    with different fields ("Id", "MovieName","Year","MovieRating","Genra","Movie_Length","Score","Director","Stars")
    Parameters
    ----------
    None

    Return
    -----------
    None
    '''
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    drop_movies = '''
        DROP TABLE IF EXISTS "Movies";
    '''

    create_movies = '''
        CREATE TABLE IF NOT EXISTS "Movies" (
            "Id"        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "MovieName"  TEXT NOT NULL,
            "Year" INTEGER,
            "MovieRating"  TEXT,
            "Genre"  TEXT,
            "MovieLength"  TEXT,
            "Score"  REAL NOT NULL,
            "Director"    TEXT NOT NULL,
            "Stars"    TEXT NOT NULL
        );
    '''

    drop_movieratings = '''
        DROP TABLE IF EXISTS "MovieRatings";
    '''

    create_movieratings = '''
        CREATE TABLE IF NOT EXISTS "MovieRatings" (
            "Id"        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "Name"  TEXT NOT NULL,
            "Full"  TEXT NOT NULL,
            "Discription" TEXT NOT NULL
        );
    '''

    insert_movieratings = '''
        INSERT INTO MovieRatings
        VALUES (NULL,?,?,?);
        '''
    insertion_G = ['G','General Audiences', 'This program is designed to be appropriate for all ages. This rating indicates a film contains nothing that would offend parents for viewing by children.']
    insertion_PG = ['PG','Parental Guidance Suggested','Parents are urged to give parental guidance. This film may contain some material parents might not like for their young children.']
    insertion_PG13 = ['PG-13','Parents Strongly Cautioned','Some material may not be suited for children under age 13. May contain violence, nudity, sensuality, language, adult activities or other elements beyond a PG rating, but doesn’t reach the restricted R category.']
    insertion_R = ['R','Restricted','This rating is for films specifically designed to be viewed by adults and therefore may be unsuitable for children under 17.']
    insertion_NC17 = ['NC-17','Clearly Adult','This rating is applied to films the MPAA believes most parents will consider inappropriate for children 17 and under. It indicates only that adult content is more intense than in an R rated movie.']

    cur.execute(drop_movies)
    cur.execute(create_movies)
    cur.execute(drop_movieratings)
    cur.execute(create_movieratings)
    cur.execute(insert_movieratings,insertion_G)
    cur.execute(insert_movieratings,insertion_PG)
    cur.execute(insert_movieratings,insertion_PG13)
    cur.execute(insert_movieratings,insertion_R)
    cur.execute(insert_movieratings,insertion_NC17)
    conn.commit()
    conn.close()

def insert_fav_db(movie):
    '''
    Insert your favorite movie information in database for Table_movie
    
    Parameters
    ----------
    movie: Movie instance

    Return
    -----------
    None
    '''
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    stars = ', '.join(movie.stars)

    insertion = [movie.name, movie.year, movie.movie_rating, movie.genre, movie.length, movie.score, movie.director, stars]

    statement = '''
        INSERT INTO Movies ('MovieName','Year','MovieRating','Genre','MovieLength','Score','Director','Stars')
        VALUES (?,?,?,?,?,?,?,?);
        '''
    movie_uniq = f"{movie.name} ({movie.year})"
    if movie_uniq not in movie_history:
        cur.execute(statement,insertion)
        conn.commit()
        movie_history.append(movie_uniq)  # Record the movie to make sure we won't add duplicate records in database

    conn.close()



class Movie:
    '''a movie

    Instance Attributes
    -------------------

    name: string
        the name of the movie (e.g. "The Godfather")
    
    year: int
        the year of the movie released (e.g. 1994)

    movie_rating: string
        the film rating (e.g. 'R')
    
    genre: string
        the genre (e.g. 'comedy')

    
    lenth: string
        the film length (e.g. '2h 22min')

    score: float
        the IMDb rating for the movie (e.g. 9.2)

    director: string
        the director of the movie
    
    stars: list of strings
        the actors and actress in the movie
    
    description: string
        The synopsis of the movie

    '''
    def __init__(self, name, year, movie_rating, genre, length, score, director, stars, description):
        self.name = name
        self.year = year
        self.movie_rating = movie_rating
        self.genre = genre
        self.length = length
        self.score = score
        self.director = director
        self.stars = stars
        self.description = description

    def info(self):
        stars = ', '.join(self.stars)
        return f"{self.name} ({self.year}) [{self.movie_rating}] is directed by {self.director} and played by {stars}. Total movie length is {self.length}"

    def story(self):
        return f"{self.description}"

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

def make_request_with_cache(url):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.

    Parameters
    ----------
    url: string

    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    CACHE_DICT = open_cache()

    if (url in CACHE_DICT.keys()):
        print("Using Cache")
        return CACHE_DICT[url]
    else:
        print("Fetching")
        response = requests.get(url)
        CACHE_DICT[url] = response.text
        save_cache(CACHE_DICT)
        return CACHE_DICT[url]

def build_movie_url_dict():
    ''' Make a dictionary that maps ranking to movie page url

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a movie ranking in IMDb and value is the url
        e.g. {1:'https://www.imdb.com/title/tt0111161/', ...}
    '''
    main_url = TOP250_URL
    url_text = make_request_with_cache(main_url)
    soup = BeautifulSoup(url_text, 'html.parser')

    movie_url_dict = {}
 
    movie_list_parent = soup.find('tbody',class_ = 'lister-list')
    movie_list_child = movie_list_parent.find_all('tr')
    iterator = 1
    for section in movie_list_child:
        movie = section.find('td',class_='titleColumn')
        movie_tag = movie.find('a')
        movie_relative_path = movie_tag['href']
        movie_url = BASE_URL+ movie_relative_path
        movie_url_dict[iterator] = movie_url
        iterator = iterator + 1

    return movie_url_dict

def create_movie_instance(movie_url):
    '''Make an instance from movie URL.

    Parameters
    ----------
    movie_url: string
        The URL for a specific movie (Within range 250)

    Returns
    -------
    instance
        a Movie instance
    '''
    url_text = make_request_with_cache(movie_url)
    soup = BeautifulSoup(url_text, 'html.parser')
    title_section = soup.find('div',class_='title_wrapper')
    name = title_section.find('h1').find(text=True,recursive=False).strip()
    year = int(title_section.find('a').text)
    movie_rating = soup.find('div',class_='subtext').find(text=True,recursive=False).strip()

    genre_list = soup.find('div',class_='subtext').find_all('a') #There might be multiple genre in it
    genre_list.pop() #Remove the last item release dates
    clean_list = []
    for i in genre_list:
        i = i.text
        clean_list.append(i)
    genre = ''
    genre = ', '.join(clean_list)



    length = soup.find('div',class_='subtext').find('time').text.strip()
    score = float(soup.find('span',itemprop='ratingValue').text)

    people_section = soup.find_all('div',class_='credit_summary_item')
    director = people_section[0].find('a').text

    star_list = []
    stars = people_section[-1].find_all('a')
    for star in stars:
        star_list.append(star.text)
    star_list.pop() #remove the last useless info which is "see full_cast & crew"

    # lowest level in HTML that captures the JS data
    summary = soup.find(class_='title-overview')
    # get the summary text
    description = summary.find(class_='summary_text').text.strip()

    movie_instance = Movie(name=name, year=year,movie_rating=movie_rating, genre=genre, length=length, score=score, director=director,stars=star_list,description=description)
    return movie_instance

def display_top(num):
    response = requests.get(TOP250_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    titlecolumn_list = soup.find_all('td',class_='titleColumn')
    movie_list = []
    for row in titlecolumn_list:
        name = row.find('a').text
        year = row.find('span').text
        title = f'{name} {year}'
        movie_list.append(title)

    iters = 1
    print(f"Top {num} Movies are displayed below")
    print("-"*100)
    for movie in movie_list[:num]:
        print(f"{iters}. ",end='')
        print(movie)
        iters = iters+1

def show_star_more(star):
    pass


def interactive_design():
    user_input = ''
    while user_input != 'exit':
        user_input = input("Please enter a number (between 1 to 250) to display top IMDb movies, or 'exit' to leave: ")
        if user_input == 'exit':
            break
        if not user_input.isnumeric() or int(user_input)>250 or int(user_input)<1:
            print('Invalid Input')
            continue
        display_top(int(user_input))
    

        print("-"*100)
        print("Which Movie you want to see detailed information?")
        user_input2 =''
        while user_input2 !='exit':
            user_input2 = input("Please enter a movie number (between 1 to 250) to find out more detailed information, enter return to go back upper level, enter exit to leave: ")
            if user_input2 == 'return':
                break
            if user_input2 == 'exit':
                exit()
            if not user_input2.isnumeric() or int(user_input2)>250 or int(user_input2)<1:
                print('Invalid Input')
                continue
            movie = create_movie_instance(imdb_dict[int(user_input2)])
            print(movie.info())

            print('-'*100)
            print("Want more information of the movie or related actors?")
            user_input3 =''
            while user_input3 !='exit':
                # Need change here
                user_input3 = input('''For more detailed information for the movie, enter 'summary' for plot summary, enter 'save' to save the movie records in your personalized database, enter 'return' to go back to upper level, or enter 'exit' to end the program: ''')
                print("-"*100)
                if user_input3 == 'return':
                    break
                elif user_input3 == 'exit':
                    exit()
                elif user_input3 == 'summary':
                    print()
                    print(movie.story())
                    print("-"*100)
                elif user_input3 in movie.stars:
                    print()
                elif user_input3 == 'save':
                    # Save the movie to the personalized database
                    insert_fav_db(movie)
                    print("You have successfully saved this movie in your favorite movie database.")
        
                else:
                    print("Invalid Input")
                    continue



if __name__ == "__main__":
    # Create IMDB_dict--------------------------------------------------------------------------------------
    imdb_dict = build_movie_url_dict()
    # print(imdb_dict)

    # Start the program ------------------------------------------------------------------------------------
    interactive_design()



    # print(imdb_dict)
    init_fav_db()
    movie1 = create_movie_instance(imdb_dict[1])
    movie2 = create_movie_instance(imdb_dict[2])
    movie30 = create_movie_instance(imdb_dict[30])
    movie44 = create_movie_instance(imdb_dict[44])

    # print(type(movie1.score))
    insert_fav_db(movie1)
    insert_fav_db(movie2)
    insert_fav_db(movie30)
    insert_fav_db(movie44)
    insert_fav_db(movie1)
    insert_fav_db(movie2)
  

    # print(movie1.length)
    # print(movie1.info())
    # print(movie1.story())
    # response = input("Do you want to lanuch the interactive program for IMDB Top 250? Enter Yes to continue: ")
    # if response =="Yes":
    #     interactive_design()
    # init_db()




