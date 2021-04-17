###     Name: Hang Song   ###
### Unique Name: hangsong ###
from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains my API key

TOP250_URL = "https://www.imdb.com/chart/top/"
BASE_URL = "https://www.imdb.com"
# BASE_URL = "https://www.nps.gov"
CACHE_FILENAME = "fp_cache.json"
CACHE_DICT = {}
# MAP_URL = "http://www.mapquestapi.com/search/v2/radius"

# consumer_key = secrets.CONSUMER_KEY
# consumer_secret = secrets.CONSUMER_SECRET



class Movie:
    '''a movie

    Instance Attributes
    -------------------

    name: string
        the name of the movie (e.g. "The Godfather")

    genre: string
        the genre (e.g. 'comedy')

    movie_rating: string
        the film rating (e.g. R)

    score: float
        the IMDb rating for the movie (e.g. 9.2)

    director: string
        the director of the movie
    
    stars: list of strings
        the actors and actress in the movie
    
    description: string
        The synopsis of the movie

    '''
    def __init__(self, name, year, movie_rating, genre, length, score, director, stars):
        self.name = name
        self.year = year
        self.movie_rating = movie_rating
        self.genre = genre
        self.length = length
        self.score = score
        self.director = director
        self.stars = stars
    
    def info(self):
        return f"{self.name} ({self.year}) is directed by {self.director}."

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
    year = title_section.find('a').text
    movie_rating = soup.find('div',class_='subtext').find(text=True,recursive=False).strip()
    genre = soup.find('div',class_='subtext').find('a').text
    length = soup.find('div',class_='subtext').find('time').text.strip()
    score = float(soup.find('span',itemprop='ratingValue').text)

    people_section = soup.find_all('div',class_='credit_summary_item')
    director = people_section[0].find('a').text

    star_list = []
    stars = people_section[-1].find_all('a')
    for star in stars:
        star_list.append(star.text)
    star_list.pop() #remove the last "see full_cast & crew"

    movie_instance = Movie(name=name, year=year,movie_rating=movie_rating, genre=genre, length=length, score=score, director=director,stars=star_list)
    return movie_instance



if __name__ == "__main__":
    imdb_dict = build_movie_url_dict()
    print(imdb_dict)
    movie1 = create_movie_instance(imdb_dict[1])
    print(movie1.info())





