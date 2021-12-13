"""
Graphs our data using plotly.graph_objects and writes to a png image
using kaleido.
"""
import datetime
import csv
import plotly.graph_objects as go
import filtration as f

# Dependencies:
# - kaleido
# - plotly
# - csv
# - datetime

# Global constants. These never change, and we really don't want to call
# store_cbc_to_dataclass more than once since it is very, very slow.
PUBLISH_DATES = [
    datetime.datetime(2020, 7, 14),
    datetime.datetime(2020, 11, 13),
    datetime.datetime(2021, 3, 5),
    datetime.datetime(2021, 5, 28),
    datetime.datetime(2021, 8, 27)
]

CBC = f.store_cbc_to_dataclass('dataset/articles.json')
GLOBAL = f.store_global_to_dataclass('dataset/global.json')
STAR = f.store_star_to_dataclass('dataset/the_star.json')


def get_avg_polarity_for_day(day: datetime.datetime, data: f.FilteredDataset) -> tuple[int, int]:
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


def read_data(file: str) -> list[list[float]]:
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
    # if file in {'dataset/july_2020.csv', 'dataset/nov_2020.csv'}:
    # if file in {'dataset/dataset_2020_07_14.csv', 'dataset/dataset_2020_11_13.csv'}:
    #     position = 11
    # else:
    #     position = 12
    position = 11

    with open(file) as csv_file:
        data = csv.reader(csv_file)
        # skip the header.
        next(data, None)
        for num, row in enumerate(data):
            list_num = num % 5
            # Since the files all end in 3 blank lines, and I don't know how to
            # get rid of them otherwise.
            if row and row[position]:
                filtered_data[list_num].append(float(row[position]))

    return filtered_data


def get_percentage_for_quarter(quarter: int) -> float:
    """
    Returns the percentage of positive articles published during the given quarter.

    Preconditions:
    - quarter in range(1, 5)
    """
    total_pos = 0
    total_articles = 0

    if quarter == 0:
        start_date = datetime.datetime(2020, 1, 1)
    else:
        start_date = PUBLISH_DATES[quarter - 1]

    end_date = PUBLISH_DATES[quarter]
    # for i in range((start_date - PUBLISH_DATES[quarter - 1]).days):
    for i in range((end_date - start_date).days):
        # print('i = ' + str(i))
        global_articles = get_avg_polarity_for_day(start_date + datetime.timedelta(i), GLOBAL)
        star_articles = get_avg_polarity_for_day(start_date + datetime.timedelta(i), STAR)
        cbc_articles = get_avg_polarity_for_day(start_date + datetime.timedelta(i), CBC)

        day_positive = global_articles[0] + star_articles[0] + cbc_articles[0]
        day_articles = global_articles[1] + star_articles[1] + cbc_articles[1]
        total_pos += day_positive
        total_articles += day_articles


    return total_pos / total_articles * 100


def generate_graph(months_until: int) -> None:
    """
    Generates a double bar graph with percentage of positive articles
    and percentage of businesses that will go bankrupt in a given time.
    The graph will be saved "graph{months_until}.png". For example, if
    months_until is 3, then the graph will be saved as "graph3.png".

    You can adjust the time until bankruptcy with the months_until parameter.
    Here are the accepted values and their effects:

    months_until = 1: businesses that will go bankrupt in less than 1 month
    months_until = 3: Businesses that will go bankrupt in 1 - 3 months
    months_until = 6: Businesses that will go bankrupt in 3 - 6 months
    months_until = 12: Businesses that will go bankrupt in 6 - 12 months
    months_until = 999: Businesses that will go bankrupt in more than 12 months

    Preconditions:
    - months_until in {1, 3, 6, 12, 999}
    """
    values = [1, 3, 6, 12, 999]
    indices = [0, 1, 2, 3, 4]
    num_months = ['less than 1', '1 - 3', '3 - 6', '6 - 12', 'more than 12']
    index = values.index(months_until)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            # x=PUBLISH_DATES[1:],
            x=[d.date() for d in PUBLISH_DATES],
            # y=[get_percentage_for_quarter(i) for i in range(1, 5)],
            y=[get_percentage_for_quarter(i) for i in range(5)],
            name='%age of positive articles'
        ))

    bankruptcy_data = [
        # read_data('dataset/july_2020.csv'),
        # read_data('dataset/nov_2020.csv'),
        # read_data('dataset/first_quarter.csv'),
        # read_data('dataset/second_quarter.csv'),
        # read_data('dataset/third_quarter.csv')
        read_data('dataset/dataset_2020_07_14.csv'),
        read_data('dataset/dataset_2020_11_13.csv'),
        read_data('dataset/dataset_2021_03_05.csv'),
        read_data('dataset/dataset_2021_05_28.csv'),
        read_data('dataset/dataset_2021_08_27.csv')
    ]
    fig.add_trace(
        go.Bar(
            # x=PUBLISH_DATES[1:],
            x=[d.date() for d in PUBLISH_DATES],
            # Change this last index to change the company size. Right now it's set at
            # 20 - 99 employees.
            # y=[bankruptcy_data[i][indices[index]][2] for i in range(1, 5)],
            y=[bankruptcy_data[i][indices[index]][2] for i in range(5)],
            name=f'%age of businesses bankrupt in {num_months[index]} month(s)'
        )
    )

    fig.update_layout(
        title='Positive Media Representation vs Time until Bankruptcy',
        xaxis=dict(type = 'category'),
        yaxis={
            'title': 'Percentage'
        }
    )

    fig.write_image(f'graph{months_until}.png', format='png')


if __name__ == '__main__':
    # import python_ta
    # import python_ta.contracts
    # python_ta.contracts.DEBUG_CONTRACTS = False
    # python_ta.contracts.check_all_contracts()
    # python_ta.check_all(config={
    #     'extra-imports': [
    #         'python_ta.contracts',
    #         'kaleido', 'csv',
    #         'plotly.graph_objects',
    #         'datetime',
    #         'python_ta',
    #         'filtration'
    #     ],
    #     'allowed-io': ['plotly.graph_objects.Figure.write_image', 'with', 'open'],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })
    generate_graph(1)
    generate_graph(3)
    generate_graph(6)
    generate_graph(12)
    generate_graph(999)
