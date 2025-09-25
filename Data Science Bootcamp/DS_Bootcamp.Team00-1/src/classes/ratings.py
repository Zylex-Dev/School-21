#!/usr/bin/env python3
import datetime
from collections import Counter, defaultdict
from .movies import Movies as M


class Ratings:
    """
    Analyzing data from ratings.csv
    """

    def __init__(
        self, path_to_ratings_file: str, path_to_movies_file: str, limit: int = 1000
    ) -> None:
        """
        Put here any fields that you think you will need.
        """
        self.joined_data = []
        self.limit = limit
        self._load_and_join_data(path_to_ratings_file, path_to_movies_file)

    def _load_and_join_data(self, ratings_file: str, movies_file: str) -> None:
        # load movies.csv file
        movies_dict = {}
        with open(movies_file, "r", encoding="utf-8") as f:
            header = f.readline()  # skip header
            for i, line in enumerate(f):
                if i >= self.limit:
                    break
                line = line.strip()
                parts = M.parse_columns(line)
                movie_id = int(parts[0])
                title = parts[1]
                genres = parts[2].split("|")
                movies_dict[movie_id] = {"title": title, "genres": genres}

        # load ratings.csv file
        with open(ratings_file, "r", encoding="utf-8") as f:
            header = f.readline()  # skip header
            for i, line in enumerate(f):
                if i >= self.limit:
                    break
                line = line.strip()
                parts = line.split(",")
                user_id = int(parts[0])
                movie_id = int(parts[1])
                rating = float(parts[2])
                timestamp = int(parts[3])
                movie_info = movies_dict.get(movie_id, {"title": None, "genres": None})
                record = {
                    "userId": user_id,
                    "movieId": movie_id,
                    "rating": rating,
                    "timestamp": timestamp,
                    "title": movie_info["title"],
                    "genres": movie_info["genres"],
                }
                self.joined_data.append(record)

    class Movies:
        def __init__(self, ratings_instance: "Ratings") -> None:
            self.data = ratings_instance.joined_data

        @staticmethod
        def _average(rating_values: list[float]) -> float:
            return sum(rating_values) / len(rating_values) if rating_values else 0.0

        @staticmethod
        def _median(rating_values: list[float]) -> float:
            if not rating_values:
                return 0.0
            sorted_ratings = sorted(rating_values)
            n = len(sorted_ratings)
            mid = n // 2
            if n % 2 == 0:
                return (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2
            else:
                return sorted_ratings[mid]

        @staticmethod
        def _variance(rating_values: list[float]) -> float:
            if not rating_values:
                return 0.0
            arithmetic_mean = Ratings.Movies._average(rating_values)
            x_squares = [(X - arithmetic_mean) ** 2 for X in rating_values]
            variance = Ratings.Movies._average(x_squares)
            return variance

        @property
        def metric_functions(self) -> dict[str, callable]:
            """
            A property that returns a dictionary, where the keys are the names of metrics, and the values are functions for calculating them.
            """
            return {
                "average": self._average,
                "median": self._median,
            }

        @staticmethod
        def get_date_from_timestamp(timestamp: int) -> int:
            dt = datetime.datetime.fromtimestamp(timestamp)
            return dt.year

        def dist_by_year(self) -> dict[int, int]:
            """
            The method returns a dict where the keys are years and the values are counts.
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            year_counts = Counter()
            for record in self.data:
                year = self.get_date_from_timestamp(record["timestamp"])
                year_counts[year] += 1
            return dict(sorted(year_counts.items()))

        def dist_by_rating(self) -> dict[float, int]:
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            rating_counts = Counter()
            for record in self.data:
                rating_counts[record["rating"]] += 1
            return dict(sorted(rating_counts.items()))

        def top_by_num_of_ratings(self, n: int) -> dict[str, int]:
            """
            The method returns top-n movies by the number of ratings.
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            if type(n) is not int:
                raise ValueError("n must be an integer")

            movie_rating_counts = Counter()
            movie_titles = {}
            for record in self.data:
                movie_id = record["movieId"]
                movie_rating_counts[movie_id] += 1
                movie_titles[movie_id] = record["title"]
            top_n = movie_rating_counts.most_common(n)
            return {movie_titles[movie_id]: count for movie_id, count in top_n}

        def top_by_ratings(self, n: int, metric: str = "average") -> dict[str, float]:
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            if metric not in self.metric_functions:
                raise ValueError(
                    f"Unsupported metric '{metric}'. Supported metrics are: {', '.join(self.metric_functions.keys())}"
                )

            if type(n) is not int:
                raise ValueError("n must be an integer")

            movie_ratings = defaultdict(list)
            movie_titles = {}
            for record in self.data:
                movie_ratings[record["movieId"]].append(record["rating"])
                movie_titles[record["movieId"]] = record["title"]

            result = {}
            for movie_id, ratings in movie_ratings.items():
                metric_value = self.metric_functions[metric](ratings)
                result[movie_titles[movie_id]] = round(metric_value, 2)

            sorted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True)[:n]
            )
            return sorted_result

        def top_controversial(self, n: int) -> dict[str, float]:
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
            Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            if type(n) is not int:
                raise ValueError("n must be an integer")

            movie_ratings = defaultdict(list)
            movie_titles = {}
            for record in self.data:
                movie_ratings[record["movieId"]].append(record["rating"])
                movie_titles[record["movieId"]] = record["title"]

            result = {}
            for movie_id, ratings in movie_ratings.items():
                variance_value = self._variance(ratings)
                result[movie_titles[movie_id]] = round(variance_value, 2)

            sorted_result = dict(
                sorted(result.items(), key=lambda x: x[1], reverse=True)[:n]
            )
            return sorted_result

        # bonus
        def dist_by_genre(self) -> dict[str, float]:
            """
            Returns a dictionary with genre as keys and average ratings as values.
            """
            genre_ratings = defaultdict(list)
            for record in self.data:
                if record["genres"] is not None:
                    for genre in record["genres"]:
                        genre_ratings[genre].append(record["rating"])

            result = {}
            for genre, ratings in genre_ratings.items():
                result[genre] = round(self._average(ratings), 2)

            return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    class Users(Movies):
        """
        In this class, three methods should work.
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
        Inherit from the class Movies. Several methods are similar to the methods from it.
        """

        def dist_by_num_of_user_ratings(self) -> dict[int, int]:
            user_rating_counts = Counter()
            for record in self.data:
                user_rating_counts[record["userId"]] += 1
            return dict(sorted(user_rating_counts.items()))

        def dist_by_user_ratings(self, metric: str = "average") -> dict[int, float]:
            if metric not in self.metric_functions:
                raise ValueError(
                    f"Unsupported metric '{metric}'. Supported metrics are: {', '.join(self.metric_functions.keys())}"
                )
            user_ratings = defaultdict(list)
            for record in self.data:
                user_ratings[record["userId"]].append(record["rating"])

            result = {}
            for user_id, ratings in user_ratings.items():
                metric_value = self.metric_functions[metric](ratings)
                result[user_id] = round(metric_value, 2)

            return dict(sorted(result.items()))

        def top_users_controversial(self, n: int) -> dict[int, float]:
            if type(n) is not int:
                raise ValueError("n must be an integer")

            user_ratings = defaultdict(list)
            for record in self.data:
                user_ratings[record["userId"]].append(record["rating"])

            result = {}
            for user_id, ratings in user_ratings.items():
                rating_variance = self._variance(ratings)
                result[user_id] = round(rating_variance, 2)
            return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:n])
