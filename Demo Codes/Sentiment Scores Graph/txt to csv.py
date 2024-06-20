import csv
import re

def extract_numbers_from_brackets(line):
    # Extract the numbers inside the brackets
    matches = re.findall(r'\[(.*?)\]', line)
    extracted_data = []
    for match in matches:
        numbers = match.split(',')
        extracted_data.append(numbers)
    return extracted_data

def txt_to_csv(input_file, output_file):
    with open(input_file, 'r') as txt_file:
        lines = txt_file.readlines()
    
    all_data = []
    for line in lines:
        extracted_data = extract_numbers_from_brackets(line)
        all_data.extend(extracted_data)
    
    # Determine the maximum number of columns
    max_columns = max(len(row) for row in all_data)

    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        for row in all_data:
            # Extend row with empty strings if it has less columns than max_columns
            row.extend([''] * (max_columns - len(row)))
            csv_writer.writerow(row)

# Usage
input_file = 'filtered_data_3_1.txt'  # Replace with your input text file name
output_file = 'output_file_1.csv'  # Replace with your desired output CSV file name

txt_to_csv(input_file, output_file)
print(f"Conversion complete. {output_file} has been created.")
