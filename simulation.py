import argparse
import random
import numpy as np

def simulate_bed(num_regions, mean_len, sd_len, gene_entries, mean_chrom_gap, sd_chrom_gap, output):
    chroms = [f"chr{i}" for i in range(1, 2006)]
    total_chroms = len(chroms)

    # Parse gene list and weights
    if len(gene_entries) % 2 != 0:
        raise ValueError("Each gene must be followed by its percentage.")
    genes = gene_entries[::2]
    weights = list(map(float, gene_entries[1::2]))
    if sum(weights) != 100:
        raise ValueError("Gene percentages must sum to 100.")

    regions_per_chrom = [num_regions // total_chroms] * total_chroms
    for i in range(num_regions % total_chroms):
        regions_per_chrom[i] += 1

    regions = []
    global_position = 0

    for chrom_index, chrom in enumerate(chroms):
        num_regions_this_chrom = regions_per_chrom[chrom_index]

        if chrom_index > 0:
            gap = 0
            while gap < 1:
                gap = int(round(np.random.normal(mean_chrom_gap, sd_chrom_gap)))
            global_position += gap

        current_pos = global_position

        for _ in range(num_regions_this_chrom):
            length = 0
            while length < 1:
                length = int(round(np.random.normal(mean_len, sd_len)))

            start = current_pos
            end = start + length
            gene = random.choices(genes, weights=weights, k=1)[0]

            regions.append((chrom, start, end, length, gene))
            current_pos = end + 1

        global_position = current_pos

    chrom_index_map = {f"chr{i}": i for i in range(1, 2006)}
    regions.sort(key=lambda x: (chrom_index_map.get(x[0], 0), x[1]))

    with open(output, 'w') as f:
        for chrom, start, end, length, gene in regions:
            f.write(f"{chrom}\t{start}\t{end}\t{length}\t{gene}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate BED file with gene type percentages")
    parser.add_argument("-n", "--number", type=int, required=True, help="Total number of regions")
    parser.add_argument("-L", "--mean_length", type=float, required=True, help="Mean region length")
    parser.add_argument("-S", "--sd_length", type=float, required=True, help="Standard deviation of region length")
    parser.add_argument("-g", "--genes", nargs="+", required=True,
                        help="List of gene types and their percentages. Example: -g ADCY10 40 MRPL19 30 C2orf3 30")
    parser.add_argument("-D", "--mean_chrom_gap", type=float, required=True, help="Mean distance between chromosomes")
    parser.add_argument("-T", "--sd_chrom_gap", type=float, required=True, help="Standard deviation of chromosome gap")
    parser.add_argument("-o", "--output", default="simulated_output.bed", help="Output BED file name")

    args = parser.parse_args()

    simulate_bed(
        args.number,
        args.mean_length,
        args.sd_length,
        args.genes,
        args.mean_chrom_gap,
        args.sd_chrom_gap,
        args.output
    )
