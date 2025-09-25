#!/usr/bin/env python3
from collections import Counter


class Tags:
    """
    Analyzing data from tags.csv
    """

    class Structure:
        def __init__(self, list):
            if len(list) == 4:
                self.user_id = int(list[0])
                self.movie_id = int(list[1])
                self.tag = list[2].strip()
                self.timestamp = list[3]
            else:
                raise Exception("Error length of the list must be 4")

    def __init__(self, path_to_the_file, number_of_lines):
        number_of_lines += 1
        self.number_of_lines = number_of_lines
        self.list_of_data = []
        with open(path_to_the_file, "r") as file:
            reader = file.readlines()
            for line in reader[1:number_of_lines]:

                data = Tags.Structure(line.split(","))
                self.list_of_data.append(data)

    def most_words(self, n):
        """
               The method returns top-n tags with most words inside. It is a dict
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        tags_count = {}
        for data in self.list_of_data:
            tag = data.tag
            if tag not in tags_count:
                tags_count[tag] = len(tag.split())
        return dict(Counter(tags_count).most_common(n))

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        unique_tags = list(set([data.tag for data in self.list_of_data if data.tag]))
        return sorted(unique_tags, key=lambda x: len(x), reverse=True)[:n]

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        top_w = set(self.most_words(self.number_of_lines))
        top_ch = set(self.longest(self.number_of_lines))
        return sorted((top_w & top_ch), key=lambda x: len(x), reverse=True)[:n]

    def most_popular(self, n):
        """
        The method returns the most popular tags.
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        return dict(
            Counter([data.tag for data in self.list_of_data if data.tag]).most_common(n)
        )

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        tags_with_word = [
            data.tag for data in self.list_of_data if word.lower() in data.tag.lower()
        ]
        return sorted(set(tags_with_word))

    def tags_by_movie(self, movie_id):
        """Returns all unique tags for the movie"""
        return list(
            set([data.tag for data in self.list_of_data if data.movie_id == movie_id])
        )

    def most_common_words(self, n):
        """Returns the most common words in all tags"""
        word_counter = Counter()
        for data in self.list_of_data:
            words = data.tag.lower().replace(",", "").split()
            word_counter.update(words)
        return dict(word_counter.most_common(n))

    def movie_with_tag(self, tag):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        movies_with_tags = [
            data.movie_id
            for data in self.list_of_data
            if tag.lower() in data.tag.lower()
        ]
        return sorted(set(movies_with_tags))
