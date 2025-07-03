import sys

def read_file(file_name):
    """
    Reads a five-column file and returns the contents as a list of lists.
    Each inner list represents a line from the file.
    """
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            data.append(line.strip().split())
    return data

def compute_differences(data):
    """
    Computes the difference between the second column of the current row
    and the third column of the previous row.
    :param data: List of rows (each row is a list of columns from the file)
    :return: List of differences (second column of the current row - third column of the previous row)
    """
    differences = []
    prev_row = None
    for row in data:
        if prev_row is not None:
            try:
                current_start = int(row[1])  # Second column (start) of the current row
                prev_end = int(prev_row[2])  # Third column (end) of the previous row
                differences.append(current_start - prev_end)
            except ValueError:
                differences.append("NA")  # Handle cases where columns are not numeric
        prev_row = row  # Update previous row
    return differences

def process_file(file_name):
    # Read the data from the file
    data = read_file(file_name)

    # Extract the 5th column (gene names) and 4th column (lengths)
    gene_names = [row[4] for row in data]
    lengths = [row[3] for row in data]

    # Compute differences between the second column of one row and the third column of the previous row
    differences = compute_differences(data)

    # Output the gene names as a comma-separated list
    gene_names_str = ",".join(gene_names)
    
    # Output the lengths as a comma-separated list
    lengths_str = ",".join(lengths)
    
    # Output the differences as a comma-separated list, starting from the second row (since the first has no previous row)
    differences_str = ",".join(map(str, differences))

    # Print the final output
    print(f"{gene_names_str} {lengths_str} {differences_str}")

if __name__ == "__main__":
    # Check if the file name argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_name>")
        sys.exit(1)
    
    # Get the file name from the command-line arguments
    file_name = sys.argv[1]
    
    # Process the file
    process_file(file_name)
