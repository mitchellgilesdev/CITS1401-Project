import os


def main():
    file_name = str(input("Enter the name of the file containing World Happiness computation data: "))

    metric = str(input("Choose metric to be tested from: min, mean, median, harmonic_mean. "))
    output_action = str(input(
        "Choose action to be performed on the data using the specified metric. The options are: list, correlation. "))

    rows = read_file(file_name)
    if rows
    print(rows)
    norm_rows = normalize_list(rows)
    print(checker(norm_rows))


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


# NOT WORKING CORRECTLY
def normalize_list(row_list):
    for row in row_list:
        row_min = min(value for value in row[2:] if value is not None)
        row_max = max(value for value in row[2:] if value is not None)

        for i, value in list(enumerate(row))[2:]:
            if value is None:
                continue
            row[i] = (value - row_min) / (row_max - row_min)

    return row_list


def checker(norm_rows):
    for row in norm_rows:
        for value in row[2:]:
            if (value is not None) and ((value < 0) or (value > 1)):
                print(row)
                return False
    return True


main()
