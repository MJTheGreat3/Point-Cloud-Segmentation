#!/bin/bash

# Define the directory where your PLY files are located.
# '.' means the current directory. Change this if your files are elsewhere.
PLY_DIR="."

echo "Starting batch processing of PLY files in $PLY_DIR..."
echo "--------------------------------------------------------"

# Loop through every file in the specified directory that ends with .ply
for INPUT_FILE in "$PLY_DIR"/*.ply; do
    
    # Check if the file exists (important if no .ply files are found)
    if [ ! -f "$INPUT_FILE" ]; then
        echo "No .ply files found in $PLY_DIR. Exiting loop."
        break
    fi

    # Create the output filename by appending '_modified' before the .ply extension
    OUTPUT_FILE="${INPUT_FILE%.ply}_modified.ply"

    echo "Processing: **$INPUT_FILE** -> Saving to **$OUTPUT_FILE**"
    
    # --- AWK Command to perform the change ---
    # The core logic remains the same: identify the header, and change $4 from 5.0 to 1.0 in the data.
    awk '
        # Header processing flag
        !header_end {
            print
            if ($0 ~ /^end_header/) {
                header_end = 1
            }
            next 
        }

        # Data processing (after "end_header")
        header_end {
            # $4 is the class property
            if ($4 == 5.000000) {
                $4 = 1.000000
            }
            print
        }
    ' "$INPUT_FILE" > "$OUTPUT_FILE"

    if [ $? -eq 0 ]; then
        echo "  [SUCCESS] $INPUT_FILE processed successfully."
    else
        echo "  [ERROR] Failed to process $INPUT_FILE."
    fi
    echo "---"

done

echo "Batch processing finished."