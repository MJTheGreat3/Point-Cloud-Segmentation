#!/bin/bash

# --- Configuration ---
INPUT_FILE="A1-A10_ongoing7.ply"
OUTPUT_FILE="modified_output.ply"

# Check if the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found."
    exit 1
fi

echo "Starting processing of $INPUT_FILE..."

# --- AWK Command to Remove the Last Column ---
# The AWK script logic:
# 1. /^(ply|format|comment|obj_info|element|property|end_header)/ { print; next }
#    - If a line starts with any of the PLY header keywords, print it and go to the next line (next).
# 2. { NF-- }
#    - For all other lines (the data lines), decrease the number of fields (NF) by 1.
#    - This effectively drops the last field/column.
# 3. { print }
#    - Print the modified line.
awk '
    /^(ply|format|comment|obj_info|element|property|end_header)/ {
        print;
        next
    }
    {
        NF--  # Decrease the Number of Fields (NF) by 1, dropping the last column
        print
    }
' "$INPUT_FILE" > "$OUTPUT_FILE"

# --- Modify Header (Important!) ---
# You need to update the header to reflect the removed property.
# The property being removed is "property float scalar_Original_cloud_index".
echo "Updating PLY header in $OUTPUT_FILE..."
sed -i.bak '/property float scalar_Original_cloud_index/d' "$OUTPUT_FILE"

echo "Processing complete."
echo "The modified data is in $OUTPUT_FILE."
echo "The original file remains unchanged."
echo "A backup of the original header is in ${OUTPUT_FILE}.bak."
