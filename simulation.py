import numpy as np
import argparse

def simulate_regions(num_regions, mean_length, std_length,
                     gene_types, gene_probs, mean_gap, std_gap, output_file):
    """
    Simulate non-overlapping BED regions across chr1–chr22 with specified parameters.
    Output columns: chromosome, start, end, length, gene_type
    """
    gene_probs = np.array(gene_probs, dtype=float)
    gene_probs = gene_probs / gene_probs.sum()  # Normalize proportions

    chroms = [f"chr{i}" for i in range(1, 23)]
    base = num_regions // 22
    extras = num_regions % 22
    regions_per_chr = [base + (1 if i < extras else 0) for i in range(22)]

    with open(output_file, 'w') as fout:
        for idx, count in enumerate(regions_per_chr, start=1):
            if count == 0:
                continue
            
            lengths = np.random.normal(mean_length, std_length, size=count)
            lengths = np.round(lengths).astype(int)
            lengths[lengths < 1] = 1  # enforce minimum of 1 bp

            gaps = np.random.normal(mean_gap, std_gap, size=count)
            gaps = np.round(gaps).astype(int)
            gaps[gaps < 0] = 0

            increments = np.empty(count, dtype=int)
            increments[0] = 0  # First region starts at 0
            if count > 1:
                increments[1:] = lengths[:-1] + gaps[1:]
            starts = np.cumsum(increments)
            ends = starts + lengths

            gene_choices = np.random.choice(gene_types, size=count, p=gene_probs)

            lines = []
            chrom = f"chr{idx}"
            for s, e, l, g in zip(starts, ends, lengths, gene_choices):
                lines.append(f"{chrom}\t{s}\t{e}\t{l}\t{g}\n")
            fout.write(''.join(lines))

def parse_args():
    parser = argparse.ArgumentParser(description="Simulate BED regions efficiently")
    parser.add_argument("--regions", type=int, default=10000, help="Total number of regions")
    parser.add_argument("--mean_length", type=float, default=1000, help="Mean region length")
    parser.add_argument("--std_length", type=float, default=100, help="Standard deviation of region length")
    parser.add_argument("--gene_types", nargs='+', default=["gene", "pseudogene"],
                        help="List of gene type labels")
    parser.add_argument("--gene_props", nargs='+', type=float, default=[0.7, 0.3],
                        help="Proportions for each gene type (same order as gene_types)")
    parser.add_argument("--mean_gap", type=float, default=100, help="Mean gap between regions")
    parser.add_argument("--std_gap", type=float, default=10, help="Std dev of gap between regions")
    parser.add_argument("--output", type=str, default="regions.bed", help="Output BED filename")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    simulate_regions(
        num_regions=args.regions,
        mean_length=args.mean_length,
        std_length=args.std_length,
        gene_types=args.gene_types,
        gene_probs=args.gene_props,
        mean_gap=args.mean_gap,
        std_gap=args.std_gap,
        output_file=args.output
    )
