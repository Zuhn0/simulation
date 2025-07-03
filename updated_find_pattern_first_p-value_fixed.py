import sys
from scipy.stats import binom_test

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

def reverse_complement(pattern):
    """
    Returns the reverse complement of a given pattern.
    Assuming the pattern consists of nucleotides (A, T, C, G).
    """
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return [complement.get(base, base) for base in reversed(pattern)]

def find_pattern(data, pattern):
    """
    Identifies all consecutive occurrences of a pattern (both forward and reverse) 
    in the fifth column of the file data.
    :param data: List of rows (each row is a list of columns from the file)
    :param pattern: List of values to match in the fifth column
    :return: List of tuples with the row numbers, direction, and the rows where the pattern occurs consecutively
    """
    pattern_length = len(pattern)
    reverse_pattern = reverse_complement(pattern)
    
    fifth_column = [row[4] for row in data]  # Extracting the 5th column (index 4)

    occurrences = []
    for i in range(len(fifth_column) - pattern_length + 1):
        forward_match = fifth_column[i:i + pattern_length] == pattern
        reverse_match = fifth_column[i:i + pattern_length] == reverse_pattern
        
        if forward_match:
            occurrences.append((i + 1, i + pattern_length, 'forward', data[i:i + pattern_length]))  # Forward match
        elif reverse_match:
            occurrences.append((i + 1, i + pattern_length, 'reverse', data[i:i + pattern_length]))  # Reverse match

    return occurrences

def compute_difference(row, prev_row):
    """
    Computes the difference between the second column of the current row
    and the third column of the previous row. Handles the case when prev_row is None.
    """
    if prev_row is None:
        return None  # No previous row exists
    try:
        current_val = float(row[1])  # Second column of current row
        previous_val = float(prev_row[2])  # Third column of previous row
        return current_val - previous_val
    except ValueError:
        return None  # If columns are not numeric, return None

def is_within_tolerance(actual, expected, tolerance):
    """
    Checks if the actual value is within the tolerance range of the expected value.
    Returns a tuple (bool, deviation), where 'bool' indicates if it's within tolerance,
    and 'deviation' is the amount the actual value deviates from the expected.
    """
    deviation = abs(actual - expected)
    return deviation <= tolerance, deviation

def calculate_p_value(num_matches, total_tries):
    """
    Calculates the p-value using a binomial test.
    """
    if total_tries > 0:
        return binom_test(num_matches, total_tries, 0.5, alternative='greater')
    return 1.0  # If no trials, return a neutral p-value

def main(file_name, pattern_str, lengths_str, differences_str, length_tolerance_str, difference_tolerance_str):
    # Reading the file
    data = read_file(file_name)
    
    # Parsing inputs
    pattern = pattern_str.split(',')
    target_lengths = list(map(float, lengths_str.split(',')))
    target_differences = list(map(float, differences_str.split(',')))
    length_tolerance = float(length_tolerance_str)
    difference_tolerance = float(difference_tolerance_str)

    # Finding the pattern
    occurrences = find_pattern(data, pattern)

    match_results = []
    
    if occurrences:
        for start, end, direction, matched_rows in occurrences:
            exact_length_matches = 0
            exact_diff_matches = 0
            within_tolerance_length_matches = 0
            within_tolerance_diff_matches = 0

            prev_row = None
            # Capture interval values
            interval_values = []
            for i, row in enumerate(matched_rows):
                interval_values.append('_'.join(row))  # Join all row values with '_'
                diff = compute_difference(row, prev_row)
                
                # Check for length and difference matches if not the first row
                if i > 0:
                    if float(row[3]) == target_lengths[i - 1]:
                        exact_length_matches += 1
                    else:
                        within_tolerance, _ = is_within_tolerance(float(row[3]), target_lengths[i - 1], length_tolerance)
                        if within_tolerance:
                            within_tolerance_length_matches += 1
                    
                    if diff is not None and diff == target_differences[i - 1]:
                        exact_diff_matches += 1
                    else:
                        if diff is not None:
                            within_tolerance, _ = is_within_tolerance(diff, target_differences[i - 1], difference_tolerance)
                            if within_tolerance:
                                within_tolerance_diff_matches += 1
                
                prev_row = row  # Update prev_row for the next iteration

            # Calculate p-value for the current match
            total_tries = len(matched_rows) - 1  # Number of comparisons
            p_value = calculate_p_value(exact_length_matches + exact_diff_matches, total_tries)
            
            # Append result for sorting
            match_results.append({
                'start': start,
                'end': end,
                'direction': direction,
                'exact_length_matches': exact_length_matches,
                'within_tolerance_length_matches': within_tolerance_length_matches,
                'exact_diff_matches': exact_diff_matches,
                'within_tolerance_diff_matches': within_tolerance_diff_matches,
                'p_value': p_value,
                'interval_values': '_'.join(interval_values)  # Join interval values
            })

        # Sort the results: first by p-value (ascending), then by total matches (descending)
        match_results.sort(key=lambda x: (x['p_value'], -(x['exact_length_matches'] + x['exact_diff_matches'])))

        # Report the sorted results in a single line
        print("Start\tEnd\tDirection\tExact_Length_Matches\tExact_Diff_Matches\tWithin_Tolerance_Length_Matches\tWithin_Tolerance_Diff_Matches\tP_value\tInterval_Values")
        for result in match_results:
            print(f"{result['start']}\t{result['end']}\t{result['direction']}\t"
                  f"{result['exact_length_matches']}\t{result['exact_diff_matches']}\t"
                  f"{result['within_tolerance_length_matches']}\t{result['within_tolerance_diff_matches']}\t"
                  f"{result['p_value']:.5f}\t{result['interval_values']}")

    else:
        print("Pattern not found in the file.")

if __name__ == "__main__":
    # Example: python script.py file.txt "pattern1,pattern2,pattern3" "length1,length2" "diff1,diff2" "length_tolerance" "diff_tolerance"
    if len(sys.argv) != 7:
        print("Usage: python script.py <file_name> <pattern> <lengths> <differences> <length_tolerance> <difference_tolerance>")
        sys.exit(1)
    
    file_name = sys.argv[1]
    pattern_str = sys.argv[2]
    lengths_str = sys.argv[3]
    differences_str = sys.argv[4]
    length_tolerance_str = sys.argv[5]
    difference_tolerance_str = sys.argv[6]
    
    main(file_name, pattern_str, lengths_str, differences_str, length_tolerance_str, difference_tolerance_str)
