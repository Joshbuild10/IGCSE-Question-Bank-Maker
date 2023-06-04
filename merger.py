import copy
import fitz

# Class to merge multiple source pdfs into one pdf
class Merge:
    def __init__(self, sources, outputPath):
        self.border = 20
        self.sources = sources
        self.output = outputPath
        self.name_tracker = []
        self.tmpPdf = fitz.open()
        self.spacing = 0
        self.loadPages()
        self.mergePages()

    # Loads all pages from the sources into the pages array
    def loadPages(self):
        self.sources.sort(key=lambda x: len(fitz.open(x)))
        for paper in self.sources:
            reader = fitz.open(paper)
            self.tmpPdf.insert_pdf(reader)
            for page in reader:
                self.name_tracker.append(paper)

    # Merges all pages into one pdf, allowing for multiple smaller pages to be merged into one A4 page
    def mergePages(self):
        height = self.border
        pwidth, pheight = fitz.paper_size("a4")
        page_number = 0
    
        writer = fitz.open()
        out_page = writer.new_page(-1, width = pwidth, height = pheight)

        for index, input_page in enumerate(self.tmpPdf):
            
            # Get the height and rectangle of the current page
            cropbox = input_page.rect
            cur_height = cropbox.y1 - cropbox.y0

            # If the current page is too big to fit on the current page, add a new page
            if (cur_height + height) > pheight:
                out_page = writer.new_page(-1, width = pwidth, height = pheight)
                height = self.border
                page_number += 1
            
            # Get the rectangle where the page will be placed
            outbox = fitz.Rect(0, height, pwidth, height + cur_height)
            # Add the page to the buffer page
            out_page.show_pdf_page(outbox, self.tmpPdf, index, clip = cropbox)
            
            # Update the height
            height += cur_height + self.spacing

            # Print statement to show progress
            print(f"\r{self.name_tracker[index]} on page {page_number} loaded into pdf", end=" ")

        print("\n All pages loaded into pdf", end=" ")

        # Write the merged pdf to the output file
        writer.save(self.output, garbage=4, deflate=True, clean=True)
