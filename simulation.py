import numpy as np
import argparse

def simulate_regions(num_regions, mean_length, std_length,
                     gene_types, gene_probs, mean_gap, std_gap, output_file):
    """
    Simulate non-overlapping BED regions across chr1–chr22 with specified parameters.
    Regions are generated in ascending order by chromosome and start position.
    """
    # Ensure probabilities sum to 1
    gene_probs = np.array(gene_probs, dtype=float)
    gene_probs = gene_probs / gene_probs.sum()

    # Evenly distribute regions across 22 chromosomes
    base = num_regions // 22
    extras = num_regions % 22
    regions_per_chr = [base + (1 if i < extras else 0) for i in range(22)]

    with open(output_file, 'w') as fout:
        for idx, count in enumerate(regions_per_chr, start=1):
            if count == 0:
                continue  # Skip if no regions for this chromosome
            
            # Generate random region lengths (normal distribution, clipped to >=1)
            lengths = np.random.normal(mean_length, std_length, size=count)
            lengths = np.round(lengths).astype(int)
            lengths[lengths < 1] = 1  # Enforce minimum length of 1 to avoid zero-length
            
            # Generate random gaps between regions (normal distribution, clipped to >=0)
            gaps = np.random.normal(mean_gap, std_gap, size=count)
            gaps = np.round(gaps).astype(int)
            gaps[gaps < 0] = 0  # No negative gaps
            
            # Compute start positions by cumulative sum of lengths+gaps
            # increments[0] = initial gap; increments[i>0] = lengths[i-1] + gaps[i]
            increments = np.empty(count, dtype=int)
            increments[0] = gaps[0]
            if count > 1:
                increments[1:] = lengths[:-1] + gaps[1:]
            starts = np.cumsum(increments)
            
            # Compute end positions
            ends = starts + lengths
            
            # Assign gene types based on specified probabilities
            gene_choices = np.random.choice(gene_types, size=count, p=gene_probs)
            
            # Build output lines for this chromosome
            # Use join on a list of strings for efficient writing:contentReference[oaicite:4]{index=4}.
            lines = []
            chrom = f"chr{idx}"
            for s, e, g in zip(starts, ends, gene_choices):
                lines.append(f"{chrom}\t{s}\t{e}\t{g}\n")
            fout.write(''.join(lines))

def parse_args():
    parser = argparse.ArgumentParser(description="Simulate BED regions efficiently")
    parser.add_argument("--regions", type=int, default=10000,
                        help="Total number of regions to generate (10k–50k)")
    parser.add_argument("--mean_length", type=float, default=1000,
                        help="Mean region length")
    parser.add_argument("--std_length", type=float, default=100,
                        help="Standard deviation of region length")
    parser.add_argument("--gene_types", nargs='+', default=["gene", "pseudogene"],
                        help="List of gene type labels")
    parser.add_argument("--gene_props", nargs='+', type=float, default=[0.7, 0.3],
                        help="Proportions for each gene type (same order as gene_types)")
    parser.add_argument("--mean_gap", type=float, default=100,
                        help="Mean gap between regions within a chromosome")
    parser.add_argument("--std_gap", type=float, default=10,
                        help="Std dev of gap between regions")
    parser.add_argument("--output", type=str, default="regions.bed",
                        help="Output BED filename")
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
