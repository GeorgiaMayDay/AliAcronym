import pandas as pd
import json

# Configuration
input_file = "Acronym Buster Data - adata - DO NOT MOVE.csv"
output_file = "acronyms.json"


def create_acronym_json():
    try:
        # Load the CSV file
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found. Please check the filename.")
        return

    # Fill NaN values with empty strings to avoid errors during processing
    df = df.fillna("")

    # Group by 'Acronym' to handle duplicates
    # This aggregates multiple definitions for the same acronym using a semicolon separator
    grouped = df.groupby('Acronym').agg({
        'Definition': lambda x: '; '.join(sorted(set([str(s).strip() for s in x if str(s).strip()]))),
        'Meaning': lambda x: '; '.join(sorted(set([str(s).strip() for s in x if str(s).strip()]))),
        'Department': lambda x: '; '.join(sorted(set([str(s).strip() for s in x if str(s).strip()])))
    }).reset_index()

    # Convert to the desired dictionary format
    final_dict = {}
    for index, row in grouped.iterrows():
        acronym = str(row['Acronym']).strip()

        # Skip empty acronyms
        if not acronym:
            continue

        final_dict[acronym] = {
            "meaning": row['Definition'],
            "description": row['Meaning'],
            "department": row['Department']
        }

    # Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(final_dict, f, indent=4)

    print(f"Success! Created {output_file} with {len(final_dict)} entries.")


if __name__ == "__main__":
    create_acronym_json()