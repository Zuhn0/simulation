import sys
import math

def read_bed_file(filename):
    with open(filename, 'r') as f:
        return [line.strip().split() for line in f if line.strip()]

def compute_differences(data):
    differences = []
    for i in range(1, len(data)):
        diff = int(data[i][1]) - int(data[i-1][2])
        differences.append(diff)
    return differences

def extract_lengths(data):
    return [int(row[3]) for row in data]

def extract_genes(data):
    return [row[4] for row in data]

def match_pattern(query_genes, query_lengths, query_diffs, segment, tol_len, tol_diff):
    segment_genes = [row[4] for row in segment]
    segment_lengths = extract_lengths(segment)
    segment_diffs = compute_differences(segment)

    inserted = []
    deleted = []
    match_len = match_diff = match_exact = 0
    i = j = 0

    while i < len(query_genes) and j < len(segment_genes):
        if query_genes[i] == segment_genes[j]:
            diff_match = abs(query_diffs[i-1] - segment_diffs[j-1]) <= tol_diff if i > 0 and j > 0 else True
            len_match = abs(query_lengths[i] - segment_lengths[j]) <= tol_len
            if diff_match:
                match_diff += 1
            if len_match:
                match_len += 1
            if len_match and diff_match:
                match_exact += 1
            i += 1
            j += 1
        elif query_genes[i] not in segment_genes[j:j+2]:
            deleted.append((i, query_genes[i]))
            i += 1
        else:
            inserted.append((j, segment_genes[j]))
            j += 1

    while i < len(query_genes):
        deleted.append((i, query_genes[i]))
        i += 1
    while j < len(segment_genes):
        inserted.append((j, segment_genes[j]))
        j += 1

    p_value = math.exp(-1 * (match_exact + 0.5 * match_len + 0.25 * match_diff))
    return {
        "match_exact": match_exact,
        "match_len": match_len,
        "match_diff": match_diff,
        "p_value": p_value,
        "inserted": inserted,
        "deleted": deleted
    }

def find_patterns(bed_data, gene_list, len_list, diff_list, tol_len, tol_diff):
    matches = []
    n = len(gene_list)

    for i in range(len(bed_data) - n + 1):
        segment = bed_data[i:i+n]
        result = match_pattern(gene_list, len_list, diff_list, segment, tol_len, tol_diff)
        matches.append((i, i+n-1, 'forward', result))

    matches.sort(key=lambda x: x[3]['p_value'])
    return matches[:3]

def print_result(start, end, direction, result):
    print(f"{start}\t{end}\t{direction}\t"
          f"{result['match_exact']}\t"
          f"{result['match_len']}\t"
          f"{result['match_diff']}\t"
          f"{result['p_value']:.5f}\t"
          f"{','.join(g for _, g in result['inserted']) or '-'}\t"
          f"{','.join(g for _, g in result['deleted']) or '-'}")

def main():
    if len(sys.argv) != 7:
        print("Usage: python3 updated_find_pattern_first_p-value_fixed.py <bed_file> <gene_list> <len_list> <diff_list> <tol_len> <tol_diff>")
        sys.exit(1)

    bed_file = sys.argv[1]
    gene_list = sys.argv[2].split(",")
    len_list = list(map(int, sys.argv[3].split(",")))
    diff_list = list(map(int, sys.argv[4].split(",")))
    tol_len = int(sys.argv[5])
    tol_diff = int(sys.argv[6])

    bed_data = read_bed_file(bed_file)
    top_matches = find_patterns(bed_data, gene_list, len_list, diff_list, tol_len, tol_diff)

    # Print header
    print("Start\tEnd\tDirection\tExact_Length_Matches\tWithin_Tolerance_Length_Matches\tWithin_Tolerance_Diff_Matches\tP_value\tInserted_Genes\tDeleted_Genes")

    for start, end, direction, result in top_matches:
        print_result(start, end, direction, result)


if __name__ == "__main__":
    main()
