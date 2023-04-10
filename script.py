from splitter import Split
from merger import Merge
from query import Query

# Splits all the papers contained in the source directory "papers"
Split("papers")


# Queries the database for all papers that contain the search string with a given similarity index
source = Query("questions/database.csv", [{"column_name": "text", "search_string": "trophic level", "similarity": 0.9}])

# Merges all the papers that match the query into one pdf
Merge(source, "test.pdf")
