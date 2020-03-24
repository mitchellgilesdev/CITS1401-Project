CITS1401 Project 1 Pseudocode
Mitchell Giles (22490361)
Program Pseudocode
input():
Required to be called 3 times from main() and passed as parameters to respective functions.
1. Input data files’ name [“file_name”]
2. Name of the metric to be computed. [“min”, “mean”, “median”, “harmonic_mean”]
3. Name of the action to be performed [“list” (DESC on metric), “correlation” (Via
Spearman’s correlation coefficient on metric vs Life Ladder score)]
file_name = user input file name
metric = user input file metric (choose from “min”, ”mean”,”median”,”harmonic_mean”)
report_action = user input output type (either “list” or “correlation”)
Read in 3 these above strings as (file_name, metric, report_action) from the users input.
1. Read in the CSV file based on “file_name” user input, use floats to store all except
first field (use ‘None’). Store as row in List of Lists data structure.
2. Compute min/max for each column except the first (ignore ‘None’)
3. Normalise column values relative to min/max scores with formula (score-min)/(maxmin) for every column.
4. Except first two columns, computed the nominated metric, based on “metric” user
input, for each row. (Avoid ‘None’ & ‘0’ for “harmonic_mean”. Output as list of
(country, score) pairs.
5. Organise the list in either DESC order or using the Spearman’s rank correlation
coefficient of (country, score) and the Life Ladder list (in desc order also) producing a
value between -1.0 and 1.0, based on the “report_action” user input.
Function readfile()
f = open file (file_name) if it exists otherwise return error
list_list = []
for line in f
 line_list = split line into “words”
 list_list[line_number] = line_list
 set type string for first two columns and then float for rest columns in each line
close the file
Function normalise list
For each row in the list of rows
 Calculate the min and max value with (value-min)/(max-min)
 Replace each value in the list with its normalised value
Function metric
Calculate the nominated metric using inbuilt functions and design algorithm to implement the
Spearman’s Rank coefficient. Store in a list that can use used to output the data as required.
Function output format:
Taking the list as an input that was returned in metric, format the list in descending order,
regardless of whether it is “correlation” or “list”.
Output:
Print the list as formatted from output format.
