"""
Bankruptcy data
"""

from dataclasses import dataclass
import os
import csv
import datetime


@dataclass
class FilteredData:
    """
    Instance Attributes:
        - pub_date: dataset publication date
        - data: the filtered data from the dataset

    Representation Invariants:
        -
    """

    pub_date: datetime.date
    data: list[list]


def load_data(filename: str) -> FilteredData:
    """
    read and filter data from csv file
    """
    # need absolute path to open file for some reason ech
    filepath = os.path.join(os.path.abspath('data'), filename)

    rows_so_far = []

    with open(filepath) as f:
        reader = csv.reader(f, delimiter=',')
        first_row = next(reader)

        for row in reader:

            if row[first_row.index('VALUE')] != '':    # because some values are empty

                # the 3 values we need:
                # row[3] business characteristics (str)
                # row[4] time length (str)
                #   ^ THIS PART REQUIRES SLIGHTLY MODIFIED DATA BECAUSE I CURRENTLY COULD NOT BE
                #   BOTHERED TO WRITE A FUNCTION TO DEAL WITH THE DATA'S INCONSISTENT STRUCTURE
                # row[first_row.index('VALUE')]    # value/percentage (float)
                #   ^ at least the heading stays consistent here
                #   (we love inconsistent structures)

                rows_so_far.append([row[3], row[4], float(row[first_row.index('VALUE')])])

    publication_date = get_pub_date_from_filename(filename)

    filtered_data = FilteredData(publication_date, rows_so_far)
    return filtered_data


def get_pub_date_from_filename(filename: str) -> datetime.date:
    """
    extract publication date from name of csv file
    """

    split_name = str.split(filename[:-4], '_')    # ['dataset', '(year)', '(month)', '(day)']

    year = int(split_name[1])
    month = int(split_name[2])
    day = int(split_name[3])

    return datetime.date(year, month, day)


# TODO: make function that converts length of time in data into numbers
