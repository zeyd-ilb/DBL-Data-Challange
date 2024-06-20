input_file = "chains_scores_v1.txt"
output_file = "filtered_data_3_1.txt"

# Read the data from the text file
with open(input_file, 'r') as file:
    data = file.read()

# Convert the string representation of the list into an actual list
data_list = eval(data)

# Filter out sublists that have more or less than one number
filtered_list = [sublist for sublist in data_list if len(sublist) > 4 ]
filtered_list = [sublist for sublist in filtered_list if len(sublist) < 6 ]

# Print the filtered list
print(filtered_list)

# Optionally, save the filtered list back to a file
with open(output_file, 'w') as file:
    file.write(str(filtered_list))
