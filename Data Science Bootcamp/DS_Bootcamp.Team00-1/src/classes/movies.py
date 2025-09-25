#!/usr/bin/env python3
import re
from collections import Counter


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file: str, limit: int = 1000):
        """
        Put here any fields that you think you will need.
        """
        self.path = path_to_the_file
        self.limit = limit
        self.data = []
        self._load_data()

    def _load_data(self) -> None:
        with open(self.path, mode="r", encoding="utf-8") as f:
            next(f)  # skip file header
            for i, line in enumerate(f):
                if i >= self.limit:
                    break
                parts = self.parse_columns(line.strip())
                record = {
                    "movieId": parts[0],
                    "title": parts[1],
                    "genres": parts[2].split("|"),
                }
                self.data.append(record)

    @staticmethod
    def parse_columns(line: str) -> list[str]:
        """
        The method for dividing a line into three columns
        """
        result_list = []
        current_column = []
        in_quotes = False

        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == "," and not in_quotes:
                result_list.append("".join(current_column).strip())
                current_column = []
            else:
                current_column.append(char)

        result_list.append("".join(current_column).strip())
        while len(result_list) < 3:
            result_list.append("")

        return result_list

    def dist_by_release(self) -> dict[int, int]:
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        year_count = Counter()
        for record in self.data:
            title = record["title"]
            found_year = re.findall(r"\d+", title)
            if found_year:
                year = int(found_year[-1])  # take last item - year
                year_count[year] += 1
        return dict(year_count.most_common())

    def dist_by_genres(self) -> dict[str, int]:
        """
           The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        genre_count = Counter()
        for record in self.data:
            for genre in record["genres"]:
                genre_count[genre] += 1
        return dict(genre_count.most_common())

    def most_genres(self, n: int) -> dict[str, int]:
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        if type(n) is not int or n <= 0:
            raise ValueError("n must be positive integer")

        top_movies = {}
        for record in self.data:
            movie_title = record["title"]
            num_of_genres = len(record["genres"])
            top_movies[movie_title] = num_of_genres
        return dict(sorted(top_movies.items(), key=lambda x: x[1], reverse=True)[:n])

    # bonus
    def most_common_words_in_titles(self, n: int = 10) -> dict[str, int]:
        """
        The method returns a dict with the most common words in movie titles.
        The keys are words, and the values are their counts.
        Sort it by counts descendingly.
        """
        word_count = Counter()
        for record in self.data:
            title = record["title"]
            title = self.get_movie_title_without_year(title)
            words = re.findall(r"\b\w+\b", title.lower())
            word_count.update(words)
        return dict(word_count.most_common(n))

    @staticmethod
    def get_movie_title_without_year(title):
        if re.findall(r"\d+", title):
            year = re.findall(r"\d+", title)[-1]
        else:
            year = None
        title = title.replace(f"({year})", "")
        return title
