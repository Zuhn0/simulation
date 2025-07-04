import argparse, sys

def parse_args():
    parser = argparse.ArgumentParser(description="Simulate mutations on a BED file")
    parser.add_argument("infile", help="Input BED filename (tab-delimited, 5 columns)")
    parser.add_argument("outfile", help="Output mutated BED filename")
    parser.add_argument("-d", "--delete", action="append",
                        help="Region to delete (format CHR:START-END or gene name)")
    parser.add_argument("--dup", action="append",
                        help="Region to duplicate (format CHR:START-END[@CHR:NEWSTART])")
    parser.add_argument("-v", "--invert", action="append",
                        help="Region to invert (format CHR:START-END or gene name)")
    parser.add_argument("-i", "--insert", action="append",
                        help="Insertion (format CHR:POS:LENGTH:GENE)")
    return parser.parse_args()

def main():
    args = parse_args()

    try:
        with open(args.infile) as f:
            bed_records = []
            for line in f:
                line = line.strip()
                if not line: continue
                cols = line.split("\t")
                if len(cols) != 5:
                    print(f"Error: Invalid BED line (expected 5 columns): {line}")
                    sys.exit(1)
                chrom, start, end, length, gene = cols
                try:
                    start = int(start); end = int(end); length = int(length)
                except ValueError:
                    print(f"Error: Non-integer value in BED line: {line}")
                    sys.exit(1)
                bed_records.append([chrom, start, end, length, gene])
    except FileNotFoundError:
        print(f"Error: Input file '{args.infile}' not found.")
        sys.exit(1)

       # Perform deletions
    if args.delete:
        for reg in args.delete:
            if "@" in reg:
                gene, start_str = reg.split("@", 1)
                try:
                    start = int(start_str)
                except ValueError:
                    print(f"Error: Invalid start coordinate in delete '{reg}'")
                    sys.exit(1)
                matches = [rec for rec in bed_records if rec[4] == gene and rec[1] == start]
            else:
                print(f"Error: For deletion, use format GENE@START (e.g. G1@502)")
                sys.exit(1)

            if not matches:
                print(f"Error: Deletion target '{reg}' not found.")
                sys.exit(1)
            for rec in matches:
                bed_records.remove(rec)

        # duplications
    if args.dup:
        for reg in args.dup:
            parts = reg.split("@")
            src = parts[0]
            chrom, rest = src.split(":", 1)
            start, end = map(int, rest.split("-", 1))
            matches = [rec for rec in bed_records if rec[0]==chrom and rec[1]==start and rec[2]==end]
            if not matches:
                print(f"Error: Duplication target '{src}' not found.")
                sys.exit(1)
            orig = matches[0]
            new_chrom = orig[0]
            new_start = orig[1]
            new_end = orig[2]
            if len(parts) > 1 and parts[1]:
                dest = parts[1]
                if ":" in dest:
                    new_chrom, new_start = dest.split(":")
                    new_start = int(new_start)
                else:
                    new_start = int(dest)
                length = orig[2] - orig[1]
                new_end = new_start + length
            else:
                length = orig[2] - orig[1]
                new_end = new_start + length

            # Shift downstream genes
            for rec in bed_records:
                if rec[0] == new_chrom and rec[1] >= new_start:
                    rec[1] += length
                    rec[2] += length
            for rec in bed_records:
                if rec[0] > new_chrom:
                    rec[1] += length
                    rec[2] += length

            new_length = new_end - new_start
            bed_records.append([new_chrom, new_start, new_end, new_length, orig[4]])

       # Handle inversions
    if args.invert:
        for reg in args.invert:
            if ":" in reg and "-" in reg:
                chrom, rest = reg.split(":", 1)
                start, end = map(int, rest.split("-", 1))
                matches = [rec for rec in bed_records if rec[0]==chrom and rec[1]==start and rec[2]==end]
            else:
                # Match ALL records by gene name
                matches = [rec for rec in bed_records if rec[4] == reg]
            if not matches:
                print(f"Error: Inversion target '{reg}' not found.")
                sys.exit(1)
            for rec in matches:
                # Flip start and end literally
                rec[1], rec[2] = rec[2], rec[1]  # reversed coordinates
                rec[3] = -(abs(rec[1] - rec[2]))  # negative length
                # Gene name stays the same



            # Handle insertions
    if args.insert:
        for reg in args.insert:
            parts = reg.split(":", 3)
            if len(parts) != 4:
                print(f"Error: Insert format must be CHR:POS:LENGTH:GENE, got '{reg}'")
                sys.exit(1)
            chrom, pos_str, length_str, gene = parts
            pos = int(pos_str)
            length = int(length_str)
            overlap = [rec for rec in bed_records if rec[0]==chrom and rec[1] < pos < rec[2]]
            if overlap:
                print(f"Error: Insertion at {chrom}:{pos} overlaps existing gene {overlap[0][4]}")
                sys.exit(1)
            for rec in bed_records:
                if rec[0]==chrom and rec[1] >= pos:
                    rec[1] += length
                    rec[2] += length
            for rec in bed_records:
                if rec[0] > chrom:
                    rec[1] += length
                    rec[2] += length
            new_rec = [chrom, pos, pos+length, length, gene]
            bed_records.append(new_rec)

    # Sort output
    def chr_sort_key(rec):
        chrom = rec[0]
        if chrom.startswith("chr"):
            chrom = chrom[3:]
        try:
            return (int(chrom), rec[1])
        except ValueError:
            return (chrom, rec[1])
    bed_records.sort(key=chr_sort_key)

    # Write to output file
    try:
        with open(args.outfile, 'w') as out:
            for chrom, start, end, length, gene in bed_records:
                out.write(f"{chrom}\t{start}\t{end}\t{length}\t{gene}\n")
    except IOError as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print(f"Mutated BED written to {args.outfile}")

if __name__ == "__main__":
    main()
