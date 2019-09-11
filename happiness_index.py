import os


def main():
    file_name = str(input("Enter the name of the file containing World Happiness computation data: "))

    # checking the file input is valid
    rows = read_file(file_name)
    if rows is None:
        raise Exception('Please enter a valid file name. The name entered was {}'.format(file_name))

    norm_rows = normalise_list(rows)
    print(norm_rows)
    metric = str(input("Choose metric to be tested from: min, mean, median, harmonic_mean. ")).lower()

    score = metric_calc(metric, norm_rows)
    print(score)

    output_action = str(input(
        "Choose action to be performed on the data using the specified metric."
        " The options are: list, correlation. "))


def read_file(file_name):
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


# Compute the min of each column across every row, and
# returns a list of [[countryName, min], [countryName, min] ...] for each column
def min_metric(rows):
    mins = []

    for row in rows:
        country_name = row[0]
        row_min = min(value for value in row[2:] if value is not None)
        mins.append([country_name, row_min])

    return mins


def mean_metric(rows):
    means = []

    for row in rows:
        country_name = row[0]
        total = 0
        for value in row[2:]:
            if value is None:
                continue
            total += value

        mean = total / (len(row) - 2)
        means.append([country_name, mean])

    return means


def median_metric(rows):
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
    return "hai"


metric_methods = {
    'min': min_metric,
    'mean': mean_metric,
    'median': median_metric,
    'harmonic_mean': harmon_metric,
}


# pass in the metric string and return for each of the functions
def metric_calc(metric_t, rows):
    func = metric_methods.get(metric_t)
    if func is None:
        raise Exception('Input a correct metric. You gave: {}'.format(metric_t))
    return func(rows)


main()
