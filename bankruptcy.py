from dataclasses import dataclass
import datetime
import csv
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@dataclass
class CSV_Item:
    geo: str                # geo
    business_char: str      # business characteristics
    Length_of_time: str     # Length of time business can continue to operate
    value: float            # percentage

# LENGTH_OF_TIME_STR = [
#     "less than 1 month",
#     "less than 3 months",
#     "less than 6 months",
#     "less than 12 months",
#     "12 months or more",
#     "unknown"
# ]
LENGTH_OF_TIME_STR = [
    "less than 1 month",
    "1 month to less than 3 months",
    "3 months to less than 6 months",
    "6 months to less than 12 months",
    "12 months or more"
]

EMPLOYEE_SIZE = [
    "1 to 4 employees",
    "5 to 19 employees",
    "20 to 99 employees",
    "100 or more employees",
]


def load_data():
    csv_data = [
        read_csv_data('dataset/dataset_2020_07_14.csv'),
        read_csv_data('dataset/dataset_2020_11_13.csv'),
        read_csv_data('dataset/dataset_2021_03_05.csv'),
        read_csv_data('dataset/dataset_2021_05_28.csv'),
        read_csv_data('dataset/dataset_2021_08_27.csv')
    ]

    return csv_data


def read_csv_data(file: str) -> list[CSV_Item]:
    """
    Reads the csv file and returns a list of CSV_Item. Each CSV_Item representing a row (filtered)

    Preconditions:
    - file is one of the csv datasets
    """
    csv_data = []

    with open(file) as csv_file:
        data = csv.DictReader(csv_file)
        # print(data.fieldnames)
       
        # the length of time field has different name in different csv files, one of them 
        # is "Length of time", the other is very long but also starts with "Length of time",
        # so search for substring "Length of time" to find the field in both cases     
        # field_length_of_time = [field for field in data.fieldnames if "Length of time" in field][0]
        found_fields = [field for field in data.fieldnames if "Length of time" in field]
        field_length_of_time = found_fields[-1]

        for row in data:
            if row and row["VALUE"]:

                geo = row["GEO"]
                bc = row["Business characteristics"]
                t = row[field_length_of_time]
                val = row["VALUE"]

                if len(found_fields) > 1:
                    is_bankruptcy = "bankruptcy" in row[found_fields[0]]
                else:
                    is_bankruptcy = True

                if is_bankruptcy and geo == "Canada" and bc.endswith("employees"):
                    item = CSV_Item(geo, bc, t, val)
                    csv_data.append(item)

    return csv_data
    

# def filter_csv_data_by_employee(data: list[CSV_Item]) -> list[CSV_Item]:
#     """
#     Returns a list of csv items with its "geo" field being "Canada" and "business characteristics" 
#     field ends with keywords "employees"

#     Preconditions:
#     - data != []
#     """
#     filtered_data = [item for item in data if (item.geo == "Canada" and 
#                                                 item.business_char.endswith("employees"))]

#     return filtered_data


def bankruptcy_value(data: list[CSV_Item], time_length: str, employee_size: str) -> float:
    """
    Returns the bankruptcy percentage value of the item with given time_length and employee_size

    Preconditions:
    - data != []
    - time_length in LENGTH_OF_TIME_STR
    - employee_size in EMPLOYEE_SIZE
    """

    items = [item for item in data if (employee_size in item.business_char and
                                       time_length in item.Length_of_time)]
 
    # some csv files may have more than 1 row per per employee size per bankcruptcy length
    # of time, we only use the first row's value
    if items:
        return items[0].value
    else:
        return 0.0


# if __name__ == "__main__":
#     load_data()
