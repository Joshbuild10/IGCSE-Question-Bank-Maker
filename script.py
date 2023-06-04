from splitter import Split
from merger import Merge
from query import Query, ParseInput

isLoading = input(r"Do you want to load new papers from the 'papers' directory into the database? (y/n): ")

if isLoading == "y":
    # Splits all the papers contained in the source directory "papers"
    Split("papers")

# Queries the database for all papers that contain the search string with a given similarity index
#source = Query("questions/database.csv", [{"column_name": "text", "search_string": "trophic level", "similarity": 0.9},
#                                          {"column_name": "subject_code", "search_string": "0610", "similarity": 1}])

isLoading = input(r"Do you want to query any loaded papers? (y/n): ")

if isLoading == "y":
    inputString = input(r"Enter a search string with the example format: text=trophic level, similarity=0.9  AND "
                        r"subject_code=0610" + "\n")

    # Queries the database for all papers that contain the search string with a given similarity index
    source = Query("questions/database.csv", ParseInput(inputString))

    # Merges all the papers that match the query into one pdf
    Merge(source, "test.pdf")

# Asks the user to press enter to exit the program
input("Press enter to exit the program")