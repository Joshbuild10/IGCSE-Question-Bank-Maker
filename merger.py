from pypdf import PdfWriter, PdfReader, Transformation, PaperSize
import copy


# Class to merge multiple source pdfs into one pdf
class Merge:
    def __init__(self, sources, outputPath):
        self.border = 20
        self.sources = sources
        self.output = outputPath
        self.pages = []
        self.loadPages()
        self.mergePages()

    # Loads all pages from the sources into the pages array
    def loadPages(self):
        self.sources.sort(key=lambda x: len(PdfReader(x).pages))
        for paper in self.sources:
            reader = PdfReader(paper)
            for page in reader.pages:
                page.cropbox = page.mediabox
                self.pages.append({"page": page, "filename": paper})

    # Merges all pages into one pdf, allowing for multiple smaller pages to be merged into one A4 page
    def mergePages(self):
        writer = PdfWriter()
        temp_page = PdfWriter().add_blank_page(height=PaperSize.A4.height, width=PaperSize.A4.width)
        height = self.border
        page_number = 0

        for rawpage in self.pages:
            page = copy.deepcopy(rawpage["page"])
            cur_height = page.cropbox[3] - page.cropbox[1]

            # If the current page is too big to fit on the current page, add a new page
            if (cur_height + height) > PaperSize.A4.height:
                writer.add_page(temp_page)
                temp_page = PdfWriter().add_blank_page(height=PaperSize.A4.height, width=PaperSize.A4.width)
                height = self.border
                page_number += 1

            # Offset to determine the right position on the page relative to the top
            offset = (PaperSize.A4.height - height) - page.cropbox[3]

            # Print statement to debug values, and page data
            # print(
            #    f"Page {page_number} qheight: {cur_height}, pageheight: {height}, offset: {offset}, cropbox: {page.cropbox},"
            #    f" filename: {rawpage['filename']}")

            # Add the transformation to the page to position it correctly
            page.add_transformation(Transformation().translate(tx=0, ty=offset))

            # Update the cropbox to match the new position
            page.cropbox[3] += offset
            page.cropbox[1] += offset

            # Set all other boxes to match the cropbox
            page.artbox = page.mediabox = page.bleedbox = page.trimbox = page.cropbox

            # Merge the page into the current page and update the height (with padding)
            temp_page.merge_page(page)
            height += cur_height + 10

        # Add the last page
        writer.add_page(temp_page)

        # Write the merged pdf to the output file
        with open(self.output, "wb") as fp:
            writer.write(fp)
