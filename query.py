# Import the csv and difflib modules
import csv
import difflib

# Function that queries the csv file and returns a list of rows that match all the parameters
def Query(csv_file="questions/database.csv", parameters = [{"column_name": "text", "search_string": "OESTROGEN", "similarity": 0.8}]):
    # Create an empty list to store the matching rows
    matching_rows = []
    # Open the csv file in read mode
    with open(csv_file, "r", encoding="utf-8") as f:

        # Create a csv reader object
        reader = csv.DictReader(f)

        # Loop through each row in the csv file
        for row in reader:
            # Flag to indicate if the row matches all the parameters
            flag = 1
            for parameter in parameters:
                # Capitalises and remove all whitespace from the search string
                parameter["search_string"] = parameter["search_string"].upper().replace(" ", "")

                # Get the column value and its length
                column_value = row[parameter["column_name"]]
                column_length = len(column_value)

                # Get the length of the search string
                search_length = len(parameter["search_string"])
                max_similarity = 0

                # Loop through each possible starting position of a substring in the column value
                for i in range(column_length - search_length + 1):

                    # Skips entries that doesn't have the first letter match
                    if column_value[i] != parameter["search_string"][0]:
                        continue

                    # Get the substring of the column value that starts at position i and has the same length as the search string
                    substring = column_value[i: i + search_length]

                    # Calculate the similarity ratio between the substring and the search string
                    similarity_ratio = difflib.SequenceMatcher(None, substring, parameter["search_string"]).ratio()
                    max_similarity = max(max_similarity, similarity_ratio)

                # Check if the max similarity ratio is below the threshold and set the flag to 0
                if max_similarity < parameter["similarity"]:
                    flag = 0
                    break
            if flag:
                matching_rows.append(row["filename"])

    #print(matching_rows) # Debugging
    return(matching_rows)