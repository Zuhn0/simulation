import argparse

def extract_rows(infile, outfile, start_row, end_row):
    with open(infile, 'r') as fin:
        lines = fin.readlines()

    # BED file lines start from index 0
    selected_lines = lines[start_row - 1:end_row]  # Adjust for 1-based input

    with open(outfile, 'w') as fout:
        fout.writelines(selected_lines)

    print(f"Extracted rows {start_row} to {end_row} into '{outfile}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract specific row range from a BED file.")
    parser.add_argument("infile", help="Input BED file")
    parser.add_argument("outfile", help="Output file for extracted rows")
    parser.add_argument("start", type=int, help="Start row number (1-based)")
    parser.add_argument("end", type=int, help="End row number (inclusive, 1-based)")
    args = parser.parse_args()

    extract_rows(args.infile, args.outfile, args.start, args.end)
