# Load necessary library
library(dplyr)
library(httr) # For checking URL responses

# Read in the TSV file
tools_df <- read.csv("proteomic_latest.tsv", sep = "\t", stringsAsFactors = FALSE)

#Filter tools that are open source or have no entry in the License column
tools_filtered <- tools_df %>%
  filter(grepl("Open access|None", Accessibility, ignore.case = TRUE) | License == "")

# Keep tools with the words 'protein', 'proteomics', 'proteins', or 'proteomic' in the Topic column
tools_filtered <- tools_filtered %>%
  filter(grepl("Protein|Proteomic|Proteome|Proteogenomic", Topic, ignore.case = TRUE))

# Remove tools that are web applications in the Tool Type column
#tools_filtered <- tools_filtered %>%
#filter(!grepl("web application|desktop application", Tool.Type, ignore.case = TRUE))

# Keep command line tools, workflow, script, library
tools_filtered <- tools_filtered %>%
  filter(grepl("Command-line tool|Script|Library|Workflow", Tool.Type, ignore.case = TRUE))

# Remove tools with specific words
tools_filtered <- tools_filtered %>%
  filter(!grepl("Transcriptomic|Genomic|Gene|Genetic|Transcription|RNA|DNA|Nucleic|Microarray|Transcript|Chemistry|Physics|ChIP|Exome|Genome", Topic, ignore.case = TRUE))

# Remove tools with no DOI available
tools_filtered <- tools_filtered %>%
  filter(!grepl("None", DOI, ignore.case = TRUE))

# Function to check if a URL is valid (i.e., does not return a 404 error)
check_url <- function(url) {
  if (is.na(url) || url == "") {
    return(FALSE) # Treat empty or missing URLs as invalid
  }
  response <- try(GET(url), silent = TRUE) # Try to connect to the URL
  if (inherits(response, "try-error")) {
    return(FALSE) # If an error occurs during the connection, treat it as invalid
  }
  return(status_code(response) != 404) # Return TRUE if the status code is not 404 (i.e., valid URL)
}

# Check homepage URLs for validity (remove tools with invalid URLs or 404 errors)
tools_filtered <- tools_filtered %>%
  rowwise() %>%
  filter(check_url(Homepage)) %>% # Apply the URL check
  ungroup()

# Write the filtered data to a new TSV file
write.table(tools_filtered, "filtered_proteomic_tools.tsv", sep = "\t", row.names = FALSE, quote = FALSE)
