"""CSC110 Fall 2021 Final Project: Dataset Filtration

    This module contains six different types of functions:
read_file, find_business, sort, polarity_analysis, datetime_converter, and store_to_dataclass.
find_business and sort are both split into two similar functions since there are some formatting
difference between 'dataset/articles.json' and the other two datasets. The datetime_converter
function is split into three functions, each specified for a dataset, because each datasets'
publish times have different formats.

    Users of this module can read a dataset file using read_file, filtrate the articles in the
dataset related to business using find_business_star_global or find_business_cbc, sort each
section(title, publish time, and body) of each article in the dataset using sort_start_or_global
or sort_cbc, analyze each article title and article body's polarity score using polarity_analysis,
and convert the publish times of articles in the dataset into datetime.datetime format. Lastly, the
store_to_dataclass functions help gather all the filtered sections of the dataset and store them
in a dataclass. 

    This module contains one dataclass: FilteredDataset. Results from sort_cbc,
sort_start_or_global, datetime_converter_star, datetime_converter_cbc, datetime_converter_global,
and polarity_analysis can be stored into different attributes of FilteredDataset.
"""

import datetime
from dataclasses import dataclass
import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

nltk.download("vader_lexicon")


def read_file(file_name: str) -> list[dict[str, str]]:
    """
    Read a dataset and return it.

    preconditions:
    - file_name in ['dataset/the_star.json', 'dataset/global.json',
    'dataset/articles.json']
    """
    with open(file_name) as file:
        storage = json.load(file)

    return storage


def find_business_star_global(file_name: str) -> list[dict[str, str]]:
    """filter the articles that are related to business and add them to business_articles

    preconditions:
    - file_name in ['dataset/the_star.json', 'dataset/global.json']
    """
    business_terms = ['business', 'company', 'money', 'bank', 'tax', 'income',
                      'sales', 'employees']
    business_articles = []
    for article in read_file(file_name):
        if any(x in article['title'].lower() or x in article['body'].lower()
               for x in business_terms):
            business_articles.append(article)

    return business_articles


def find_business_cbc(file_name: str) -> list[dict[str, str]]:
    """
    filter the articles that are related to business and add them to business_articles.
    This dataset used a different function than sort_star_or_global since
    the key corresponding to the article body for each article dictionary in
    'dataset/articles.json' is 'description' instead of 'body'.
    Using a single sort_dataset function for all three datasets will raise key error.

    preconditions:
    - file_name == 'dataset/articles.json'
    """
    business_terms = ['business', 'company', 'money', 'bank', 'tax', 'income',
                      'sales', 'employees', 'shop', 'market']
    business_articles = []
    for article in read_file(file_name):
        if any(x in article['title'].lower() or x in article['description'].lower()
               for x in business_terms):
            business_articles.append(article)

    return business_articles


def sort_star_or_global(file_name: str) -> tuple[list[str], list[str], list[str]]:
    """
    Sort the given dataset's(the_star.json or global.json) data into three sections:
    titles, publish dates, and bodies.

    preconditions:
    - file_name in ['dataset/the_star.json', 'dataset/global.json']
    """
    # ACCUMULATOR titles: keep track of the articles' titles in
    # the given dataset sorted so far
    titles = []

    # ACCUMULATOR publish_dates: keep track of the articles' publish dates in
    # the given dataset sorted so far
    publish_dates = []

    # ACCUMULATOR bodies: keep track of the articles' bodies in
    # the given dataset sorted so far
    bodies = []

    for article in find_business_star_global(file_name):
        titles.append(article['title'])
        publish_dates.append(article['publish_time'])
        bodies.append(article['body'])

    return titles, publish_dates, bodies


def sort_cbc(file_name: str) -> tuple[list[str], list[str], list[str]]:
    """
    Sort 'dataset/articles.json''s data into three sections:
    titles, publish dates, and bodies.

    preconditions:
    - file_name == 'dataset/articles.json'
    """
    # ACCUMULATOR titles: keep track of the articles' titles in
    # 'dataset/article.json' sorted so far
    titles = []

    # ACCUMULATOR publish_dates: keep track of the articles' publish dates in
    # 'dataset/article.json' sorted so far
    publish_dates = []

    # ACCUMULATOR bodies: keep track of the articles' bodies in
    # 'dataset/article.json' sorted so far
    bodies = []

    for article in find_business_cbc(file_name):
        titles.append(article['title'])
        publish_dates.append(article['publish_time'])
        bodies.append(article['description'])

    return titles, publish_dates, bodies


def polarity_analysis(sorted_data: tuple[list[str], list[str], list[str]]) -> \
        tuple[list[dict[str: float]], list[dict[str: float]]]:
    """return an average polarity score dictionary for every article title
    and article body in the sorted_data parameter

    preconditions:
    - sorted_data != ()
    - all(not(x == [] for x in sorted_data))
    """
    analysis = SentimentIntensityAnalyzer()

    title_score_tracker = []
    body_score_tracker = []

    for article_title in sorted_data[0]:
        score = analysis.polarity_scores(article_title)
        title_score_tracker.append(score)

    for article_body in sorted_data[2]:
        score = analysis.polarity_scores(article_body)
        body_score_tracker.append(score)

    return title_score_tracker, body_score_tracker


def datetime_converter_cbc(file_name: str) -> list[datetime.datetime]:
    """Convert the raw publish date data in the CBC dataset to datetime.datetime format.

    preconditions
    - file_name == 'dataset/articles.json'
    """
    # ACCUMULATOR date_times_cbc: keep track of the publish times in datetime.datetime
    # format for all CBC business articles
    date_times_cbc = []

    for article in find_business_cbc(file_name):
        raw_date = article['publish_time']
        year = int(raw_date[0:4])
        month = int(raw_date[5: 7])
        day = int(raw_date[8: 10])
        date_time = datetime.datetime(year, month, day)
        date_times_cbc.append(date_time)

    return date_times_cbc


def datetime_converter_star(file_name: str) -> list[datetime.datetime]:
    """Convert the raw publish date data in the the Star dataset to datetime.datetime
    format.

    preconditions
    - file_name == 'dataset/the_star.json'
    """
    month_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    # ACCUMULATOR date_times_star: keep track of the publish times in datetime.datetime
    # format for all the Star business articles
    date_times_star = []

    for article in find_business_star_global(file_name):
        raw_date = article['publish_time']
        year = int(raw_date[14: 19])
        month = month_num[str(raw_date[6: 9])]
        if raw_date[12].isnumeric():
            day = int(raw_date[11: 13])
        else:
            day = int(raw_date[11])
        date_time = datetime.datetime(year, month, day)
        date_times_star.append(date_time)

    return date_times_star


def datetime_converter_global(file_name: str) -> list[datetime.datetime]:
    """Convert the raw publish date data in the CBC dataset to datetime.datetime format.

    preconditions
    - file_name == 'dataset/articles.json'
    """
    month_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    # ACCUMULATOR date_times_global: keep track of the publish times in datetime.datetime
    # format for all Global business articles
    date_times_global = []

    for article in find_business_star_global(file_name):
        raw_date = article['publish_time']
        split_lst = str.split(raw_date, ' ')
        year = int(split_lst[3])
        raw_month = split_lst[1]
        short_month = raw_month[0: 3]
        month = month_num[str(short_month)]
        raw_day = split_lst[2]
        raw_day_lst = list(raw_day)
        raw_day_lst.remove(',')
        day = int(''.join(raw_day_lst))
        date_time = datetime.datetime(year, month, day)
        date_times_global.append(date_time)

    return date_times_global


@dataclass
class FilteredDataset:
    """the titles, publish dates, bodies, and polarity scores of articles in a certain dataset

    Representation Invariants:
    - len(self.Titles) == len(self.PublishDate) == len(self.Bodies) == len(self.PolarityScores)
    - all(len(x) == 4 for x in self.PolarityScores)

    Instance Attributes:
    - Titles: the list of article titles in the dataset
    - PublishDate: the list of each article's publish date
    - Bodies: the list of article bodies in the dataset,
    each Title-Body pair shares the same index in their separate attribute list
    - TitlePolarityScores: the list of dictionaries of polarity scores for
    article titles generated with the nltk
    SentimentIntensityAnalyzer.
    - TitlePolarityScores: the list of dictionaries of polarity scores for
    article bodies generated with the nltk
    SentimentIntensityAnalyzer.
    """
    titles: list[str]
    publish_dates: list[datetime.datetime]
    bodies: list[str]
    title_polarity_scores: list[dict[str: float]]
    body_polarity_scores: list[dict[str: float]]


def store_star_to_dataclass(file_name: str) -> FilteredDataset:
    """Store all filtered sections of the given dataset into a FilteredDataset class, such filtered
    sections include: titles, datetime.datetime publish dates, bodies, title polarity scores, and
    body polarity scores.

    preconditions:
    - file_name == 'dataset/the_star.json'
    """
    # the_star = FilteredDataset(sort_star_or_global(file_name)[0],
    #                            datetime_converter_star(file_name),
    #                            sort_star_or_global(file_name)[2],
    #                            polarity_analysis(sort_star_or_global(file_name))[0],
    #                            polarity_analysis(sort_star_or_global(file_name))[1]
    #                            )
    sorted_data = sort_star_or_global(file_name)
    polarity = polarity_analysis(sorted_data)

    the_star = FilteredDataset(sorted_data[0],
                               datetime_converter_star(file_name),
                               sorted_data[2],
                               polarity[0],
                               polarity[1]
                               )
    return the_star


def store_global_to_dataclass(file_name: str) -> FilteredDataset:
    """Store all filtered sections of the given dataset into a FilteredDataset class, such filtered
    sections include: titles, datetime.datetime publish dates, bodies, title polarity scores, and
    body polarity scores.

    preconditions:
    - file_name == 'dataset/the_star.json'
    """
    # global_ = FilteredDataset(sort_star_or_global(file_name)[0],
    #                           datetime_converter_global(file_name),
    #                           sort_star_or_global(file_name)[2],
    #                           polarity_analysis(sort_star_or_global(file_name))[0],
    #                           polarity_analysis(sort_star_or_global(file_name))[1]
    #                           )

    sorted_data = sort_star_or_global(file_name)
    polarity = polarity_analysis(sorted_data)

    global_ = FilteredDataset(sorted_data[0],
                              datetime_converter_global(file_name),
                              sorted_data[2],
                              polarity[0],
                              polarity[1]
                              )
    return global_


def store_cbc_to_dataclass(file_name: str) -> FilteredDataset:
    """Store all filtered sections of the given dataset into a FilteredDataset class, such filtered
    sections include: titles, datetime.datetime publish dates, bodies, title polarity scores, and
    body polarity scores.

    preconditions:
    - file_name == 'dataset/the_star.json'
    """
    # cbc = FilteredDataset(sort_cbc(file_name)[0],
    #                       datetime_converter_cbc(file_name),
    #                       sort_cbc(file_name)[2],
    #                       polarity_analysis(sort_cbc(file_name))[0],
    #                       polarity_analysis(sort_cbc(file_name))[1]
    #                       )

    sorted_data = sort_cbc(file_name)
    polarity = polarity_analysis(sorted_data)

    cbc = FilteredDataset(sorted_data[0],
                          datetime_converter_cbc(file_name),
                          sorted_data[2],
                          polarity[0],
                          polarity[1]
                          )
    return cbc


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # import python_ta
    # import python_ta.contracts
    # python_ta.contracts.DEBUG_CONTRACTS = False
    # python_ta.contracts.check_all_contracts()
    # python_ta.check_all(config={
    #     'extra-imports': ['nltk', 'json', 'dataclass', 'python_ta.contracts',
    #                       'python_ta', 'doctest', ],
    #     'allowed-io': ['read_file', 'sort_star_or_global', 'sort_cbc'],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })
