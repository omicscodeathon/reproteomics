import gseapy as gp
import pandas as pd

# Set paths for input data and gene sets
abundance_matrix_file = "abundance_matrix.txt"
protein_sets_file = "HYPOCHROMIC_MICROCYTIC_ANEMIA.gmt"

# Load the abundance matrix (rows = proteins, columns = samples)
abundance_df = pd.read_csv(abundance_matrix_file, sep="\t", index_col=0)

# Load protein-centric gene sets
protein_sets = gp.gsea.GeneSets(protein_sets_file)

# Perform ssGSEA
result = gp.ssgsea(data=abundance_df, gene_sets=protein_sets)

# Print top enriched pathways
enriched_pathways = result.res2d.sort_values("fdr", ascending=True)
print("Top enriched pathways:")
print(enriched_pathways.head(10))

# Save the ssGSEA results to a CSV file
output_file = "ssgsea_results_proteins.csv"
result.res2d.to_csv(output_file, sep="\t")
print(f"Results saved to {output_file}")
