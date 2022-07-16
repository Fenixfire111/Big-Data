# Get-movies
The program determines the N highest rated films for each specified genre

## Usage
```sh
python3 get-movies.py [--N <n>]  [--genres <genres>] [--year_from <year_from>] [--year_to <year_to>] [--regexp <regexp>]
```
##### Options
|   Name    | Description | 
| :---        |    :----:   |
| ``` --N```      | number of top rated films       |
| ``` --genres```      | filtering by selected genres'       |
| ``` --year_from```      | filtering from this year       |
| ``` --year_to```      | filtering until this year      |
| ``` --regexp```      | filter (regular expression) on movie title      |
| ``` --help```      | information about using the program    |
All arguments are optional.
Movies are sorted according to the following criteria:
1. rating desc
2. year desc
3. title asc

## Config
    [Files]
    # path to file movies.csv
    movies_file_path = data/movies.csv
    # path to file ratings.csv
    ratings_file_path = data/ratings.csv
    [CSV]
    # delimiter in csv file
    delimiter = ,
    # character encoding standard
    encoding = utf-8
    # output data names
    headers = genre,title,year,rating
    [Regexp]
    # regular expression for year
    re_year = \(\d+\) 

## Examples
Displays all movies:

    python3 get-movies.py
Displays the top 50 films of genres action, drama, documentary from 2015 to 2016 with the search for the substring "All" in the title:

    python3 get-movies.py --N 50 --genres "Action|Drama|Documentary" --year_from 2015 --year_to 2016 --regexp .*All.*

