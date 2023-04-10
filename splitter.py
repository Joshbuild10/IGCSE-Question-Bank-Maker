from pypdf import PdfWriter, PdfReader, Transformation, PaperSize
import copy
import os
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Class to split a pdf into individual questions and store them in a csv file
class Split:

    def __init__(self, path, crawl=True):
        self.paths = []

        # If crawl is true, crawl the directory and subdirectories for all pdfs
        if crawl:
            self.crawl(path)
        else:
            self.paths.append(path)

        for path in self.paths:
            #print(path)
            self.writer = PdfWriter()
            self.reader = PdfReader(path)
            self.questionArr, self.paper, self.rows = [], [], []
            self.info = {}
            self.text = ""
            self.curCoords = {"y1": 0, "y2": 0}
            self.border = 45
            self.extract_questions()
            if not self.check_order():
                print(path, "Error loading all questions")
                continue
            self.get_info(path)
            self.split_questions()
            self.to_csv()

        # Clear duplicates from the csv file
        clear_duplicates()

    def crawl(self, path):
        rootdir = os.fsencode(path)

        # Split all pdfs in the root directory if it exists
        if rootdir is not None:
            if os.path.isfile(rootdir):
                self.paths.append(rootdir.decode('UTF-8'))
            elif os.path.exists(rootdir):
                for subdir, dirs, files in os.walk(rootdir):
                    for file in files:
                        filepath = (subdir + os.sep.encode('UTF-8') + file).decode('UTF-8')
                        if filepath.endswith(".pdf") and "qp" in filepath:
                            self.paths.append(filepath)

    def extract_questions(self):
        for page, content in enumerate(self.reader.pages):
            self.flag = 0
            content.extract_text(visitor_text=self.flag_blank)
            if not self.flag:
                self.newPage = len(self.paper)
                content.extract_text(visitor_text=self.locate_questions)
                self.paper.append(copy.deepcopy(self.reader.pages[page]))


    # Gets the name and info of the paper from the filename
    def get_info(self, path):
        temp_info = path[path.rfind(os.sep) + 1: -4].upper().split('_')

        # Stores the info in a dictionary
        self.info = {"subject_code": temp_info[0], "year": f"20{temp_info[1][1:]}", "season": temp_info[1][0],
                     "paper": temp_info[3], "name": f"{temp_info[0]}_{temp_info[1]}_{temp_info[3]}"}

    # Splits the questions into individual pdfs
    def split_questions(self):

        # Iterates through all questions and splits them into individual pdfs
        for index, question in enumerate(self.questionArr):
            self.text = ""
            curPdf = PdfWriter()
            questionNum = question["question"]
            nextQuestion = self.questionArr[index + 1] if index < (len(self.questionArr) - 1) else {"y": self.border, "page": len(self.paper) - 1}
            filename = f"questions{os.sep}{ self.info['subject_code'] }{os.sep}{self.info['year']}{os.sep}{self.info['name'] }-Q{ questionNum }.pdf"

            # Creates a temporary pdf for the text at the side
            packet = io.BytesIO()  # Create a buffer for the new PDF
            can = canvas.Canvas(packet, pagesize=A4)  # Create a canvas object
            can.rotate(90)  # Rotate the canvas 90 degrees
            can.drawString(10, -15, f"{self.info['name'] }-Q{questionNum}")  # Draw the text at a rotated position
            can.save()  # Save the canvas
            packet.seek(0)  # Move to the beginning of the buffer
            label_pdf = PdfReader(packet)  # Create a new PDF with reportlab

            # Iterates through all pages between the current and next question and adds them to the pdf (trimming as needed)
            for i in range(question["page"], nextQuestion["page"] + (1 if (nextQuestion["y"] < 700) else 0)):
                curPage = copy.deepcopy(self.paper[i])

                # Trims the page to contain just the question
                curPage.mediabox.top = question["y"] + 10 if i == question["page"] else curPage.mediabox.top - self.border
                curPage.mediabox.bottom = nextQuestion["y"] if i == nextQuestion["page"] else curPage.mediabox.bottom + self.border

                # Sets the width to A4 size
                curPage.mediabox.right = PaperSize.A4.width

                self.curCoords["y1"] = curPage.mediabox.top
                self.curCoords["y2"] = curPage.mediabox.bottom

                # Extracts the text from the page, so it can be stored in the database
                curPage.extract_text(visitor_text=self.page_text)

                # Transforms the page so it's aligned to bottom
                curPage.add_transformation(Transformation().translate(tx=0, ty= -curPage.mediabox.bottom))

                # Adjusts mediabox accordingly
                curPage.mediabox.top -= curPage.mediabox.bottom
                curPage.mediabox.bottom -= curPage.mediabox.bottom

                # Sets all other boxes to match the mediabox
                curPage.cropbox = curPage.bleedbox = curPage.artbox = curPage.trimbox = curPage.mediabox

                curPdf.add_page(curPage)

            # Compresses the pages in the pdf to reduce file size using compress_content_streams
            for page in curPdf.pages:
                page.merge_page(label_pdf.pages[0])
                page.compress_content_streams()

            os.makedirs(os.path.dirname(filename), exist_ok=True)

            try:
                # Outputs to file with appropriate name
                with open(filename, "wb") as fp:
                    curPdf.write(fp)

                self.rows.append({
                    "subject_code": self.info['subject_code'],
                    "year": self.info['year'],
                    "season": self.info['season'],
                    "paper": self.info['paper'],
                    "question": questionNum,
                    "filename": filename,
                    "text": self.text
                })
            except:
                print(f"Error: Could not write to file {filename}")


    # Writes paper info to the database
    def to_csv(self):

        headers = ["subject_code", "year", "season", "paper", "question", "filename", "text"]

        isExist = os.path.exists(f"questions{os.sep}database.csv")
        with open(f"questions{os.sep}database.csv", "a", newline='', encoding="utf-8") as csvfile:
            cwriter = csv.DictWriter(csvfile, fieldnames=headers)
            if not isExist:
                cwriter.writeheader()
            cwriter.writerows(self.rows)


    # Removes blank and additional pages from the document
    def flag_blank(self, text, cm, tm, fontDict, fontSize):
        x = int(tm[4])
        y = int(tm[5])

        # Removes all whitespace and makes text uppercase
        text = text.replace(" ", "").upper()

        # Checks conditions for a blank/additional page
        if ((0 < len(text))
            and (("BLANKPAGE" in text) or ("ADDITIONALPAGE" in text))
            and "Bold" in fontDict['/BaseFont']):
            self.flag = 1


    # Locates question numbers, and stores their positions in an array
    def locate_questions(self, text, cm, tm, fontDict, fontSize):
        x = int(tm[4])
        y = int(tm[5])


        try:
            # Extracts digits from the text
            numbers = ''.join(map(str, [int(i) for i in text if i.isdigit()]))
        except:
            print("Error extracting digits")
            return

        if (
            (0 < len(numbers) < 3)
            and x < 120
            and (self.border <= y <= self.reader.pages[0].mediabox.top - 40)
            and "Bold" in fontDict['/BaseFont']
            and (text[0].isnumeric()
                or ("Question" in text and len(text) < 12)
                or text[len(text)-1].isnumeric())):
            self.questionArr.append({
                "question": numbers,
                "x": x,
                "y": y,
                "page": self.newPage})

    def page_text(self, text, cm, tm, fontDict, fontSize):
        y = int(tm[5])
        if self.curCoords["y2"] < y < self.curCoords["y1"]:
            self.text += "".join(text.split()).upper()

    # Function to check if the question numbers are in numerical order, if not throw an error
    def check_order(self):
        for i in range(1, len(self.questionArr)):
            if int(self.questionArr[i]["question"]) != (int(self.questionArr[i-1]["question"]) + 1):
                print("Error: Question numbers are not in order")
                return False
        return True

# Removes duplicate entries from the csv based on filename column
def clear_duplicates():
    if (os.path.exists(f"questions{os.sep}database.csv")):
        # Open the csv file and read the lines
        with open(f"questions{os.sep}database.csv", encoding="utf-8") as f:
            lines = f.readlines()
        # Get the index of the filename column from the header line
        filename_index = lines[0].split(",").index("filename")
        # Create a set to store the filenames that have been seen
        seen_filenames = set()
        # Create a list to store the lines that are not duplicates
        new_lines = []
        # Loop through the lines and check the filename column
        for line in lines:
            # Get the filename from the line
            filename = line.split(",")[filename_index]
            # If the filename is not in the seen set, add it to the new lines and the seen set
            if filename not in seen_filenames:
                new_lines.append(line)
                seen_filenames.add(filename)
        # Write the new lines to the csv file
        with open(f"questions{os.sep}database.csv", 'w', encoding="utf-8") as t:
            t.writelines(new_lines)