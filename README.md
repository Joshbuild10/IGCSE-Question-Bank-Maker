# IGCSE Question Bank Maker
 A tool to split IGCSE Past Papers into individual questions, and query them to be compiled in a single Pdf.
This is still an early version and will be made more user-friendly in the near future.
## Usage
Please ensure all file names follow the format of the example: 0610_s21_qp_11.pdf. Otherwise, the program will not work 
properly, papers with that format can be downloaded from papers.gceguide.com.

### Prerequisites
The following python packages are going to need to be installed:
pypdf
reportlab

### Splitting the papers
To split the papers, copy all the IGCSE papers into the "papers" directory, and in script.py run the following:
```python
from splitter import Split
# Splits all the papers contained in the source directory "papers"
Split("papers")
```
This only needs to be run once, however if extra papers are added to the directory, it should be run again.
The command will split the papers into individual questions, and save them in the "questions" directory.

### Querying and compiling the questions
To query and then compile the questions, run the following:
```python
from query import Query
from merger import Merge

# Queries the database for all papers that contain the search string with a given similarity index
source = Query("questions/database.csv", [{"column_name": "text", "search_string": "trophic level", "similarity": 0.9}])

# Compiles the questions into a single pdf
Merge(source, "output.pdf")
```
The search string can be changed to whatever you want, and the similarity index can be changed to whatever you want and 
the list accepts multiple search strings (allowing for multiple conditions to be met). 
The similarity index determines how exact the matches should be, 1 being an exact match, and 0 being any match.
For words with different spellings/tenses 0.8 would generally be a good place to put the similarity index at.
The command will return a list of the filepath all the papers that contain the search string.
Note: the column name is the column of the database you want to the search string to be found in, these are the valid
columns that can currently be search: "subject_code", "year", "season", "paper", question", "filename", "text"

The merge function then takes the list of files and compiles them into a single pdf, which can be found in the "output"
file as provided in the example.