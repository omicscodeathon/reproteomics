# Load necessary library
library(dplyr)

# Read in the TSV file
tools_df <- read.csv("proteomics.tsv", sep = "\t", stringsAsFactors = FALSE)

#Filter tools that are open source or have no entry in the License column
tools_filtered <- tools_df %>%
  filter(grepl("Open access|None", Accessibility, ignore.case = TRUE) | License == "")

# Keep tools with the words 'protein', 'proteomics', 'proteins', or 'proteomic' in the Topic column
tools_filtered <- tools_filtered %>%
  filter(grepl("Protein|Proteomics|Proteins|Proteomic", Topic, ignore.case = TRUE))

# Remove tools that are web applications in the Tool Type column
tools_filtered <- tools_filtered %>%
  filter(!grepl("web application|desktop application", Tool.Type, ignore.case = TRUE))

# Remove tools with specific words
tools_filtered <- tools_filtered %>%
  filter(!grepl("Proteogenomics|Proteogenomic|Transcriptomic|Transcriptomics|Genomics|Transcription|RNA-Seq|Zoology|Microbiology|Animal|Plant|RNA|Ecology", Topic, ignore.case = TRUE))

# Remove tools with no DOI available
tools_filtered <- tools_filtered %>%
  filter(!grepl("None", DOI, ignore.case = TRUE))

# Write the filtered data to a new TSV file
write.table(tools_filtered, "filtered_tools.tsv", sep = "\t", row.names = FALSE, quote = FALSE)
