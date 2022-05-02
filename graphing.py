"""
Graphs our data using plotly.graph_objects and writes to a png image
using kaleido.
"""
import datetime
# import csv
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import filtration as f
import bankruptcy as b

# Dependencies:
# - kaleido
# - plotly
# - csv
# - datetime

# Global Constants
PUBLISH_DATES = [
    datetime.datetime(2020, 7, 14),
    datetime.datetime(2020, 11, 13),
    datetime.datetime(2021, 3, 5),
    datetime.datetime(2021, 5, 28),
    datetime.datetime(2021, 8, 27)
]

f.load_business_data()
CBC = f.store_to_dataclass('cbc')
GLOBAL = f.store_to_dataclass('global')
STAR = f.store_to_dataclass('star')
# CBC = f.store_cbc_to_dataclass('dataset/cbc.json')
# GLOBAL = f.store_global_to_dataclass('dataset/global.json')
# STAR = f.store_star_to_dataclass('dataset/the_star.json')


def get_avg_polarity(start_date: datetime.datetime, 
                     end_date: datetime.datetime,
                     data: f.FilteredDataset) -> tuple[int, int]:
    """
    Returns number of positive articles and number of articles in data that were
    published within a given date range.
    """
    articles = []
    for i in range(len(data.publish_dates)):
        if start_date < data.publish_dates[i] <= end_date:
            articles.append(data.body_polarity_scores[i])

    pos_articles = 0
    for article in articles:
        if article['compound'] > 0.20:
            pos_articles += 1

    return pos_articles, len(articles)


def get_percentage_for_quarter(quarter: int) -> float:
    """
    Returns the percentage of positive articles published during the given quarter.

    Preconditions:
    - quarter in range(0, 5)
    """

    if quarter == 0:
        start_date = datetime.datetime(2020, 1, 1)
    else:
        start_date = PUBLISH_DATES[quarter - 1]

    end_date = PUBLISH_DATES[quarter]

    global_articles = get_avg_polarity(start_date, end_date, GLOBAL)
    star_articles = get_avg_polarity(start_date, end_date, STAR)
    cbc_articles = get_avg_polarity(start_date, end_date, CBC)

    total_positive = global_articles[0] + star_articles[0] + cbc_articles[0]
    total_articles = global_articles[1] + star_articles[1] + cbc_articles[1]

    return total_positive / total_articles * 100


def generate_graph(time_ind: int, size_ind: int) -> str:
    """
    Generates a double bar graph with percentage of positive articles and percentage 
    of businesses that will go bankrupt in a given time for a given number of employees.
    The graph will be saved "graph{time_ind}_{size_ind}.png". For example, if time_ind 
    is 3 and size_ind is 2, then the graph will be saved as "graph3_2.png".
    Returns the name of the graph after saving the image

    You can adjust the time until bankruptcy with the time_ind parameter.
    The value of time_ind corresponds to the index for LENGTH_OF_TIME_STR in bankruptcy.py
    Here are the accepted values and their effects:

    time_ind = 0: Businesses that will go bankrupt in less than 1 month
    time_ind = 1: Businesses that will go bankrupt in 1 - 3 months
    time_ind = 2: Businesses that will go bankrupt in 3 - 6 months
    time_ind = 3: Businesses that will go bankrupt in 6 - 12 months
    time_ind = 4: Businesses that will go bankrupt in more than 12 months
    time_ind = 5: Businesses that will go bankrupt in unknown time

    You can adjust the business size with the size_ind parameter.
    The value of size_ind corresponds to the index for EMPLOYEE_SIZE in bankruptcy.py

    size_ind = 0: Businesses with 1 to 4 employees,
    size_ind = 1: Businesses with 5 to 19 employees
    size_ind = 2: Businesses with 20 to 99 employees
    size_ind = 3: Businesses with 100 or more employees

    Preconditions:
    - time_ind in range(0, 6)
    - size_ind in range(0, 4)
    """

    filtered_data = b.load_data()

    # fig = go.Figure()
    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(
        go.Bar(
            x=[d.date() for d in PUBLISH_DATES],
            y=[get_percentage_for_quarter(i) for i in range(5)],
            name='%age of positive articles',
            showlegend=True,
        ),
        row=1, col=1
    )

    sample_time = b.LENGTH_OF_TIME_STR[time_ind]
    sample_size = b.EMPLOYEE_SIZE[size_ind]
    fig.add_trace(
        go.Bar(
            x=[d.date() for d in PUBLISH_DATES],
            y=[b.bankruptcy_value(data, time_length=sample_time, 
                                  employee_size=sample_size) for data in filtered_data],
            name=f'%age of businesses with {sample_size} <br> bankrupt in {sample_time}'
        ),
        row=1, col=1
    )

    fig.update_layout(
        title="Positive Media Representation vs Time until Bankruptcy",
        xaxis=dict(type='category'),
        yaxis={
            'title': 'Percentage'
        },
    )

    img_name = f'graphs/graph{time_ind}_{size_ind}.png'
    fig.write_image(img_name, format='png')
    return img_name


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
    python_ta.check_all(config={
        'extra-imports': [
            'python_ta.contracts',
            'kaleido', 'csv',
            'plotly.graph_objects',
            'datetime',
            'python_ta',
            'filtration'
        ],
        'allowed-io': ['plotly.graph_objects.Figure.write_image', 'with', 'open'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
