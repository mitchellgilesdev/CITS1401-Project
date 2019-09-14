"""
File: happiness_index.py
Title: Project 1: Computing World Happiness Index
Author: Mitchell Giles
Student_Number: 22490361
"""

import os


def main():
    # capturing the user file_name input
    file_name = str(input("Enter the name of the file containing World Happiness computation data: "))

    # normalising the file if no error occurs
    rows = read_file(file_name)
    try:
        norm_rows = normalise_list(rows)
    except TypeError:
        print("Please input a valid file. You gave: ", file_name)
        return None
    except IndexError:
        print("The file you gave was incorrectly formatted or didn't contain enough data. You gave:", file_name)
        return None

    # calculating the specified metric with valid input
    metric = str(input("Choose metric to be tested from: min, mean, median, harmonic_mean. ")).lower()
    try:
        country_score = metric_calc(metric, norm_rows)
    except TypeError:
        print("The metric type you gave was invalid. You gave: ", metric)
        return None

    # producing the output
    output_type = str(input(
        "Choose action to be performed on the data using the specified metric."
        " The options are: list, correlation. ")).lower()
    try:
        output_format(output_type, country_score, norm_rows, metric)
    except ValueError:
        print("The action you gave was invalid. You gave:", output_type)
        return None


def read_file(file_name):
    """
    Reads in the file line by line

    :param file_name: the name of the file in the current directory
    :return: a list of each of the lines in the file
    """

    if not os.path.isfile(file_name):
        return None

    row_list = []

    in_file = open(file_name, "r")
    lines = in_file.readlines()
    for row in lines[1:]:
        row_contents = row.split(",")
        for i in range(len(row_contents)):
            if i == 0:
                row_contents[i] = str(row_contents[i])
                continue
            if (row_contents[i] == "\n") or (row_contents[i] == ""):
                row_contents[i] = None
                continue
            row_contents[i] = float(row_contents[i])
        row_list.append(row_contents)
    in_file.close()
    return row_list


def normalise_list(row_list):
    """
    Normalises all the values in a row based on the row min and max

    :param row_list: a list of each or the rows to be normalised
    :return: a list of the normalised rows
    """
    column_num = 2
    row_size = len(row_list[1])
    while column_num < row_size:
        column_max = max(x for x in [row[column_num] for row in row_list] if x is not None)
        column_min = min(x for x in [row[column_num] for row in row_list] if x is not None)

        for row in row_list:
            value = row[column_num]
            if value is None:
                continue
            row[column_num] = (value - column_min) / (column_max - column_min)

        column_num += 1

    return row_list


def min_metric(rows):
    """
    Compute the min of of all columns for each row. Excluding None.

    :param rows: a list of rows
    :return: a list of [country_name, min] pairs for each country
    """
    mins = []

    for row in rows:
        country_name = row[0]
        row_min = min(value for value in row[2:] if value is not None)
        mins.append([country_name, row_min])

    return mins


def mean_metric(rows):
    """
    Compute the mean of all the columns for each row. Excluding None.

    :param rows: a list of rows
    :return: a list of [country_name, mean] pairs for each country
    """
    means = []

    for row in rows:
        country_name = row[0]
        total = 0
        skipped = 0
        for value in row[2:]:
            if value is None:
                skipped += 1
                continue
            total += value

        mean = total / (len(row) - 2 - skipped)
        means.append([country_name, mean])

    return means


def median_metric(rows):
    """
    Compute the median for all the columns in a row. Excluding None values.

    :param rows: a list of rows
    :return: a list of [country_name, median] pairs for each row
    """
    medians = []

    for row in rows:
        country_name = row[0]
        row_aesc = sorted(x for x in row[2:] if x is not None)

        if len(row_aesc) % 2 == 1:
            median = row_aesc[int((len(row_aesc) - 1) / 2)]
            medians.append([country_name, median])
        elif len(row_aesc) % 2 == 0:
            middle_right_index = int(len(row_aesc) / 2)
            median = (row_aesc[middle_right_index] + row_aesc[middle_right_index - 1]) / 2
            medians.append([country_name, median])

    return medians


def harmon_metric(rows):
    """
    Compute the harmonic mean for all the columns in a row. Excluding None and 0 values.

    :param rows: a list of rows
    :return: a list of [country_name, harmonic_mean] pairs for each row.
    """
    harmon_means = []

    for row in rows:
        country_name = row[0]
        row_size = 0
        inverse_sum = 0
        for value in row[2:]:
            if value is not None and (value != 0):
                row_size += 1
                inverse_sum += 1 / value
        harmonic_mean = row_size / inverse_sum
        harmon_means.append([country_name, harmonic_mean])

    return harmon_means


"""
Used to map each string to it's respective function name.
"""
metric_methods = {

    'min': min_metric,
    'mean': mean_metric,
    'median': median_metric,
    'harmonic_mean': harmon_metric,
}


def metric_calc(metric_t, rows):
    """
    Converting the string to a function call to the respective metric calculation.

    :param metric_t: the specified metric as a string
    :param rows: a list containing each row
    :return: a [country_name, metric] pair for each row
    """
    func = metric_methods.get(metric_t)
    return func(rows)


def output_format(action, list_pair, rows, calc_metric):
    """
    Sorts the list as required, formats the outputs and prints.

    :param action: the output type to be used
    :param list_pair: the [country_name, metric] list as calculated
    :param rows: the normalised list of rows
    :param calc_metric: the metric calculated from user input
    :return: 0 if printed correctly, ValueError if incorrect input
    """
    if action == "list":
        pairs = sorted(list_pair, key=lambda x: x[1], reverse=True)
        print('Ranked list of countries\' happiness scores based on the {} metric'.format(calc_metric))
        for pair in pairs:
            print('{} {:.4f}'.format(pair[0], pair[1]))
    elif action == "correlation":
        ranked_calc_score = sorted(list_pair, key=lambda x: x[1], reverse=True)
        ranked_life_score = sorted(rows, key=lambda x: x[1], reverse=True)

        # e.g. {"Australia": [calc_rank, life_rank]}
        ranks = {}

        for i, value in enumerate(ranked_calc_score):
            ranks.update({value[0]: [i + 1]})
        for i, value in enumerate(ranked_life_score):
            ranks[value[0]].append(i + 1)

        diff_sum = 0
        for _, values in ranks.items():
            diff_sqrd = (values[1] - values[0]) ** 2
            diff_sum += diff_sqrd

        n = len(ranks)
        spearman = 1 - ((6 * diff_sum) / (n * (n ** 2 - 1)))
        print(
            'The correlation coefficient between the study ranking and the ranking using the {} metric is {:.4f}'.format(
                calc_metric, spearman))

    else:
        # return an error code if the action input was invalid to catch
        raise ValueError
