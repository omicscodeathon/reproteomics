# Load necessary libraries
library(dplyr)

# Read in dataset
tool_data <- read.csv("tool_scoring.csv", check.names = TRUE)  # check.names = TRUE will ensure all columns have valid names

# Check for any missing or NA column names
colnames(tool_data) <- ifelse(colnames(tool_data) == "" | is.na(colnames(tool_data)), paste0("Unnamed_Col_", seq_along(colnames(tool_data))), colnames(tool_data))

# Rename the columns to replace periods with underscores
colnames(tool_data) <- gsub("\\.", "_", colnames(tool_data))

# Function to assign ratings based on my criteria
rate_tool <- function(Preservation_of_data_and_software, Version_control, Licensing_and_legal, 
                      Community_engagement, Assessment_against_benchmarks, Containerization, 
                      Workflow_management_systems, Documentation, 
                      Standardized_input_and_output_formats, Scalability_and_parallelization) {
  
  # Initialize rating variables
  version_control_rating <- 0
  licensing_and_legal_rating <- 0
  community_engagement_rating <- 0
  testing_benchmark_rating <- 0
  containerization_rating <- 0
  workflow_management_rating <- 0
  documentation_rating <- 0
  standardized_io_rating <- 0
  scalability_rating <- 0
  preservation_rating <- 0
  
  # Preservation of data and software rating
  if (Preservation_of_data_and_software == "Both tool and data are archived in trusted, well-maintained repositories (e.g., Zenodo, ProteomeXchange).") {
    preservation_rating <- 3
  } else if (Preservation_of_data_and_software == "Archived data or tool in a trusted repository.") {
    preservation_rating <- 2
  } else if (Preservation_of_data_and_software == "Not archived or hosted in unreliable locations.") {
    preservation_rating <- 1
  }
  
  # Version control rating
  if (Version_control == "Comprehensive version control with regular updates, clear changelogs, and active maintenance.") {
    version_control_rating <- 3
  } else if (Version_control == "Minimal or inconsistent version control, tool still functional but not actively maintained.") {
    version_control_rating <- 2
  } else if (Version_control == "No version control, tool is deprecated or unreliable.") {
    version_control_rating <- 1
  }
  
  # Licensing and legal rating
  if (Licensing_and_legal == "Fully open-source with a permissive license (e.g., MIT, Apache), code publicly available.") {
    licensing_and_legal_rating <- 3
  } else if (Licensing_and_legal == "Open source but with restrictions (e.g., limited commercial use or missing code access).") {
    licensing_and_legal_rating <- 2
  } else if (Licensing_and_legal == "Proprietary or restricted access, requires payment or a limited free trial.") {
    licensing_and_legal_rating <- 1
  }
  
  # Community engagement rating
  if (Community_engagement == "Active engagement across multiple platforms (e.g., GitHub, forums, Q&A sites) with regular interactions.") {
    community_engagement_rating <- 3
  } else if (Community_engagement == "Minimal engagement, limited to one platform (e.g., GitHub issues or a single forum).") {
    community_engagement_rating <- 2
  } else if (Community_engagement == "No evidence of community engagement or support.") {
    community_engagement_rating <- 1
  }
  
  # Testing against benchmarks rating
  if (Assessment_against_benchmarks == "Regular benchmarking and validation against widely accepted datasets with updates.") {
    testing_benchmark_rating <- 3
  } else if (Assessment_against_benchmarks == "Tested only at the time of initial tool publication.") {
    testing_benchmark_rating <- 2
  } else if (Assessment_against_benchmarks == "No benchmarking or testing reported.") {
    testing_benchmark_rating <- 1
  }
  
  # Containerization rating
  if (Containerization == "Fully containerized (e.g., Docker, Singularity) with comprehensive dependency management.") {
    containerization_rating <- 3
  } else if (Containerization == "Partially containerized, e.g., as part of a broader pipeline or incomplete container.") {
    containerization_rating <- 2
  } else if (Containerization == "Not containerized or dependency management is manual.") {
    containerization_rating <- 1
  }
  
  # Workflow management system rating
  if (Workflow_management_systems == "Fully compatible and integrated with workflow management systems for automation.") {
    workflow_management_rating <- 3
  } else if (Workflow_management_systems == "Usable as part of a pipeline in workflow systems (e.g., Snakemake, Galaxy).") {
    workflow_management_rating <- 2
  } else if (Workflow_management_systems == "Cannot integrate into workflow management systems.") {
    workflow_management_rating <- 1
  }
  
  # Manual, documentation, logging, and reporting rating
  if (Documentation == "Detailed manual, thorough and clear documentation, and complete logging/reporting.") {
    documentation_rating <- 3
  } else if (Documentation == "Sufficient documentation but lacks a manual or comprehensive logging/reporting.") {
    documentation_rating <- 2
  } else if (Documentation == "Lacks a manual; minimal or unclear documentation, logging, or reporting.") {
    documentation_rating <- 1
  }
  
  # Standardized inputs and outputs rating
  if (Standardized_input_and_output_formats == "Uses standardized formats directly, ensuring seamless interoperability with other tools.") {
    standardized_io_rating <- 3
  } else if (Standardized_input_and_output_formats == "Formats are non-standard but can be converted with effort.") {
    standardized_io_rating <- 2
  } else if (Standardized_input_and_output_formats == "Input/output formats are unknown or non-standard.") {
    standardized_io_rating <- 1
  }
  
  # Scalability and parallelization rating
  if (Scalability_and_parallelization == "The tool is designed for high scalability and parallelization, capable of efficiently processing very large datasets. It supports distributed computing, cloud platforms, and HPC environments, with optimization for resource allocation and task distribution.") {
    scalability_rating <- 3
  } else if (Scalability_and_parallelization == "The tool supports basic scalability. It can handle moderately large datasets but may not fully utilize advanced computational resources.") {
    scalability_rating <- 2
  } else if (Scalability_and_parallelization == "The tool has unknown or no built-in scalability or parallelization capabilities. It struggles to handle large datasets efficiently and cannot leverage cloud or HPC resources.") {
    scalability_rating <- 1
  }
  
  # Calculate the final rating as the average of the ratings, rounded to the nearest whole number
  final_rating <- round(mean(c(version_control_rating, licensing_and_legal_rating, 
                               community_engagement_rating, testing_benchmark_rating, 
                               containerization_rating, workflow_management_rating, 
                               documentation_rating, standardized_io_rating, 
                               scalability_rating), na.rm = TRUE))
  
  return(final_rating)
}

# Apply the function to each row of the dataset
tool_data <- tool_data %>%
  mutate(Rating = mapply(rate_tool, Preservation_of_data_and_software, Version_control, Licensing_and_legal, 
                         Community_engagement, Assessment_against_benchmarks, Containerization, 
                         Workflow_management_systems, Documentation, 
                         Standardized_input_and_output_formats, Scalability_and_parallelization))

# Save the updated dataset as a table
write.table(tool_data, "ranked_tools.tsv", sep = "\t", row.names = FALSE, quote = FALSE)
