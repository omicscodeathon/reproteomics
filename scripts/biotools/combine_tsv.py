# First import necessary libraries
import pandas as pd  # Data manipulation
import argparse  # Command-line arguments
from pathlib import Path  # File path handling
import logging  # Display messages 

# Set up logging to display messages with timestamps and the level of importance
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# This creates the function to combine all tsv files in a directory
def combine_tsv(directory, include_source):
    dataframes = []  # Creates an empty list to store data from each tsv file
    directory = Path(directory)  # Converts the directory path to a Path object for easier handling

    # Check if the provided directory does exist
    if not directory.exists():
        logging.error(f"Directory {directory} does not exist.")  # Log an error if the directory does not exist
        return None  # Stop the function and return nothing if the directory does not exist

    # Find all tsv files in the directory
    tsv_files = list(directory.glob("*.tsv"))  # Use the glob method to list all files ending with .tsv "finds all the pathnames matching a specified pattern according to the rules, results are returned in arbitrary order""

    # Checks if there are no tsv files in the directory
    if not tsv_files:
        logging.warning(f"No tsv files found in directory {directory}.")  # Log a warning if no files are found
        return None  # Stop the function and return nothing if not tsv files found

    # Loop through each tsv file found in the directory
    for filepath in tsv_files:
        try:
            # Try to read the tsv file, skipping any lines that cause problems
            df = pd.read_csv(filepath, sep='\t', on_bad_lines='skip')

            # If I want to add the source file name and the column doesn't already exist
            if include_source and "Source File" not in df.columns:
                # Add a new column called "Source File" at the start, with the file name (without tsv extension)
                df.insert(0, "Source File", filepath.stem)
            
            # Add the dataframe (the data from the file) to the list of dataframes
            dataframes.append(df)
        
        # If there's an error while reading the appended file, log the error message
        except Exception as e:
            logging.error(f"Error reading {filepath.name}: {e}")

    # If there are any dataframes in the list (files found)
    if dataframes:
        # Combine all the dataframes into one large dataframe
        combined_df = pd.concat(dataframes, ignore_index=True)
        return combined_df  # Return the combined dataframe
    else:
        # If no files were successfully read, log an error
        logging.error("No valid data to combine.")
        return None  # Stop the function and return nothing

# Main function to handle command-line arguments and run the script
def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Combine tsv files from a directory into one.')
    
    # tsv directory
    parser.add_argument('directory', type=str, help='The directory containing the tsv files.')
    
    # Output file name
    parser.add_argument('output', type=str, help='The output tsv file.')
    
    # Optional: to add source file name as a column
    parser.add_argument('--include-source', action='store_true', help='Include a column with the source file name.')
    
    # Parse the provided arguments
    args = parser.parse_args()

    # Call the arguments
    combined_df = combine_tsv(args.directory, args.include_source)

    # If combining was successful
    if combined_df is not None:
        # Save the combined dataframe to the specified output file
        combined_df.to_csv(args.output, sep='\t', index=False)
        logging.info(f"Combined tsv saved to {args.output}")  # Log a message indicating success
    else:
        # If combining wasn't successful, log an error
        logging.error("Failed to combine tsv files.")

if __name__ == "__main__":
    main()
