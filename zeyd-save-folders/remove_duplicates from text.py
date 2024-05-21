import time 
start = time.time()

def remove_duplicates(input_file, output_file):
    unique_ids = set()
    
    # Read the file and collect unique IDs
    with open(input_file, 'r') as file:
        for line in file:
            id = line.strip()
            unique_ids.add(id)

    # Write the unique IDs to a new file
    with open(output_file, 'w') as file:
        for id in unique_ids:
            file.write(id + '\n')

if __name__ == "__main__":
    # File paths
    input_file = 'ids.txt'
    output_file = 'unique_ids.txt'

    # Remove duplicates
    remove_duplicates(input_file, output_file)

    end = time.time()
    print(f"Duplicates removed. Unique IDs are stored in {output_file}")