# Input and output file paths
input_file = 'BA_AirlineReviews.csv'
output_file = 'cleaned_BA_AirlineReviews4.csv'

# Open input and output files
with open(input_file, 'r', encoding='utf-8') as f_input, \
     open(output_file, 'w', newline='', encoding='utf-8') as f_output:

    # Read the header and write it to the output CSV file
    header = f_input.readline().strip()
    f_output.write(header + '\n')

    # Iterate through each line in the input CSV file
    for line in f_input:
        # Check if the line is empty or starts with a double quote (")
        if not line.strip() or line.startswith('"'):
            continue  # Skip this line

        # Write the line to the output CSV file
        f_output.write(line)
