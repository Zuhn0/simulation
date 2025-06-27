import argparse
import random
import numpy as np

def simulate_bed(num_regions, mean_len, sd_len, genes, mean_dist, sd_dist, output):
    # Define chromosome names chr1..chr22
    chroms = [f"chr{i}" for i in range(1, 23)]
    # Track the last end coordinate used on each chromosome
    last_end = {chrom: 0 for chrom in chroms}
    regions = []
    
    for _ in range(num_regions):
        # Draw a positive region length from N(mean_len, sd_len)
        length = 0
        while length < 1:
            length = int(round(np.random.normal(mean_len, sd_len)))
        
        # Draw a positive distance to the previous region
        distance = 0
        while distance < 1:
            distance = int(round(np.random.normal(mean_dist, sd_dist)))
        
        # Randomly pick a chromosome
        chrom = random.choice(chroms)
        
        # Compute start: if no region yet on this chromosome, use 'distance' as start; 
        # else place after last_end + distance
        if last_end[chrom] == 0:
            start = distance
        else:
            start = last_end[chrom] + distance
        
        end = start + length  # end coordinate
        last_end[chrom] = end  # update last end for this chromosome
        
        # Pick a random gene type from the provided list
        gene = random.choice(genes)
        
        # Record the region
        regions.append((chrom, start, end, length, gene))
    
    # Sort regions by chromosome index and start position
    chrom_index = {f"chr{i}": i for i in range(1, 23)}
    regions.sort(key=lambda x: (chrom_index[x[0]], x[1]))
    
    # Write output to BED file
    with open(output, 'w') as f:
        for chrom, start, end, length, gene in regions:
            f.write(f"{chrom}\t{start}\t{end}\t{length}\t{gene}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate a BED file of random regions")
    parser.add_argument("-n", "--number", type=int, required=True,
                        help="Number of regions to simulate")
    parser.add_argument("-L", "--mean_length", type=float, required=True,
                        help="Mean length of each region")
    parser.add_argument("-S", "--sd_length", type=float, required=True,
                        help="Standard deviation of region length")
    parser.add_argument("-g", "--genes", nargs="+", required=True,
                        help="List of gene types (space-separated)")
    parser.add_argument("-D", "--mean_distance", type=float, required=True,
                        help="Mean distance between regions")
    parser.add_argument("-T", "--sd_distance", type=float, required=True,
                        help="Standard deviation of distance")
    parser.add_argument("-o", "--output", default="simulated_output.bed",
                        help="Output BED file name")
    args = parser.parse_args()
    
    simulate_bed(args.number, args.mean_length, args.sd_length,
                 args.genes, args.mean_distance, args.sd_distance, args.output)
