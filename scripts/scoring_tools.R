# Load necessary libraries
library(dplyr)

# Replace with the path to your CSV file
file_path <- "path_to_your_file.csv"

# Load your dataset
df <- read.csv(file_path)

# Define scoring function based on keywords
score_criterion <- function(text, keywords) {
  if (any(grepl(keywords[[3]], text, ignore.case = TRUE))) {
    return(3)
  } else if (any(grepl(keywords[[2]], text, ignore.case = TRUE))) {
    return(2)
  } else if (any(grepl(keywords[[1]], text, ignore.case = TRUE))) {
    return(1)
  } else {
    return(NA) # If no match is found, NA is returned
  }
}

# Define the keywords for each criterion (adjust as needed based on your actual data)
keywords <- list(
  Preservation_of_data_and_software = c("Not archived", "", "Archived tool and data"),
  Version_control_maintainance = c("No version control", "", "Complete version control"),
  Licensing_and_legal = c("Proprietary", "Open-source", "Fully open-source"),
  Community_engagement = c("No community engagement", "Community engagement - 1 platform", "Community engagement - >1 platform"),
  Testing_against_benchmarks = c("No testing", "Testing done on initial tool publication", "Frequent testing done with updates"),
  Containerization = c("Not containerized", "", "Containerized"),
  Workflow_management_system = c("No workflow", "", "A workflow management system is used"),
  Manual_documentation_logging_reporting = c("No manual", "No manual, good documentation", "Full manual"),
  Standardized_inputs_outputs = c("", "", "Formats can be converted to standardized inputs and outputs"),
  FAIR_principles = c("Unknown", "Possibly follows some", "Fully follows FAIR principles")
)

# Apply scoring to each criterion in your dataframe
df <- df %>%
  mutate(
    Score_Preservation = sapply(Preservation_of_data_and_software, score_criterion, keywords = keywords$Preservation_of_data_and_software),
    Score_Version = sapply(Version_control_maintainance, score_criterion, keywords = keywords$Version_control_maintainance),
    Score_Licensing = sapply(Licensing_and_legal, score_criterion, keywords = keywords$Licensing_and_legal),
    Score_Community = sapply(Community_engagement, score_criterion, keywords = keywords$Community_engagement),
    Score_Testing = sapply(Testing_against_benchmarks, score_criterion, keywords = keywords$Testing_against_benchmarks),
    Score_Containerization = sapply(Containerization, score_criterion, keywords = keywords$Containerization),
    Score_Workflow = sapply(Workflow_management_system, score_criterion, keywords = keywords$Workflow_management_system),
    Score_Documentation = sapply(Manual_documentation_logging_reporting, score_criterion, keywords = keywords$Manual_documentation_logging_reporting),
    Score_Standardization = sapply(Standardized_inputs_outputs, score_criterion, keywords = keywords$Standardized_inputs_outputs),
    Score_FAIR = sapply(FAIR_principles, score_criterion, keywords = keywords$FAIR_principles)
  )

# Check column names
colnames(df)

# Replace these with the actual column names
df <- df %>%
  mutate(
    Score_Preservation = sapply(df$`Preservation of data and software`, score_criterion, keywords = keywords$Preservation_of_data_and_software),
    Score_Version = sapply(df$`Version control - maintainance`, score_criterion, keywords = keywords$Version_control_maintainance),
    Score_Licensing = sapply(df$`Licensing and legal`, score_criterion, keywords = keywords$Licensing_and_legal),
    Score_Community = sapply(df$`Community engagement`, score_criterion, keywords = keywords$Community_engagement),
    Score_Testing = sapply(df$`Testing against benchmarks`, score_criterion, keywords = keywords$Testing_against_benchmarks),
    Score_Containerization = sapply(df$`Containerization`, score_criterion, keywords = keywords$Containerization),
    Score_Workflow = sapply(df$`Workflow management system`, score_criterion, keywords = keywords$Workflow_management_system),
    Score_Documentation = sapply(df$`Manual, documentation, logging, reporting`, score_criterion, keywords = keywords$Manual_documentation_logging_reporting),
    Score_Standardization = sapply(df$`Standardized inputs and outputs`, score_criterion, keywords = keywords$Standardized_inputs_outputs),
    Score_FAIR = sapply(df$`FAIR principles`, score_criterion, keywords = keywords$FAIR_principles)
  )

# Write the updated dataframe with scores to a new CSV file (or overwrite the original)
output_file <- "scored_tools.csv"
write.csv(df, output_file, row.names = FALSE)



