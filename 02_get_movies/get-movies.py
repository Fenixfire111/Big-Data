import argparse
import csv
import re
import sys
from collections import defaultdict
import configparser

"""create a parser for the config file"""
config = configparser.ConfigParser()
config.read("config.ini")

# delimiter in csv file
DELIMITER = config.get('CSV', 'delimiter')
# path to file movies.csv
MOVIES_FILE = config.get('Files', 'movies_file_path')
# path to file ratings.csv
RATINGS_FILE = config.get('Files', 'ratings_file_path')
# character encoding standard
ENCODING = config.get('CSV', 'encoding')
# output data names
HEADERS = config.get('CSV', 'headers').split(',')
# regular expression for year
RE_YEAR = config.get('Regexp', 're_year')


def main():
    # try:
        # get input data
        input_data = get_input_data()
        # get a dictionary with an average movie rating
        average_ratings = get_average_ratings()
        # get sorted array of movies
        sorted_movies = get_sorted_movies(average_ratings)
        # output the received data
        output_result_data(sorted_movies, input_data)

    # except Exception:
    #     sys.stderr = open('errors.txt', 'w')
    #     sys.stderr.write('the program ended incorrectly')
    #     print('the program ended incorrectly')
    #     sys.stderr.close()


def get_input_data():
    """create a parser to process command line arguments
    and get command line arguments"""
    arg_parser = argparse.ArgumentParser(
        description='The program determines the N highest rated films for each specified genre')
    arg_parser.add_argument('--N', nargs=1,
                            type=int,
                            metavar='<n>',
                            default=0,
                            help='number of top rated films')

    arg_parser.add_argument('--genres', nargs=1,
                            type=str,
                            metavar='<genres>',
                            default='',
                            help='filtering by selected genres')

    arg_parser.add_argument('--year_from', nargs=1,
                            type=int,
                            metavar='<year_from>',
                            default=0,
                            help='filtering from this year')

    arg_parser.add_argument('--year_to', nargs=1,
                            type=int,
                            metavar='<year_to>',
                            default=0,
                            help='filtering until this year')

    arg_parser.add_argument('--regexp', nargs=1,
                            type=str,
                            metavar='<regexp>',
                            default='',
                            help='filter (regular expression) on movie title')

    return arg_parser.parse_args()


def get_average_ratings():
    """create a dictionary of films and their average ratings"""
    average_ratings = defaultdict(float)
    number_ratings = defaultdict(int)
    with open(RATINGS_FILE, encoding=ENCODING) as input_file:
        input_data = csv.DictReader(input_file, delimiter=DELIMITER)
        # calculate the sum of all ratings and their number for each film
        for line in input_data:
            if all(line.values()):
                average_ratings[line['movieId']] += float(line['rating'])
                number_ratings[line['movieId']] += 1

    # calculate the average rating for each movie
    for movie_id, number in number_ratings.items():
        average_ratings[movie_id] = average_ratings[movie_id] / number

    return average_ratings


def transform_data(average_ratings, input_data):
    """create an array with movies from a dictionary
    and input data from a file with movie names"""
    movies = []
    # process line from file
    for line in input_data:
        genres = line['genres'].split('|')
        rating = average_ratings[line['movieId']]
        title = line['title'].strip()
        year = re.search(RE_YEAR, title)
        if year:
            # find the name of the movie and the year of creation
            title = re.sub(RE_YEAR, '', title).strip()
            year = int(year[0].strip('()'))
        # checking a string for empty data
        if (all((genres, title, year, rating))
                and genres[0] != '(no genres listed)'):
            # add a movie to the array as many times as there are genres
            for genre in genres:
                movies.append((genre, title, year, rating))

    return movies


def get_sorted_movies(average_ratings):
    """get sorted array of movies from dictionary with average ratings"""
    def sort_rule(value):
        # movie sorting rule
        _, title, year, rating = value
        return -rating, -year, title

    with open(MOVIES_FILE, encoding=ENCODING) as input_file:
        input_data = csv.DictReader(input_file, delimiter=DELIMITER)
        # convert dictionary to array
        movies = transform_data(average_ratings, input_data)

    # sort the array according to the rules
    movies = sorted(movies, key=sort_rule)
    return movies


def condition_check(line_counter, line, args):
    """check if the data matches the search criteria"""
    result = True

    genre, title, year, _ = line
    year_from, year_to = args.year_from[0], args.year_to[0]
    genres, regexp, n = args.genres[0], args.regexp[0], args.N[0]

    if args.year_from and result:
        result = (year >= year_from)
    if args.year_to and result:
        result = (year <= year_to)
    if args.genres and result:
        result = (genre in genres)
    if args.regexp and result:
        result = bool(re.findall(regexp, title))
    if args.N and result:
        result = (line_counter <= n)

    return result


def output_result_data(movies, args):
    """output data according to the conditions"""
    csv_writer = csv.writer(sys.stdout, delimiter=DELIMITER)
    csv_writer.writerow(HEADERS)

    line_counter = 1
    # output lines that match the conditions
    for line in movies:
        if condition_check(line_counter, line, args):
            csv_writer.writerow(line)
            line_counter += 1


if __name__ == '__main__':
    main()
