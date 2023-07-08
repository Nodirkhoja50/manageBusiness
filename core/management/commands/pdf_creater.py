'''from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from PyPDF2 import PdfReader, PdfWriter

# Create a new PDF
pdf = SimpleDocTemplate("output.pdf", pagesize=letter)

# Define the data for the table
data = [
    ["Name", "Age", "Country"],
    ["John Doe", "30", "USA"],
    ["Jane Smith", "25", "Canada"],
    ["David Lee", "35", "UK"]
]

# Define the table style
table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
])

# Create the table
table = Table(data)
table.setStyle(table_style)

# Build the PDF document
pdf.build([table])





'''


'''from fpdf import FPDF

pdf = FPDF('P','mm','Letter')

pdf.add_page()

pdf.set_font('helvetica','',16)



pdf.cell(400,0,"hello world",ln=True)
pdf.cell(70,20,"22")
'''

'''import PyPDF2
from fpdf import FPDF





def full_info_pastel(file,sana, katta, kichkina, nalichka, gastiny, jami):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica','', size=12)
    extracted_text = f" sana:{sana}\n katta:{katta}\n kichkina:{kichkina}\n nalichka:{nalichka}\n gastiny:{gastiny}\n jami:{jami}\n\n\n"
    num_pages = 0
    try:
        with open(file, 'rb') as file:
        
        # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Get the number of pages in the PDF
            num_pages = len(pdf_reader.pages)

    # Extract text from each page
    except:
        if num_pages == 0:
            pdf.cell(extracted_text)
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        extracted_text += '\n' + page.extract_text()


    
    # Create a new PDF object
    
    

    # Add the extracted text to the new PDF
    pdf.multi_cell(100, 10, extracted_text,ln=True)

    # Save the new PDF file
    pdf.output(file)

'''
import PyPDF2
from fpdf import FPDF

def full_info_pastel(file, sana, katta, kichkina, nalichka, gastiny, jami):
    extracted_text = f"\n\nsana:{sana}\nkatta:{katta}\nkichkina:{kichkina}\nnalichka:{nalichka}\ngastiny:{gastiny}\nxisob:{jami}"

    # Check if the file exists
    try:
        with open(file, 'rb') as file_obj:
            
            # Check if the file is empty
            if file_obj.read(1):
                # If the file is not empty, reset the file pointer
                file_obj.seek(0)
                
                # Create a PDF reader object
                pdf_reader = PyPDF2.PdfReader(file_obj)

                # Extract existing text from each page
                existing_text = ""
                for page in pdf_reader.pages:
                    existing_text += page.extract_text()

                # Append the new text to the existing text
                extracted_text = existing_text + extracted_text
            else:
                # If the file is empty, use the new text as it is
                #pdf.cell(extracted_text)
                pass

    except FileNotFoundError:
        # If the file does not exist, use the new text as it is
        pass

    # Create a new PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', '', size=12)

    # Add the extracted text to the new PDF
    pdf.multi_cell(100, 10, extracted_text, ln=True)

    # Save the new PDF file
    output_file = file # Specify the desired output file path
    pdf.output(output_file)




