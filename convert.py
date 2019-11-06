from jinja2 import Environment, FileSystemLoader
import csv
import sys
import ast
import os
import json

# arg 1 is path it input mapping csv
mapping_path = sys.argv[1]

# arg 2 path to about data
about_path = sys.argv[2]

# arg 2 is path to csv file to transform
source_csv_path = sys.argv[3]

# arg 3 is output path
output_path = sys.argv[4]

# load the dataset about info
with open(about_path) as about_file:
    about_data = json.load(about_file)

# parse input mapping
columns = []
removed = set()
with open(mapping_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row_idx, row in enumerate(reader):
        if len(row) > 1:
            entry = {
                'name': row[0],
                'type': row[1],
                'map': ast.literal_eval(row[2]),
                'description': row[3]
            }
            columns.append(entry)
        else:
            removed.add(row_idx)

# render using template
env = Environment(loader=FileSystemLoader('./templates'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('template.j2')
json_output = template.render(columns=columns, about=about_data)

# open the input data
remapped_data = []
with open(source_csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    # skip header
    next(reader, None)

    # append the new header names
    remapped_data.append(['d3mIndex'] + [column['name'] for column in columns])

    # for each element in a given row, add a d3m index and check to see if it needs to have its value remapped
    for row_num, row in enumerate(reader):
        remapped_row = [row_num]
        col_idx = 0
        for col_value in row:
            if col_idx in removed:
                continue

            col_map = columns[col_idx]['map']
            col_idx += 1

            value = col_value
            if len(col_map) > 0 and col_value in col_map:
                value = col_map[col_value]
            remapped_row.append(value)
        remapped_data.append(remapped_row)

# create the output dir
tables_path = os.path.join(output_path, 'tables')
if not os.path.exists(tables_path):
    os.makedirs(tables_path)

# write out the dataset doc
dataset_doc_path = os.path.join(output_path, 'datasetDoc.json')
with open(dataset_doc_path, 'w', newline='') as dataset_doc_file:
    dataset_doc_file.write(json_output)

# write out the remapped csv file
learning_data_path = os.path.join(tables_path, 'learningData.csv')
with open(learning_data_path, 'w', newline='') as learning_data_file:
    learning_data_writer = csv.writer(learning_data_file, quoting=csv.QUOTE_MINIMAL)
    learning_data_writer.writerows(remapped_data)

