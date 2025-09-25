#!/usr/bin/env python3
import requests
import re
import os
from bs4 import BeautifulSoup
from collections import Counter
from .movies import Movies


class Links:
    """
    Analyzing data from links.csv
    """

    class Movie:
        def __init__(self, movie_id):
            self.movie_id = movie_id
            self.name = None
            self.year = None
            self.rating = None
            self.director = None
            self.budget = None
            self.wwgross = None
            self.runtime = None
            self.origin_country = None

    def __init__(self, path_to_the_file, number_of_movies, temp_filename):
        number_of_movies += 1
        with open(path_to_the_file, "r", encoding="utf-8") as file:
            reader = file.readlines()
            # Сохраняем данные в формате: {movieId: imdbId}
            self.links_data = {
                int(line.split(",")[0]): (line.split(",")[1])
                for line in reader[1:number_of_movies]
            }
        self.list_of_movies = []
        self.number_of_movies = number_of_movies
        self.temp_filename = temp_filename
        self.fill_fields()
        self.get_movie_title_and_year(f"{os.path.dirname(path_to_the_file)}/movies.csv")

    def get_movie_title_and_year(self, path_to_the_file):
        with open(path_to_the_file, "r", encoding="utf-8") as f:
            next(f)
            iterator = 1
            for line in f:
                if iterator == self.number_of_movies:
                    break
                movie_id = line.split(",")[0]
                part = Movies.parse_columns(line)[1]
                if re.findall(r"\d+", part):
                    year = re.findall(r"\d+", part)[-1]
                else:
                    year = None
                title = part.replace(f"({year})", "")
                for movie in self.list_of_movies:
                    if int(movie_id) == int(movie.movie_id):
                        movie.year = year
                        if "," not in title:
                            movie.name = title.strip()
                iterator += 1

    @staticmethod
    def get_only_int(s):
        digits = re.sub(r"\D", "", s)
        return int(digits) if digits else 0

    def fill_fields(self):

        def check_the_movies():
            existing_movies = set()
            try:
                with open(self.temp_filename, "r", encoding="utf-8") as f:
                    next(f)
                    existing_movies = {line.split(",")[0].strip('"') for line in f}
                return existing_movies
            except FileNotFoundError:
                return set()

        def save_to_csv(self):
            """
            Saves movie data to a CSV file.
            If the movie already exists in the file, it is not added.
            """
            header = [
                "movie_id",
                "name",
                "rating",
                "director",
                "budget",
                "wwgross",
                "runtime",
                "origin_country",
            ]

            file_exists = False
            try:
                with open(
                    self.temp_filename, mode="r", newline="", encoding="utf-8"
                ) as file:
                    header_file = file.readline()
                    if header_file.strip('"').strip().split(",") == header:
                        file_exists = True
            except FileNotFoundError:
                pass
            existing_movies = check_the_movies()
            with open(self.temp_filename, mode="a", newline="", encoding="utf-8") as f:

                if not file_exists:
                    f.write(",".join(header) + "\n")

                for movie in self.list_of_movies:
                    if str(movie.movie_id) not in existing_movies:
                        country = (
                            movie.origin_country if movie.origin_country else ["N/A"]
                        )
                        row = [
                            str(movie.movie_id),
                            (
                                f'"{movie.name}"'
                                if "," in str(movie.name)
                                else str(movie.name)
                            ),
                            str(movie.rating),
                            str(movie.director),
                            str(movie.budget) if movie.budget is not None else "",
                            str(movie.wwgross) if movie.wwgross is not None else "",
                            str(movie.runtime) if movie.runtime is not None else "",
                            "|".join(country),
                        ]
                        f.write(",".join(row) + "\n")
                        existing_movies.add(str(movie.movie_id))

        def load_from_csv(self):
            """
            Reads movie data from a CSV file and populates the list_of_movies.
            The list is sorted by movie_id.
            """
            self.list_of_movies = []
            try:
                with open(
                    self.temp_filename, mode="r", newline="", encoding="utf-8"
                ) as f:
                    iterator = 1
                    next(f)
                    for line in f:
                        if iterator == self.number_of_movies:
                            break
                        parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', line.strip())

                        movie = Links.Movie(int(parts[0]))
                        movie.name = (
                            parts[1].strip('"').strip()
                            if parts[1].startswith('"')
                            else parts[1].strip()
                        )
                        movie.rating = parts[2] if parts[2] != "" else None
                        movie.director = parts[3] if parts[3] != "" else None
                        movie.budget = (
                            int(parts[4]) if parts[4] and parts[4] != "" else None
                        )
                        movie.wwgross = (
                            int(parts[5]) if parts[5] and parts[5] != "" else None
                        )
                        movie.runtime = parts[6] if parts[6] != "" else None
                        movie.origin_country = (
                            tuple(parts[7].split("|")) if parts[7] != "N/A" else ()
                        )

                        self.list_of_movies.append(movie)
                        iterator += 1

                    self.list_of_movies.sort(key=lambda x: x.movie_id)
            except FileNotFoundError:
                print(
                    f"File {self.temp_filename} not found. Starting with empty dataset."
                )
            except Exception as e:
                print(f"An error occurred while reading the CSV file: {e}")

        def get_soup(imdbId):
            url = f"https://www.imdb.com/title/tt{imdbId}/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            try:
                response = requests.get(url, headers=headers, timeout=30)
                if response.raise_for_status():
                    print(response.raise_for_status())
                    return None
                return BeautifulSoup(response.text, "html.parser")
            except requests.exceptions.Timeout:
                print(f"Request timed out for IMDb ID: {imdbId}")
                return None
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url}: {str(e)}")
                return None

        def parse_the_imdb(self):
            existing_movies = check_the_movies()
            if existing_movies:
                load_from_csv(self)
            for MovieId, imdbId in self.links_data.items():
                if not existing_movies or (str(MovieId) not in existing_movies):
                    print(f"proccesing movie id : {MovieId}")
                    movie = Links.Movie(MovieId)
                    soup = get_soup(imdbId)
                    if soup:
                        # get title
                        title_element = soup.find(
                            "div", {"class": "sc-ec65ba05-1 fUCCIx"}
                        )
                        if title_element:
                            movie.name = title_element.text[16:].strip()
                        else:
                            title_element = soup.find(
                                "span", {"class": "hero__primary-text"}
                            )
                            if title_element:
                                movie.name = title_element.text.strip()
                        # get rating
                        rating_element = soup.find(
                            "div", {"data-testid": "hero-rating-bar__aggregate-rating"}
                        )
                        if rating_element:
                            movie.rating = rating_element.text[11:14]
                        # get director
                        director_element = soup.find(
                            "div",
                            {"class": "ipc-metadata-list-item__content-container"},
                        )
                        if director_element:
                            movie.director = director_element.text.strip()
                        # get budget
                        budget_element = None
                        for element in soup.find_all(
                            "li", {"class": "ipc-metadata-list__item"}
                        ):
                            label = element.find(
                                "span", {"class": "ipc-metadata-list-item__label"}
                            )
                            if label and "Budget" in label.text:
                                budget_element = element.find(
                                    "span",
                                    {
                                        "class": "ipc-metadata-list-item__list-content-item"
                                    },
                                )
                                break
                        if (
                            budget_element
                            and "$" in budget_element.text
                            and not "A$" in budget_element.text
                        ):
                            movie.budget = self.get_only_int(budget_element.text)
                        # get gross
                        for element in soup.find_all("li", {"role": "presentation"}):
                            label = element.find(
                                "span", {"class": "ipc-metadata-list-item__label"}
                            )
                            if label and "Gross worldwide" in label.text:
                                gross_element = element.find(
                                    "span",
                                    {
                                        "class": "ipc-metadata-list-item__list-content-item"
                                    },
                                )
                                break
                        else:
                            gross_element = None
                        if gross_element:
                            movie.wwgross = self.get_only_int(gross_element.text)
                        # get runtime
                        for element in soup.find_all("li", {"role": "presentation"}):
                            label = element.find(
                                "span", {"class": "ipc-metadata-list-item__label"}
                            )
                            if label and "Runtime" in label.text:
                                runtime_element = element.find(
                                    "div",
                                    {
                                        "class": "ipc-metadata-list-item__content-container"
                                    },
                                )
                                break
                        if runtime_element:
                            movie.runtime = runtime_element.text.strip()
                        # get Country of origin
                        origin_country_element = soup.find(
                            "li", {"data-testid": "title-details-origin"}
                        )
                        if origin_country_element:
                            # Находим все теги <a> внутри контейнера
                            country_links = origin_country_element.find_all(
                                "a",
                                {
                                    "class": "ipc-metadata-list-item__list-content-item--link"
                                },
                            )
                            movie.origin_country = tuple(
                                link.text.strip() for link in country_links
                            )
                        else:
                            movie.origin_country = ("N/A",)
                        # Вывод информации о фильме
                        # print("-" * 40)
                        # print(f"Movie ID: {movie.movie_id}")
                        # print(f"Name: {movie.name}")
                        # print(f"Rating: {movie.rating}")
                        # print(f"Director: {movie.director}")
                        # print(f"Budget: {movie.budget}")
                        # print(f"Gross worldwide: {movie.wwgross}")
                        # print(f"Runtime: {movie.runtime}")
                        # print(f"Countries of origin: {movie.origin_country}")
                        # print("-" * 40)
                        self.list_of_movies.append(movie)
                        save_to_csv(self)

        parse_the_imdb(self)

    # main funcs

    def get_imdb(self, Movies_ids: list[str]) -> list[list[str]]:
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
                For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
                The values should be parsed from the IMDB webpages of the movies.
             Sort it by movieId descendingly.
        """
        imdb_info = []
        for movie in self.list_of_movies:
            if str(movie.movie_id) in [str(i) for i in Movies_ids]:
                temp_list = [
                    movie.movie_id,
                    movie.name,
                    movie.year,
                    movie.rating,
                    movie.director,
                    movie.budget,
                    movie.wwgross,
                    movie.runtime,
                    movie.origin_country,
                ]
                imdb_info.append(temp_list)
        return sorted(imdb_info, key=lambda x: x[0], reverse=True)

    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        directors = []
        for movie in self.list_of_movies:
            directors.append(movie.director)
        return dict(Counter(directors).most_common(n))

    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        movies = [movie for movie in self.list_of_movies if movie.budget]
        sorted_movies = sorted(movies, key=lambda x: int(x.budget), reverse=True)
        return {movie.name: f"{movie.budget}$" for movie in sorted_movies[:n]}

    def most_profitable(self, n):
        """
           The method returns a dict with top-n movies where the keys are movie titles and
           the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        movies = [
            movie for movie in self.list_of_movies if movie.budget and movie.wwgross
        ]
        sorted_movies = sorted(
            movies, key=lambda x: int(x.wwgross) - int(x.budget), reverse=True
        )
        return {
            movie.name: f"{movie.wwgross - movie.budget}$"
            for movie in sorted_movies[:n]
        }

    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
        Sort it by runtime descendingly.
        """

        def parse_runtime(runtime_str):
            """
            Auxiliary function for duration parsing.
            Accepts a string in the format "x hours y minutes" or "y minutes"
            and returns the total number of minutes.
            """
            if not runtime_str or not isinstance(
                runtime_str, str
            ):  # Проверяем, что строка существует и является строкой
                return 0

            digits = re.sub(r"[^\d\s]", "", runtime_str)
            parts = digits.split()
            if len(parts) == 1:
                try:
                    return int(parts[0])
                except ValueError:
                    return 0
            elif len(parts) == 2:
                try:

                    return int(parts[0]) * 60 + int(parts[1])
                except ValueError:
                    return 0
            else:
                return 0

        movies = [movie for movie in self.list_of_movies if movie.runtime]

        sorted_movies = sorted(
            movies, key=lambda x: parse_runtime(x.runtime), reverse=True
        )

        return {movie.name: movie.runtime for movie in sorted_movies[:n]}

    def top_cost_per_minute(self, n):
        """
                The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it.
             The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        movies = [
            movie for movie in self.list_of_movies if movie.budget and movie.runtime
        ]
        sorted_movies = sorted(
            movies,
            key=lambda x: x.budget
            / (int(x.runtime[0]) * 60 + self.get_only_int(x.runtime[6:])),
            reverse=True,
        )
        return {
            movie.name: round(
                movie.budget
                / (int(movie.runtime[0]) * 60 + self.get_only_int(movie.runtime[6:])),
                2,
            )
            for movie in sorted_movies[:n]
        }

    # bonus funcs
    def movies_by_country(self, n):
        """
        Returns top-n countries of origin by number of movies.
        """
        country_count = {}
        for movie in self.list_of_movies:
            if movie.origin_country:
                for country in movie.origin_country:
                    if country not in country_count:
                        country_count[country] = 0
                    country_count[country] += 1

        return dict(sorted(country_count.items(), key=lambda x: x[1], reverse=True)[:n])

    def top_directors_by_total_gross(self, n):
        """
        Returns top-n directors by total worldwide gross of their movies.
        """
        director_gross = {}
        for movie in self.list_of_movies:
            if movie.director and movie.wwgross:
                if movie.director not in director_gross:
                    director_gross[movie.director] = 0
                director_gross[movie.director] += int(movie.wwgross)

        return dict(
            sorted(director_gross.items(), key=lambda x: x[1], reverse=True)[:n]
        )

    def top_directors_by_average_rating(self, n, number_of_movies):
        """
        Returns the top n directors by the average rating of their films.
        """
        director_ratings = {}
        director_movie_counts = {}

        for movie in self.list_of_movies:
            if movie.director and movie.rating:
                if movie.director not in director_ratings:
                    director_ratings[movie.director] = 0
                    director_movie_counts[movie.director] = 0

                director_ratings[movie.director] += float(movie.rating)
                director_movie_counts[movie.director] += 1

        for director in director_ratings.keys():
            director_ratings[director] /= director_movie_counts[director]

        directors_with_info = [
            (director, rating, director_movie_counts[director])
            for director, rating in director_ratings.items()
        ]

        sorted_directors = sorted(
            filter(lambda x: x[2] >= number_of_movies, directors_with_info),
            key=lambda x: x[1],
            reverse=True,
        )

        return {item[0]: (item[1], item[2]) for item in sorted_directors[:n]}

    def top_countries_by_average_rating(self, n, number_of_movies):
        """
        Returns the top n countries based on the average rating of films created in these countries.
        """
        country_ratings = {}
        country_movie_counts = {}

        for movie in self.list_of_movies:
            if movie.origin_country and movie.rating:
                for country in movie.origin_country:
                    if country not in country_ratings:
                        country_ratings[country] = 0
                        country_movie_counts[country] = 0

                    country_ratings[country] += float(movie.rating)
                    country_movie_counts[country] += 1

        for country in country_ratings.keys():
            country_ratings[country] /= country_movie_counts[country]

        countries_with_info = [
            (country, rating, country_movie_counts[country])
            for country, rating in country_ratings.items()
        ]

        sorted_countries = sorted(
            filter(lambda x: x[2] >= number_of_movies, countries_with_info),
            key=lambda x: x[1],
            reverse=True,
        )

        return {item[0]: (item[1], item[2]) for item in sorted_countries[:n]}
