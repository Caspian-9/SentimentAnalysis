import plotly.graph_objects as go
import datetime
import csv
import filtration as f

# Dependencies:
# - kaleido
# - plotly
# - csv
# - datetime

cbc = f.store_cbc_to_dataclass('datasets/articles.json')
global_ = f.store_global_to_dataclass('datasets/global.json')
star = f.store_star_to_dataclass('datasets/the_star.json')


# TODO: Add type annotation [int, int]
def get_avg_polarity_for_day(day: datetime.datetime, data: f.FilteredDataset) -> tuple:
    """
    Returns number of positive articles and number of articles in data that were
    published on a given day.
    """
    articles = []
    for i in range(len(data.publish_dates)):
        if data.publish_dates[i] == day:
            articles.append(data.body_polarity_scores[i])

    pos_articles = 0
    for article in articles:
        if article['compound'] > 0.20:
            pos_articles += 1

    return pos_articles, len(articles)


# TODO: add type annotation list[list[float]]
def read_data(file: str) -> list:
    """
    Reads the csv file and returns a list of lists. Each list contained represents
    the time until the company goes bankrupt, and each inner list is sorted by
    company size. For example, the third element of the second list is the
    percentage of businesses with 20 - 99 employees that will go bankrupt
    in 1 - 3 months.

    Preconditions:
    - file is one of the csv datasets
    """
    # Accumulator: list of lists, each inner list contains the percentage of
    # companies that will go bankrupt in 1, 3, 6, 12, more than 12 months respectively,
    # sorted in order of number of employees
    filtered_data = [[], [], [], [], []]

    # Since the datasets have different formats -_-
    if file in {'datasets/july_2020.csv', 'datasets/nov_2020.csv'}:
        position = 11
    else:
        position = 12

    with open(file) as csv_file:
        data = csv.reader(csv_file)
        # skip the header.
        next(data, None)
        for num, row in enumerate(data):
            list_num = num % 5
            # Since the files all end in 3 blank lines, and I don't know how to
            # get rid of them otherwise.
            if row:
                filtered_data[list_num].append(float(row[position]))

    return filtered_data


publish_dates = [
    datetime.datetime(2020, 7, 14),
    datetime.datetime(2020, 11, 13),
    datetime.datetime(2021, 3, 5),
    datetime.datetime(2021, 5, 28),
    datetime.datetime(2021, 8, 27)
]


def get_percentage_for_quarter(quarter: int) -> float:
    """
    Returns the percentage of positive articles published during the given quarter.

    Preconditions:
    - quarter in range(1, 5)
    """
    total_pos = 0
    total_articles = 0
    start_date = publish_dates[quarter]
    for i in range((start_date - publish_dates[quarter - 1]).days):
        global_articles = get_avg_polarity_for_day(start_date + datetime.timedelta(i), global_)
        star_articles = get_avg_polarity_for_day(start_date + datetime.timedelta(i), star)
        cbc_articles = get_avg_polarity_for_day(start_date + datetime.timedelta(i), cbc)

        day_positive = global_articles[0] + star_articles[0] + cbc_articles[0]
        day_articles = global_articles[1] + star_articles[1] + cbc_articles[1]
        total_pos += day_positive
        total_articles += day_articles

    return total_pos / total_articles * 100


fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=publish_dates[1:],
        y=[get_percentage_for_quarter(i) for i in range(1, 5)],
        name='%age of positive articles'
    ))

bankruptcy_data = [
    read_data('datasets/july_2020.csv'),
    read_data('datasets/nov_2020.csv'),
    read_data('datasets/first_quarter.csv'),
    read_data('datasets/second_quarter.csv'),
    read_data('datasets/third_quarter.csv')
]
fig.add_trace(
    go.Bar(
        x=publish_dates[1:],
        y=[bankruptcy_data[i][1][2] for i in range(1, 5)],
        name='%age of businesses bankrupt in 1-3 months'
    )
)

fig.update_layout(
    title='Positive Media Representation vs Time until Bankruptcy',
    yaxis = {
        'title': 'Percentage'
    }
)

fig.write_image('graph.png', format='png')

