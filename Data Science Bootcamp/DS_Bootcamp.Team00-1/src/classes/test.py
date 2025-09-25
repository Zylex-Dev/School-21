#!/usr/bin/env python3
import pytest
import os
from .links import Links
from .movies import Movies
from .ratings import Ratings
from .tags import Tags

# Текущая рабочая директория (откуда запущен скрипт)
current_working_directory = os.getcwd()
# Функция для поиска корня Git-репозитория


def find_git_root(start_dir):
    current_dir = os.path.abspath(start_dir)
    while True:
        if os.path.isdir(os.path.join(current_dir, ".git")):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Если достигли корня файловой системы
            raise FileNotFoundError("Корень Git-репозитория не найден")
        current_dir = parent_dir


# Начинаем поиск корня репозитория от директории скрипта
repo_root = find_git_root(os.path.dirname(os.path.abspath(__file__)))

# Путь к директории datasets в репозитории
datasets_path = os.path.join(repo_root, "datasets")

# Рассчитываем относительный путь от текущей рабочей директории до datasets
relative_path = os.path.relpath(datasets_path, current_working_directory)


@pytest.fixture
def movie_instance():
    movies_file_path = f"{relative_path}/movies.csv"
    return Movies(movies_file_path, limit=1000)


@pytest.fixture
def links_instance():
    links_file_path = f"{relative_path}/links.csv"
    temp_file = f"{repo_root}/src/classes/temp_data_from_imdb.csv"
    links = Links(links_file_path, number_of_movies=1000, temp_filename=temp_file)
    return links


@pytest.fixture
def ratings_instance():
    ratings_file_path = f"{relative_path}/ratings.csv"
    movies_file_path = f"{relative_path}/movies.csv"
    return Ratings(ratings_file_path, movies_file_path, limit=1000)


@pytest.fixture
def ratings_movies_instance(ratings_instance):
    return Ratings.Movies(ratings_instance)


@pytest.fixture
def ratings_users_instance(ratings_instance):
    return Ratings.Users(ratings_instance)


@pytest.fixture
def tags_instance():
    tags_file_path = f"{relative_path}/tags.csv"
    return Tags(tags_file_path, number_of_lines=1000)


@pytest.fixture
def movie_instance_with_sample_data(tmp_path):
    file_content = (
        "movieId,title,genres\n"
        "1,First Movie,Adventure|Comedy|Horror\n"
        "2,Second Movie,Horror|Adventure\n"
        "3,Third Movie,Adventure\n"
    )
    file_path = tmp_path / "test_movies.csv"
    file_path.write_text(file_content, encoding="utf-8")
    return Movies(str(file_path), limit=3)


@pytest.fixture
def ratings_instance_with_sample_data(tmp_path):
    movie_file_content = (
        "movieId,title,genres\n"
        "1,a,Adventure|Comedy|Horror\n"
        "2,b,Horror|Adventure\n"
        "3,c,Adventure\n"
    )
    ratings_file_content = (
        "userId,movieId,rating,timestamp"
        "1,1,1.0,964982703\n"
        "2,1,2.0,964981247\n"
        "3,1,3.0,964982224\n"
    )
    movie_file = tmp_path / "test_movies.csv"
    movie_file.write_text(movie_file_content, encoding="utf-8")

    ratings_file = tmp_path / "test_ratings.csv"
    ratings_file.write_text(ratings_file_content, encoding="utf-8")

    r = Ratings(str(ratings_file), str(movie_file), limit=3)
    return r.Movies(r)


@pytest.fixture
def tags_instance_with_sample_data(tmp_path):
    file_content = (
        "userId,movieId,tag,timestamp\n"
        "2,60756,funny,1445714994\n"
        "3,60756,funny,1445714996\n"
        "2,60756,cool,1445714992\n"
    )
    file_path = tmp_path / "test_tags.csv"
    file_path.write_text(file_content, encoding="utf-8")
    return Tags(str(file_path), number_of_lines=3)


class Test:
    # tests for Movies class
    def test_dist_by_release_type_and_sorting(self, movie_instance):
        result = movie_instance.dist_by_release()

        assert isinstance(result, dict)

        for key, value in result.items():
            assert isinstance(key, int)
            assert isinstance(value, int)

        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_dist_by_genres_type_and_sorting(self, movie_instance):
        result = movie_instance.dist_by_genres()

        assert isinstance(result, dict)

        for key, value in result.items():
            assert isinstance(key, str)
            assert isinstance(value, int)

        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_most_genres_type_sorting_and_n(self, movie_instance):
        n = 5
        result = movie_instance.most_genres(n)

        assert isinstance(result, dict)
        assert len(result) == n

        for key, value in result.items():
            assert isinstance(key, str)
            assert isinstance(value, int)

        values = list(result.values())
        assert values == sorted(values, reverse=True)

    def test_most_common_words_in_titles_type_and_sorting(self, movie_instance):
        n = 10
        result = movie_instance.most_common_words_in_titles(n)

        assert isinstance(result, dict)
        assert len(result) == n

        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, int)
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    # tests for Ratings class
    def test_dist_by_year_type_and_sorting(self, ratings_movies_instance):
        result = ratings_movies_instance.dist_by_year()

        assert isinstance(result, dict)
        years = list(result.keys())
        assert all(isinstance(year, int) for year in years)
        assert years == sorted(years)
        assert all(isinstance(count, int) for count in result.values())

    def test_dist_by_rating_type_and_sorting(self, ratings_movies_instance):
        result = ratings_movies_instance.dist_by_rating()

        assert isinstance(result, dict)
        rating_keys = list(result.keys())
        assert all(isinstance(i, float) for i in rating_keys)
        assert rating_keys == sorted(rating_keys)
        assert all(isinstance(i, int) for i in result.values())

    def test_top_by_num_of_ratings_type_sorting_and_n(self, ratings_movies_instance):
        n = 3
        result = ratings_movies_instance.top_by_num_of_ratings(n)
        assert isinstance(result, dict)
        assert len(result) == n
        for title, count in result.items():
            assert isinstance(title, str)
            assert isinstance(count, int)
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_top_by_num_of_ratings_non_integer(self, ratings_movies_instance):
        with pytest.raises(ValueError):
            ratings_movies_instance.top_by_num_of_ratings("2")

    def test_top_by_ratings_type_sorting_and_n(self, ratings_movies_instance):
        n = 3
        result = ratings_movies_instance.top_by_ratings(n)
        assert isinstance(result, dict)
        assert len(result) == n
        for title, value in result.items():
            assert isinstance(title, str)
            assert isinstance(value, float)
            assert value == round(value, 2)

    def test_top_by_ratings_invalid_metric(self, ratings_movies_instance):
        with pytest.raises(ValueError):
            ratings_movies_instance.top_by_ratings(2, metric="invalid")

    def test_top_by_ratings_non_integer(self, ratings_movies_instance):
        with pytest.raises(ValueError):
            ratings_movies_instance.top_by_ratings("2")

    def test_top_controversial_type_sorting_and_n(self, ratings_movies_instance):
        n = 5
        result = ratings_movies_instance.top_controversial(n)
        assert isinstance(result, dict)
        assert len(result) == n
        for title, value in result.items():
            assert isinstance(title, str)
            assert isinstance(value, float)
            assert value == round(value, 2)
        variances = list(result.values())
        assert variances == sorted(variances, reverse=True)

    def test_top_controversial_non_integer(self, ratings_movies_instance):
        with pytest.raises(ValueError):
            ratings_movies_instance.top_controversial("2")

    def test_dist_by_num_of_user_ratings_type_and_sorting(self, ratings_users_instance):
        result = ratings_users_instance.dist_by_num_of_user_ratings()
        assert isinstance(result, dict)
        for user_id, count in result.items():
            assert isinstance(user_id, int)
            assert isinstance(count, int)
        list_user_ids = list(result.keys())
        assert list_user_ids == sorted(list_user_ids)

    def test_dist_by_user_ratings_type_and_sorting(self, ratings_users_instance):
        result = ratings_users_instance.dist_by_user_ratings()
        assert isinstance(result, dict)
        user_ids = list(result.keys())
        assert all(isinstance(uid, int) for uid in user_ids)
        assert user_ids == sorted(user_ids)
        for value in result.values():
            assert isinstance(value, float)
            assert value == round(value, 2)

    def test_dist_by_user_ratings_invalid_metric(self, ratings_users_instance):
        with pytest.raises(ValueError):
            ratings_users_instance.dist_by_user_ratings(metric="invalid")

    def test_top_users_controversial_type_sorting_and_n(self, ratings_users_instance):
        n = 2
        result = ratings_users_instance.top_users_controversial(n)
        assert isinstance(result, dict)
        assert len(result) == n
        for uid, value in result.items():
            assert isinstance(uid, int)
            assert isinstance(value, float)
            assert value == round(value, 2)
        variances = list(result.values())
        assert variances == sorted(variances, reverse=True)

    def test_top_users_controversial_non_integer(self, ratings_users_instance):
        with pytest.raises(ValueError):
            ratings_users_instance.top_users_controversial("2")

    def test_dist_by_genre_type_and_sorting(self, ratings_movies_instance):
        result = ratings_movies_instance.dist_by_genre()

        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, str)
            assert isinstance(value, float)
        values = list(result.values())
        assert values == sorted(values, reverse=True)

    # tests for Links class
    def test_get_imdb_return_type_and_storing(self, links_instance):
        """
        Checks that get_imdb returns a list of lists,
        that the first element of each inner list (movieId) is an int,
        and that the list is sorted in descending order by movieId.
        """

        list_of_movies_id = ["2", "1", "3"]
        result = links_instance.get_imdb(Movies_ids=list_of_movies_id)
        assert isinstance(result, list)
        assert isinstance(result[0], list)
        for movie_info in result:
            assert isinstance(movie_info[0], int)
        movie_ids = [movie_info[0] for movie_info in result]
        assert movie_ids == sorted(movie_ids, reverse=True)

    def test_top_directors_return_type_and_sorting(self, links_instance):
        """
        Checks that top_directors returns a dict,
        that the keys are strings (director names),
        that the values are integers (number of movies),
        and that the dict is sorted by values in descending order.
        """
        n = 5
        result = links_instance.top_directors(n)

        assert isinstance(result, dict)
        for director, count in result.items():
            assert isinstance(director, str)
            assert isinstance(count, int)

        counts = [count for _, count in result.items()]
        assert counts == sorted(counts, reverse=True)

    def test_most_expensive_return_type_and_sorting(self, links_instance):
        """
        Checks that most_expensive returns a dict,
        that the keys are strings (movie titles),
        that the values are strings (budgets with a dollar sign),
        and that the dict is sorted by budgets in descending order.
        """
        n = 5
        result = links_instance.most_expensive(n)

        assert isinstance(result, dict)
        for title, budget in result.items():
            assert isinstance(title, str)
            assert isinstance(budget, str)
            assert budget.endswith("$")

        budgets = [int(budget.strip("$")) for budget in result.values()]
        assert budgets == sorted(budgets, reverse=True)

    def test_most_profitable_return_type_and_sorting(self, links_instance):
        """
        Checks that most_profitable returns a dict,
        that the keys are strings (movie titles),
        that the values are strings (profit with a dollar sign),
        and that the dict is sorted by profit in descending order.
        """
        n = 5
        result = links_instance.most_profitable(n)

        assert isinstance(result, dict)
        for title, profit in result.items():
            assert isinstance(title, str)
            assert isinstance(profit, str)
            assert profit.endswith("$")

        profits = [int(profit.strip("$")) for profit in result.values()]
        assert profits == sorted(profits, reverse=True)

    def test_longest_return_type_and_sorting(self, links_instance):
        """
        Checks that longest returns a dict,
        that the keys are strings (movie titles),
        that the values are strings (runtime),
        and that the dict is sorted by runtime in descending order.
        """
        n = 5
        result = links_instance.longest(n)

        assert isinstance(result, dict)
        for title, runtime in result.items():
            assert isinstance(title, str)
            assert isinstance(runtime, str)

        runtimes = [int(runtime.split()[0]) for runtime in result.values()]
        assert runtimes == sorted(runtimes, reverse=True)

    def test_top_cost_per_minute_return_type_and_sorting(self, links_instance):
        """
        Checks that top_cost_per_minute returns a dict,
        that the keys are strings (movie titles),
        that the values are floats (cost per minute),
        and that the dict is sorted by cost per minute in descending order.
        """
        n = 5
        result = links_instance.top_cost_per_minute(n)

        assert isinstance(result, dict)
        for title, cost in result.items():
            assert isinstance(title, str)
            assert isinstance(cost, float)

        costs = list(result.values())
        assert costs == sorted(costs, reverse=True)

    def test_movies_by_country_return_type_and_sorting(self, links_instance):
        """
        Checks that movies_by_country returns a dict,
        that the keys are strings (country names),
        that the values are integers (number of movies),
        and that the dict is sorted by the number of movies in descending order.
        """
        n = 5
        result = links_instance.movies_by_country(n)

        assert isinstance(result, dict)
        for country, count in result.items():
            assert isinstance(country, str)
            assert isinstance(count, int)

        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_top_directors_by_total_gross_return_type_and_sorting(self, links_instance):
        """
        Checks that top_directors_by_total_gross returns a dict,
        that the keys are strings (director names),
        that the values are integers (total worldwide gross),
        and that the dict is sorted by total gross in descending order.
        """
        n = 5
        result = links_instance.top_directors_by_total_gross(n)

        assert isinstance(result, dict)
        for director, gross in result.items():
            assert isinstance(director, str)
            assert isinstance(gross, int)

        gross_values = list(result.values())
        assert gross_values == sorted(gross_values, reverse=True)

    def test_top_directors_by_average_rating_return_type_and_sorting(
        self, links_instance
    ):
        """
        Checks that top_directors_by_average_rating returns a dict,
        that the keys are strings (director names),
        that the values are tuples (average rating, number of movies),
        and that the dict is sorted by average rating in descending order.
        """
        n = 5
        min_movies = 2
        result = links_instance.top_directors_by_average_rating(n, min_movies)

        assert isinstance(result, dict)
        for director, (rating, count) in result.items():
            assert isinstance(director, str)
            assert isinstance(rating, float)
            assert isinstance(count, int)

        ratings = [rating for rating, _ in result.values()]
        assert ratings == sorted(ratings, reverse=True)

    def test_top_countries_by_average_rating_return_type_and_sorting(
        self, links_instance
    ):
        """
        Checks that top_countries_by_average_rating returns a dict,
        that the keys are strings (country names),
        that the values are tuples (average rating, number of movies),
        and that the dict is sorted by average rating in descending order.
        """
        n = 5
        min_movies = 2
        result = links_instance.top_countries_by_average_rating(n, min_movies)

        assert isinstance(result, dict)
        for country, (rating, count) in result.items():
            assert isinstance(country, str)
            assert isinstance(rating, float)
            assert isinstance(count, int)

        ratings = [rating for rating, _ in result.values()]
        assert ratings == sorted(ratings, reverse=True)

    # tests for Tags class
    def test_most_words_type_and_sorting(self, tags_instance):
        result = tags_instance.most_words(n=3)
        assert isinstance(result, dict)
        for tag, count in result.items():
            assert isinstance(tag, str)
            assert isinstance(count, int)
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_longest_type_and_sorting(self, tags_instance):
        result = tags_instance.longest(n=3)
        assert isinstance(result, list)
        for tag in result:
            assert isinstance(tag, str)
        lengths = [len(tag) for tag in result]
        assert lengths == sorted(lengths, reverse=True)

    def test_most_words_and_longest_type_and_sorting(self, tags_instance):
        result = tags_instance.most_words_and_longest(n=3)
        assert isinstance(result, list)
        for tag in result:
            assert isinstance(tag, str)

        lengths = [len(tag) for tag in result]
        assert lengths == sorted(lengths, reverse=True)
        assert len(result) == 3

    def test_most_popular_type_and_sorting(self, tags_instance):
        result = tags_instance.most_popular(n=3)
        assert isinstance(result, dict)
        for tag, count in result.items():
            assert isinstance(tag, str)
            assert isinstance(count, int)
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_tags_with_type_and_sorting(self, tags_instance):
        result = tags_instance.tags_with("movie")
        assert isinstance(result, list)
        for tag in result:
            assert isinstance(tag, str)
            assert "movie" in tag.lower()

    def test_tags_by_movie_type_and_value(self, tags_instance):
        result = tags_instance.tags_by_movie(movie_id=60756)
        assert isinstance(result, list)
        for tag in result:
            assert isinstance(tag, str)
        assert len(result) == len(set(result))
        assert "funny" in result

    def test_most_common_words_type_and_sorting(self, tags_instance):
        result = tags_instance.most_common_words(n=3)
        assert isinstance(result, dict)
        for word, count in result.items():
            assert isinstance(word, str)
            assert isinstance(count, int)
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_movie_with_tag_type_and_sorting(self, tags_instance):
        result = tags_instance.movie_with_tag(tag="drugs")
        assert isinstance(result, list)
        for movie_id in result:
            assert isinstance(movie_id, int)
        assert result == sorted(result)
        expected_movie_id = 106782
        assert expected_movie_id in result

    # Bonus tests

    # movies method
    def test_dist_by_genres_sample_data(self, movie_instance_with_sample_data):
        expected = {
            "Adventure": 3,
            "Horror": 2,
            "Comedy": 1,
        }
        result = movie_instance_with_sample_data.dist_by_genres()
        assert result == expected

    def test_most_common_words_in_titles_sample_data(
        self, movie_instance_with_sample_data
    ):
        expected = {
            "movie": 3,
            "first": 1,
            "second": 1,
            "third": 1,
        }
        result = movie_instance_with_sample_data.most_common_words_in_titles()
        assert result == expected

    # ratings method
    def test_dist_by_genre_sample_data(self, ratings_instance_with_sample_data):
        expected = {
            "Adventure": 2.5,
            "Horror": 2.5,
            "Comedy": 2.5,
        }
        result = ratings_instance_with_sample_data.dist_by_genre()
        assert result == expected

    # tags method
    def test_most_common_words_sample_data(self, tags_instance_with_sample_data):
        expected = {
            "funny": 2,
            "cool": 1,
        }
        result = tags_instance_with_sample_data.most_common_words(n=3)
        assert result == expected

    # links method
    def test_movies_by_country(self, links_instance):
        expected = {
            "United States": 838,
            "United Kingdom": 164,
            "France": 110,
            "Canada": 41,
            "Italy": 38,
        }
        result = links_instance.movies_by_country(n=5)
        assert result == expected
