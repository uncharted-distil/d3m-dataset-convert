from jinja2 import Environment, FileSystemLoader
import csv
import sys
import ast
import os

# arg 1 is path input mapping csv file
input_mapping_path = sys.argv[1]

# arg 2 is path to csv file to transform
source_csv_path = sys.argv[2]

# arg 3 is output path
output_path = sys.argv[3]

# TODO: grab dataset info
dataset = {
    'id': '',
    'name': '',
    'description': '',
    'license': '',
    'source': '',
    'uri': '',
    'size': '',
    'digest': ''
}

# parse input mapping
columns = []
with open(input_mapping_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        entry = {
            'name': row[0],
            'type': row[1],
            'map': ast.literal_eval(row[2]),
            'description': row[3]
        }
        columns.append(entry)

# render using template
env = Environment(loader=FileSystemLoader('./templates'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('template.j2')
json_output = template.render(columns=columns, dataset=dataset)

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
        for col_idx, col_value in enumerate(row):
            col_map = columns[col_idx]['map']
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
dataset_doc_path = os.path.join(output_path, 'datsetDoc.json')
with open(dataset_doc_path, 'w', newline='') as dataset_doc_file:
    dataset_doc_file.write(json_output)

# write out the remapped csv file
learning_data_path = os.path.join(tables_path, 'learningData.csv')
with open(learning_data_path, 'w', newline='') as learning_data_file:
    learning_data_writer = csv.writer(learning_data_file, quoting=csv.QUOTE_MINIMAL)
    learning_data_writer.writerows(remapped_data)

