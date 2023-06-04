# IGCSE Question Bank Maker
 A tool to split IGCSE Past Papers into individual questions, and query them to be compiled in a single Pdf.
This is still an early version and will be made more user-friendly in the near future.

## Getting Started
Please ensure all file names follow the format of the example: 0610_s21_qp_11.pdf. Otherwise, the program will not work 
properly, papers with that format can be downloaded from papers.gceguide.com.

### Prerequisites
The following python packages are going to need to be installed if running script.py:

pymupdf

### Usage
To run the program, simply run the script.exe file or script.py (if you have a python compiler).
The program will ask if you want to load new papers contained in the papers folder, or use the ones already loaded.
Afterwards, it will ask you if you want to query the papers to be compiled into a single pdf.
If you choose to do so, you will be asked to provide the query in the format displayed.
The program will then compile the pdf and save it in the output folder.

### Example
```console
python script.py
Do you want to load new papers from the 'papers' directory into the database? (y/n): y
0606_S10_21 loaded into database: 2/2 
Finished loading all papers into database
Do you want to query any loaded papers? (y/n): y
Enter a search string with the example format: text=trophic level, similarity=0.9  AND subject_code=0610
text=trophic level, similarity=0.9  AND subject_code=0610
31 number of matching questions were found
questions\0610\2020\0610_S20_41-Q5.pdf on page 45 loaded into pdf 
 All pages loaded into pdf
```

### Loading new papers
To load new papers, simply place them in the papers folder and run the script.py/script.exe file.
Type y when prompted to load new papers.
The program will then load all the papers in the papers folder into the database.
The program will only load papers that are not already in the database,
so you can run the program multiple times on the same folder without worrying about duplicates.

As the papers are loads, a message will be displayed showing the progress of the loading process.
Any papers that failed to load will be printed to console.

### Querying papers
To query papers, type the y when prompted to query papers.
The program will then ask you to enter a query in the format displayed.
The format goes ```<column_name>=<value>, similarity=<value> AND <column_name>=<value>, similarity=<value> ...```

The similarity parameter is optional and defaults to 1 when omitted. It is used to specify how exact the match should be. 
The similarity parameter is a number between 0 and 1.
A similarity of 1 means that the match must be exact, while a similarity of 0 means that the match can be anything.

The column names are the names of the columns in the database. Valid column names are: 
```"subject_code", "year", "season", "paper", "variant", "question", "filename", "text"```


### Output
The program will output a pdf file in a test.pdf file in the output folder.
The pdf file will contain all the pages of the matching questions.