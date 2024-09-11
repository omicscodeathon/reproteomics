from gprofiler import GProfiler

# Create a gProfiler object
gp = GProfiler(return_dataframe=True)  # Use return_dataframe=True to get results as a pandas DataFrame

# Perform enrichment analysis
enrichment_results = gp.profile(
    query=["gene1", "gene2", "gene3"],  # List of genes
    organism="hsapiens",  # Organism
    sources=['GO:BP'],  # Functional categories (e.g., GO Biological Process)
    user_threshold=0.05  # Significance threshold
)

print(enrichment_results)
at 
